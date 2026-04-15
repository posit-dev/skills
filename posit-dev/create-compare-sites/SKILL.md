---
name: create-compare-sites
description: >
  Use when adding a site-comparison script to a documentation repository.
  Triggered by requests to "compare two builds", "add visual regression testing",
  "set up a compare-sites script", or "detect differences between site versions".
  Generates a TypeScript script that crawls two builds of a documentation site
  using Playwright and Claude vision via AWS Bedrock to detect visual, HTTP, and
  console/network regressions. Requires AWS credentials with Bedrock access.
metadata:
  author: E Nelson
  version: "1.0"
license: MIT
---

# Create a Compare-Sites Script

Generate a TypeScript script that compares two builds of a documentation site
by crawling every page and reporting differences in HTTP status, console/network
errors, and visual rendering. Uses Playwright for page capture and Claude vision
via AWS Bedrock for screenshot comparison.

## Workflow

### Stage 1: Explore the Repository

Before writing any files:

1. Look for existing test directories (`tests/`, `test/`, `e2e/`, `scripts/`).
2. Check for `package.json` at the root and in any test directory — note existing
   scripts, dependencies, and whether TypeScript is already configured.
3. Look for `tsconfig.json` files.
4. Scan the site source for patterns that affect customization:
   - Does the site embed Shinylive apps? (look for `shinylive` in source files,
     `_quarto.yml`, or `requirements.txt`)
   - What third-party services are used? (look for analytics, CDN, or external
     embeds in layout/template files)

**Output directory:** Use an existing test directory if one clearly fits.
Otherwise create `tests/`.

### Stage 2: Ask the User

Ask the following in a single message (all at once):

1. **AWS region** — where to run Bedrock inference (default: `us-east-1`)
2. **Default ports** — old build port and new build port (default: `1414` and `1415`)
3. **Additional noise URL patterns** — beyond the defaults (Google Analytics,
   GTM, Plausible, shinyapps.io), any other third-party URLs to silence
   (e.g., internal CDNs, embed providers)?
4. **Shinylive** — does this site embed Shinylive apps? (affects the visual
   comparison prompt and adds a `SHINYLIVE_NOT_LOADED` signal to the output)

If the answers are obvious from the repo (e.g., Shinylive is clearly present or
absent), skip those questions and note your inference.

### Stage 3: Read the Templates

Read both reference files in full before generating any code:

- `references/compare-sites.ts` — main comparison script template
- `references/shared.ts` — shared utilities template

### Stage 4: Generate Files

Create the following files in the output directory, customized for this repo:

#### `compare-sites.ts`

Customizations from the template:
- Set `DEFAULT_OLD` and `DEFAULT_NEW` to the user's ports
- Set `awsRegion` to the user's AWS region
- If the site does **not** use Shinylive: remove the `SHINYLIVE_NOT_LOADED`
  branch from `compareScreenshots()`, remove it from `diffSnapshots()`, remove
  the `unverified` tracking in `main()`, and remove it from `writeReport()`
- If the site **does** use Shinylive: keep the `SHINYLIVE_NOT_LOADED` handling
  as-is from the template
- Update the usage comment at the top to use the actual repo's build command
  instead of `make site` (infer from `Makefile`, `package.json` scripts, or
  `_quarto.yml` project type)

#### `shared.ts`

Customizations from the template:
- Add any repo-specific noise URL patterns to `NOISE_PATTERNS`

#### `package.json`

If a `package.json` already exists in the output directory, add to it:
```json
{
  "scripts": {
    "compare": "npx tsx compare-sites.ts"
  },
  "dependencies": {
    "@anthropic-ai/bedrock-sdk": "^0.12.0",
    "playwright": "^1.47.0",
    "sharp": "^0.33.0"
  },
  "devDependencies": {
    "tsx": "^4.0.0",
    "typescript": "^5.0.0",
    "@types/node": "^20.0.0"
  }
}
```
If no `package.json` exists, create a minimal one with `"type": "module"` and
the above scripts and dependencies.

#### `tsconfig.json`

If no `tsconfig.json` exists in the output directory, create:
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "outDir": "dist"
  },
  "include": ["*.ts"]
}
```

### Stage 5: Print Run Instructions

After writing the files, output:

```
## Setup

cd <output-directory>
npm install
npx playwright install chromium

## Usage

# Terminal 1 — serve old build
<old-build-command> && npx serve <build-dir> -l <old-port>

# Terminal 2 — serve new build
<new-build-command> && npx serve <build-dir> -l <new-port>

# Terminal 3 — run comparison
npm run compare

# Options
npm run compare -- --filter /docs      # only pages matching /docs
npm run compare -- --exclude /archive  # skip pages matching /archive
npm run compare -- --old http://... --new http://...  # custom URLs
```

Fill in the actual build command and build output directory inferred from
the repo (e.g., `_site`, `_book`, `_build`, `public`, `dist`).

## Notes

- The script discovers pages from `/llms.txt` or `/sitemap.xml` — at least one
  must be accessible on each build.
- AWS credentials must be available in the environment (`AWS_PROFILE`,
  `AWS_ACCESS_KEY_ID`/`AWS_SECRET_ACCESS_KEY`, or instance role).
- The script exits with code 1 if any regressions are found (useful for CI).
- Reports are written to `<output-directory>/compare-sites-<timestamp>.md`.
