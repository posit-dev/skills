# Diagnosis: Measurement Tools and Multi-User Scaling

Read this when you need to profile, load-test, or reason about multi-user
capacity. Choose the tool by question: **OpenTelemetry** — "which reactive
code is slow"; **py-spy** — "where does CPU time go in the live process";
**timeit** — "which implementation is faster"; **shinyloadtest** — "how many
users can this app support".

Remember: measurement confirms and discovers — it is not a prerequisite for
applying the safe fixes from the smell scan. If tooling is slow or ambiguous,
fix what the scan found and record what couldn't be verified.

## OpenTelemetry — where the time goes (built into Shiny ≥ 1.6)

Shiny emits spans for session lifecycle, each reactive update cycle, and
every `@reactive.calc` / `@reactive.effect` / `@render.*` / extended task —
with the source file and line attached. Zero app code needed:

```bash
uv pip install "shiny[otel]"

# Console exporter while developing:
SHINY_OTEL_COLLECT=reactivity \
opentelemetry-instrument --traces_exporter console --logs_exporter console \
    --metrics_exporter none shiny run app.py
```

Interact with the app, then read the span hierarchy:

```text
session_start
  └─ reactive_update
      ├─ reactive.calc filtered_data    1.2 s  app.py:42
      └─ output table                   0.8 s  app.py:55
```

- **Widest repeated spans** are the bottleneck; one-time towers at session
  start are per-session setup work (data-loading.md, Rule 1).
- `SHINY_OTEL_COLLECT` levels, least to most detail: `none`, `session`,
  `reactive_update` (one span per flush — a good production level),
  `reactivity` (a span per calc/effect/output — the development level),
  `all` (currently same as `reactivity`).
- Production overhead control: lower the level, sample
  (`OTEL_TRACES_SAMPLER=parentbased_traceidratio`,
  `OTEL_TRACES_SAMPLER_ARG=0.1`), and suppress hot or sensitive reactives
  with `@otel.suppress` (must sit **below** the `@render`/`@reactive`
  decorator; the setting is captured when the reactive object is created).
- Export to any OTLP backend (Logfire, Jaeger, Honeycomb, Datadog...) by
  launching under `opentelemetry-instrument` with the standard `OTEL_*`
  env vars. Don't call `trace.set_tracer_provider()` in app code under the
  wrapper — it's ignored (exception: SDKs that manage OTel themselves, e.g.
  `logfire.configure()`, where you run `shiny run` directly).

## py-spy — sampling profiler for the live process

A Shiny app is an ordinary Python process, so standard profilers work.
`py-spy` samples a running process without restarting it:

```bash
pip install py-spy
py-spy top --pid <PID>                              # live "top" of Python stacks
py-spy record -o profile.svg --pid <PID> --duration 30   # flame graph
```

Attach, reproduce the slowness by clicking through the app, then read the
flame graph: widest blocks across the bottom are where CPU time goes — often
pandas/numpy/DuckDB internals rather than your code. This is the tool when
you need to see *inside* heavy sync calls that OTel only times as a whole.

Limitations: time blocked on network/disk shows as idle stacks, not work
(that's the hint the operation is I/O-bound — async-tasks.md); it cannot see
inside `ProcessPoolExecutor` workers — profile the synchronous function
standalone instead.

## Timing checks — verify scope, not just speed

The cheapest diagnostic in the toolkit: stderr timestamps around suspect
work.

```python
import sys, time
t0 = time.perf_counter()
scorecard = pd.read_csv("scorecard.csv")
print(f"load scorecard: {time.perf_counter() - t0:.3f}s",
      file=sys.stderr, flush=True)
```

- A startup line that prints on **every page open** is per-session work that
  belongs in module scope (data-loading.md).
- Wrap an interactive path and click through: the delta between prints tells
  you which stage eats the interaction budget.

## Compare two implementations with `timeit`

```bash
python -m timeit -s "import app" "app.heavy_function(1_000)"
# or in a scratch script: time 3–5 repeats of A(x) vs B(x) with time.perf_counter()
```

Read **memory** alongside speed (`tracemalloc`), and remember the biggest wins
are ordered: do it once instead of N times (hoist out of loops/reactives) >
vectorize (numpy/polars) > pre-allocate > micro-optimize.

## Inspecting live state: test mode (not timing)

`SHINY_TESTMODE=1 shiny run app.py` serves a read-only JSON snapshot of each
session's `input`/`output`/`export` values (`export_test_values()` exposes
internal calcs to it). Useful for verifying *what* computed, and asserting
before/after equivalence cheaply.

## shinyloadtest — capacity, not single-session speed

Only when the complaint is "dies with N users". `shinyloadtest` (the
TypeScript successor to shinycannon — Node.js 20+, `npm install -g
shinyloadtest`) records a session and replays it with concurrent workers;
it works against any deployed Shiny app, including Python ones:

```bash
# 1. Record one realistic session (proxy in front of the app; click through;
#    close the browser tab to stop)
shinyloadtest record http://app.example.com/            # -> recording.log

# 2. Replay with simulated users — from a DIFFERENT machine on the same network
shinyloadtest replay recording.log http://app.example.com/ \
    --workers 1  --loaded-duration-minutes 5 --output-dir run1     # baseline
shinyloadtest replay recording.log http://app.example.com/ \
    --workers 20 --loaded-duration-minutes 5 --output-dir run20

# 3. Analyze
shinyloadtest report run1 run20 --format text    # or default HTML dashboard
```

Reading the report: loaded session durations ≈ the 1-user baseline mean the
app handles that load; 2×+ means users are queuing on the app process. Always
take the 1-user baseline first. Workers loop the recording, so workers ≠
unique sessions, and sessions are sticky per browser — don't fake a load test
by opening 5 tabs. Legacy R toolchain (`shinyloadtest` R package +
shinycannon) reads the same recording and log formats if you prefer R for
the analysis step.

If the load test shows degradation, the code fixes in caching.md and
async-tasks.md come before the infrastructure knobs below.

## The multi-user process model

One Shiny for Python process = one asyncio event loop = one Python thread:

- **Reactive functions run serially, never concurrently — even async ones,
  even across sessions.** One blocking call ties up every session on the
  process. This is why code fixes come first (async-tasks.md).
- **Sessions hold state in memory**, so a browser must keep talking to the
  *same* process: sticky-session load balancing is mandatory whenever more
  than one app process serves a URL. This rules out `uvicorn --workers >1`,
  the `WEB_CONCURRENCY` env var, and multi-worker Gunicorn — they'll
  *appear* to work but features using HTTP round-trips (file uploads,
  downloads) will randomly fail (py-shiny issue #335).
- **Scale by running multiple single-worker processes** (one
  `shiny run`/uvicorn each) behind a sticky-session proxy (nginx
  `ip_hash`/cookie-hash routing, an ALB with session affinity, ...). The
  community `shinynx` package packages this nginx pattern for py-shiny.
- **Module-scope data and in-memory caches are per-process**: 4 processes =
  4 cold-start loads, 4 copies of the data in RAM, 4 independent cache
  misses. Use disk caches (caching.md) to share; watch RAM = processes ×
  module data when sizing (the most common OOM).

## Deployment knobs (last resort, after code fixes)

**Posit Connect** (content's Runtime tab — check your server's defaults):

| Setting | Meaning |
|---|---|
| Max processes | Upper bound of app processes per node |
| Min processes | Keep processes warm — raise toward Max when the app preloads data at process start (avoids cold starts) |
| Max connections per process | Concurrent browser connections per process |
| Load factor | Fraction of capacity that triggers a new process; lower = spawn sooner |

Capacity ≈ Max processes × Max connections per process. 503s/timeouts under
load mean raise Max processes or connections; every added process re-pays
module-scope loads and memory. Changes take effect for new connections.

**Posit Connect Cloud** combines per-instance resources (RAM 256 MB–8 GB,
1 GB default) with run settings (worker processes per instance, min/max
instances, idle timeout, max connections per worker — default 50 — and load
factor). OOM shows up as a grey screen and "killed" in logs — fix with a
bigger instance or *fewer* workers.

More processes is the easy, costly fix; code optimization is the durable one.
When recommending infrastructure changes, hand the user the load-test
numbers that justify them.

## Recording results

End every diagnosis with re-checkable numbers: seconds to first usable page,
seconds per key interaction, slow spans from the OTel trace, and workers ×
users sustained at < 2× baseline latency. These are the acceptance criteria
for every fix.

## Further reading

- OpenTelemetry in Shiny for Python:
  <https://shiny.posit.co/py/docs/opentelemetry.html>
- Non-blocking operations: <https://shiny.posit.co/py/docs/nonblocking.html>
- py-spy: <https://github.com/benfred/py-spy>
- shinyloadtest: <https://github.com/posit-dev/shinyloadtest>
- Self-hosted deployments (sticky sessions, why not Gunicorn):
  <https://shiny.posit.co/py/get-started/deploy-on-prem.html>
- uvicorn multi-worker limitation: <https://github.com/posit-dev/py-shiny/issues/335>
- Load-test case study (methodology):
  <https://rstudio.github.io/shinyloadtest/articles/case-study-scaling.html>
