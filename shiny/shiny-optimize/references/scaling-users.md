# Scaling to Many Users (Brief)

The core skill is code-level optimization — this file is the minimum needed to
reason about *multi-user* problems and to hand off cleanly to deployment
tuning when code fixes are exhausted. Read it when the complaint is "it works
for me but degrades with several users", or before advising on deployment
settings.

## The process model (why user count changes everything)

One Shiny R process is **single-threaded**: it serves its sessions'
computations one at a time, roughly 5–30 simple requests/second. Apps scale by
running **multiple R processes** (workers), each with its own memory and its
own globals/caches, with connections distributed across them.

Code-level implications you must know before scaling:

- **Blocking operations** (sync sleeps, long computes without ExtendedTask)
  tie up the whole *process*, i.e. every user on it — this is why code fixes
  (async-tasks.md, caching.md) come first.
- **Globals and app-level caches are per-process**: with 3 worker processes,
  `bindCache(cache = "app")` in memory exists 3× independently. Use
  `cachem::cache_disk()` for a cache shared across processes (caching.md).
- **Global-scope data loads are per-process**: 3 workers = 3 copies of the
  2 GB data frame in RAM, and 3 cold starts. Lean startup + lazy reactives
  matter more as process count grows.
- Sessions are **sticky** (routed by cookie): one browser's tabs all hit the
  same worker — don't diagnose capacity by opening 5 tabs; use shinyloadtest.

## Load testing loop (recap)

Record a realistic session, replay at 1 user and N users with shinycannon from
a separate machine, compare session durations and latency histograms
(diagnosis.md has the full workflow). Degraded sessions at N users + code
fixes already applied → the levers below.

## Posit Connect scheduler knobs (content's Runtime tab)

| Setting | Default | Meaning |
|---|---|---|
| Max processes | 3 | Upper bound of R workers for the content |
| Max connections per process | 20 | Concurrent connections per worker |
| Load factor | 0.5 | Fraction of capacity in use that triggers a new process; lower = spawn sooner |
| Min processes | 0 | Keep processes warm — set near Max when the app preloads shared data at process start (avoids cold starts) |

Capacity ≈ Max processes × Max connections per process. Monitor
`worker.pool.utilization` (near 1.0 = saturated). Watch total RAM: many
processes × global data = the most common OOM.

Prerendered Shiny documents (`runtime: shiny_prerendered`) reduce per-user
memory for Rmd-based apps because most code runs once at render time rather
than per session.

## shinyapps.io knobs

- Instance RAM sizes: 256 MB → 8 GB (large/1 GB is default). Each worker is an
  R process consuming RAM; **OOM shows up as a grey screen and "killed" in
  logs** — fix with a bigger instance or *fewer* workers.
- Tunables (Basic plan+): workers per instance, max instances, min instances
  (always-on), idle timeout, max connections per worker (default 50), Worker
  Load Factor (default 5% — a new worker spawns at ~2–3 connections), Instance
  Load Factor (default 50%).
- Defaults support ~50 conns/worker × 3 workers × 50% ⇒ a new instance around
  the 76th connection; hard ceiling 3 × 50 = 150 unless raised.

## The honest summary

More processes/instances is the easy, *costly* fix; code optimization is the
durable one. As the Shiny Server Pro docs put it: "no settings will make up
for poorly written code — profile first." When you do recommend infrastructure
changes, hand the user the load-test numbers (diagnosis.md) that justify them,
plus the process-model caveats above (per-process caches/globals) so the
deployment choice doesn't silently break app-level assumptions.
