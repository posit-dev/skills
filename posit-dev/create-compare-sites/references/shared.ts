/**
 * Shared utilities for compare-sites.ts.
 *
 * CUSTOMIZATION:
 *   - Add repo-specific noise URL patterns to NOISE_PATTERNS.
 */

import { type Browser, type ConsoleMessage, type Request } from "playwright";
import { fileURLToPath } from "url";
import { dirname } from "path";

// ---------------------------------------------------------------------------
// ESM __dirname shim
// ---------------------------------------------------------------------------

export const __dirname = dirname(fileURLToPath(import.meta.url));

// ---------------------------------------------------------------------------
// Noise filtering
// ---------------------------------------------------------------------------

// CUSTOMIZE: add repo-specific third-party URLs to suppress from error reports
const NOISE_PATTERNS = [
  "google-analytics.com",
  "googletagmanager.com",
  "plausible.io/js",
  "plausible.io/api",
  "shinyapps.io",
];

// Error text patterns to suppress regardless of URL
const NOISE_ERROR_PATTERNS = [
  "ERR_BLOCKED_BY_RESPONSE",
];

export function isNoise(url: string): boolean {
  return NOISE_PATTERNS.some((p) => url.includes(p));
}

// ---------------------------------------------------------------------------
// Page list discovery
// ---------------------------------------------------------------------------

export async function getPages(baseUrl: string): Promise<string[]> {
  for (const path of ["/llms.txt", "/sitemap.xml"]) {
    try {
      const res = await fetch(`${baseUrl}${path}`);
      if (!res.ok) continue;
      const text = await res.text();

      let pages: string[];
      if (path === "/llms.txt") {
        pages = [...text.matchAll(/\]\((.+?)\.llms\.md\)/g)].map((m) => `/${m[1]}.html`);
      } else {
        pages = [...text.matchAll(/<loc>(.+?)<\/loc>/g)]
          .map((m) => new URL(m[1]).pathname)
          .filter((p) => p.endsWith(".html"));
      }

      return pages.filter((p) => p.startsWith("/"));
    } catch {
      continue;
    }
  }
  return [];
}

// ---------------------------------------------------------------------------
// Concurrency pool
//
// Safety: `nextIndex++` is a synchronous read-modify-write. This is safe in
// Node.js's single-threaded event loop because workers only yield at `await`.
// ---------------------------------------------------------------------------

export async function pooled<T, R>(
  items: T[],
  concurrency: number,
  fn: (item: T) => Promise<R>,
  onError: (item: T, index: number, err: unknown) => R,
): Promise<R[]> {
  const results: R[] = new Array(items.length);
  let nextIndex = 0;

  async function worker() {
    while (nextIndex < items.length) {
      const i = nextIndex++;
      try {
        results[i] = await fn(items[i]);
      } catch (err) {
        results[i] = onError(items[i], i, err);
      }
    }
  }

  await Promise.all(Array.from({ length: Math.min(concurrency, items.length) }, worker));
  return results;
}

// ---------------------------------------------------------------------------
// Retry wrapper for transient Bedrock errors (throttling, transient 5xx)
// ---------------------------------------------------------------------------

function isRetryable(err: unknown): boolean {
  const msg = err instanceof Error ? err.message : String(err);
  return /429|503|500|timeout|ECONNRESET|ETIMEDOUT/i.test(msg);
}

export async function withRetry<T>(fn: () => Promise<T>, retries = 3, delayMs = 2000): Promise<T> {
  if (retries < 1) throw new Error("retries must be >= 1");
  for (let i = 0; i < retries; i++) {
    try {
      return await fn();
    } catch (err) {
      const isLast = i === retries - 1;
      if (isLast || !isRetryable(err)) throw err;
      await new Promise((r) => setTimeout(r, delayMs * (i + 1)));
    }
  }
  throw new Error("withRetry: exhausted retries");
}

// ---------------------------------------------------------------------------
// Error message normalization (strip dynamic content before comparing)
// ---------------------------------------------------------------------------

export function normalizeError(msg: string): string {
  return msg
    .replace(/https?:\/\/\S+/g, "<url>")
    .replace(/^\s*at\s+\S.*$/gm, "")
    .replace(/[a-f0-9]{8,}/gi, "<id>")
    .replace(/\d{4,}/g, "<n>")
    .trim();
}

// ---------------------------------------------------------------------------
// Shared page capture — handles context lifecycle, event wiring, navigation
// ---------------------------------------------------------------------------

export interface CapturedPage {
  httpStatus: number | null;
  consoleErrors: string[];
  networkErrors: string[];
  /** Release the browser context. Always call this when done. */
  close: () => Promise<void>;
  /** Take a screenshot. Caller is responsible for resizing. */
  screenshot: (options?: { fullPage?: boolean }) => Promise<Buffer>;
}

export async function capturePage(
  browser: Browser,
  url: string
): Promise<CapturedPage | { error: string }> {
  let context;
  const consoleErrors: string[] = [];
  const networkErrors: string[] = [];

  try {
    context = await browser.newContext({ viewport: { width: 1280, height: 900 } });
    const page = await context.newPage();

    page.on("console", (msg: ConsoleMessage) => {
      if (msg.type() === "error") {
        const text = msg.text();
        if (!text.startsWith("preload error:") && !NOISE_ERROR_PATTERNS.some((p) => text.includes(p)))
          consoleErrors.push(text);
      }
    });

    page.on("requestfailed", (req: Request) => {
      try {
        const reqUrl = req.url();
        const errorText = req.failure()?.errorText ?? "";
        if (!isNoise(reqUrl) && !NOISE_ERROR_PATTERNS.some((p) => errorText.includes(p)))
          networkErrors.push(`${errorText}: ${reqUrl}`);
      } catch {
        // Swallow: request objects can be invalid when context is closing
      }
    });

    const response = await page.goto(url, {
      waitUntil: "domcontentloaded",
      timeout: 60_000,
    });

    // Wait for network to settle; cap at 5s for pages with persistent connections
    try {
      await page.waitForLoadState("networkidle", { timeout: 5_000 });
    } catch {
      // Expected on pages with persistent WebSocket connections
    }

    // Dismiss cookie consent banner if present
    try {
      await page.getByRole("button", { name: /accept|allow all|i agree/i }).click({ timeout: 2_000 });
      await page.waitForTimeout(300);
    } catch {
      // No consent banner found
    }

    const httpStatus = response?.status() ?? null;

    return {
      httpStatus,
      consoleErrors,
      networkErrors,
      close: () => context!.close(),
      screenshot: async (options) => {
        // Wait for Quarto dev-server render bar to disappear before screenshotting
        try {
          const cancelBtn = page.getByRole("button", { name: /^cancel$/i });
          if (await cancelBtn.isVisible({ timeout: 1_000 })) {
            await cancelBtn.waitFor({ state: "hidden", timeout: 15_000 });
          }
        } catch {
          // No render bar present
        }
        return page.screenshot({ fullPage: options?.fullPage ?? false });
      },
    };
  } catch (err) {
    await context?.close();
    return { error: err instanceof Error ? err.message : String(err) };
  }
}
