# Non-Blocking Operations: ExtendedTask, Threads, and Process Pools

Async is the **last** tool to reach for. It doesn't make any computation
faster — it changes *who waits*. Exhaust elimination (reactive-graph.md) and
caching (caching.md) first: caching gives 10–100×; async gives concurrency at
the cost of serialization overhead and harder debugging.

## Why blocking hurts — and why `async def` doesn't help

Shiny for Python runs on a single asyncio event loop per process, and it
deliberately runs **reactive functions serially, never concurrently — even
when they are `async def`, even across sessions in the same process**. Two
`async` effects that each `await asyncio.sleep(1)` run one after the other;
one user's blocking call freezes every session in the process.

Consequences:

- `async def` on a calc/effect/renderer exists so you can call async-only
  APIs (an async HTTP client, `session.send_custom_message`). **It does not
  make the app faster or more responsive.** Replacing `time.sleep(5)` with
  `await asyncio.sleep(5)` changes nothing for your users.
- A *synchronous* call in any reactive function (`time.sleep`, `requests`,
  a sync DuckDB/pandas query) blocks the event loop itself — nothing in the
  process gets served until it returns. This is the single most destructive
  pattern in a Shiny for Python app, and it's invisible in development with
  one user.

## The decision path

1. Can the operation be **eliminated** (not computed when not shown)?
2. **Cached** (caching.md), so it runs at most once per unique input?
3. **Precomputed** offline (data-loading.md)?
4. Genuinely a request-time, multi-second, user-specific computation (model
   fit on uploaded data, slow external API)? → **Then**
   `@reactive.extended_task` is appropriate.

Async pays off for a few big hotspots. Diffuse small slowness gets *worse*
with async (fixed per-task overhead).

## The `@reactive.extended_task` pattern

The complete, recommended pattern:

```python
import asyncio
from shiny import App, reactive, render, ui

app_ui = ui.page_fluid(
    ui.input_select("model", "Model", ["glm", "rf", "xgb"]),
    ui.input_task_button("fetch", "Fetch data"),
    ui.output_text_verbatim("result"),
)

def server(input, output, session):
    # 1. Declare the task. The function MUST be `async def`, and the body
    #    must NOT read reactive sources — everything it needs is passed in.
    @ui.bind_task_button(button_id="fetch")      # keeps the button busy
    @reactive.extended_task
    async def fetch_model(model_id: str) -> str:
        return await query_slow_api(model_id)    # async I/O: await it

    # 2. Invoke from an effect — reactive values are read HERE and passed
    #    as arguments, snapshotted at invoke time.
    @reactive.effect
    @reactive.event(input.fetch)
    def _():
        fetch_model(input.model())

    # 3. Consume the result reactively — re-runs when the task finishes.
    @render.text
    def result():
        return fetch_model.result()

app = App(app_ui, server)
```

Semantics worth knowing cold:

- `task.result()` — reactive read for consumers: silent exception (blank
  output) before the first run; a special "in progress" state while running
  (this drives the busy indicator); the resolved value on success; the error
  re-raised in the consuming output on failure. **Don't wrap `result()` in
  `@reactive.event`/`isolate()`** — its invalidations are the mechanism.
- `task.status()` — reactive read: `"initial"` | `"running"` |
  `"success"` | `"error"` | `"cancelled"`; drive conditional UI from it.
- `.invoke()` (calling the task object) returns `None` immediately. A second
  invoke while running is **queued**, not parallelized.
  `ui.input_task_button` disables itself while running so repeat clicks can't
  queue silently; `ui.bind_task_button` extends that to the task's full
  lifetime. Plain `ui.input_action_button` gets none of this.
- `task.cancel()` cancels the running invocation and clears the queue.
- The work runs once per invoke, no matter how many consumers read
  `result()`. Route downstream readers through one shared calc that reads
  `result()`; consumers must never call the task themselves.
- Declare the task **inside `server()`** (or Express top level of
  `app.py`) → one instance per session. A module-level declaration is shared
  across all visitors (rarely what you want).
- Extended tasks run on the **same event loop**. `await`ing genuinely async
  I/O is non-blocking; a *synchronous* call inside the async body still
  blocks everything — see the next section.

## Offloading synchronous and CPU-bound work

`@reactive.extended_task` removes you from the reactive flush, but the body
still runs on the event loop. Match the offload to the work:

| Work | Offload |
|---|---|
| Genuinely async API (`httpx`, `asyncpg`) | `await` it directly in the task body |
| Synchronous I/O (sync `requests`, sync DB drivers, `pd.read_csv` of a big file) | `await asyncio.to_thread(fn, args)` |
| CPU-bound (model fits, heavy pandas/polars transforms, big DuckDB queries) | Module-level `ProcessPoolExecutor` |

```python
import asyncio
import concurrent.futures

pool = concurrent.futures.ProcessPoolExecutor()   # MODULE level — shared

def fit_model(x: float, y: float) -> dict:       # MODULE level — must be
    ...                                          # picklable for processes

def server(input, output, session):
    @reactive.extended_task
    async def train(x: float, y: float) -> dict:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(pool, fit_model, x, y)
    ...

app = App(app_ui, server)
app.on_shutdown(pool.shutdown)                   # clean shutdown — don't skip
```

- **Thread pools don't help CPU-bound work** (the GIL serializes Python
  bytecode; `asyncio.to_thread` only buys you I/O concurrency). CPU-bound →
  process pool.
- Executors must be **module level** (shared across sessions), and worker
  functions for `ProcessPoolExecutor` must be module-level and picklable.
  Register `app.on_shutdown(pool.shutdown)` or you leak processes.
- `asyncio.to_thread` is the one-liner for sync I/O; reach for the explicit
  `ThreadPoolExecutor` only when you need to bound/limit concurrent threads.
- Executors are unavailable under Shinylive/WASM.
- Process pools pay **spawn + serialization** costs: arguments copied in,
  results copied back. Don't ship a 2 GB DataFrame to a worker to add one
  column.

## Hard rules for worker code

1. **No reactive reads inside the task body** (`input.x()`, `reactive.value`,
   calcs all raise). Read reactives in the invoking effect and pass values
   as arguments — they're snapshotted at invoke time; inputs may change
   before the worker starts.
2. **`session` is off-limits** in workers for the same reason.
3. **Plotting happens in the main process.** Matplotlib figures generally
   don't pickle; return data from the worker, build the figure in the
   renderer.
4. **Don't mutate shared module-level objects** in the worker (they may be
   pickled copies, or shared between sessions — either way it's wrong).
5. **Debugging is harder off the flush.** Errors re-raise in the consuming
   output; py-spy and cProfile see less inside pools — profile the
   synchronous version first, convert only the proven hotspot.

## UI expectations

- `ui.input_task_button` shows a busy label and disables itself — feedback
  instead of a frozen app.
- While a task runs the rest of the session stays live: verify with a
  ticking output (`reactive.invalidate_later(1)` clock) in another session
  or another output.
- Busy indicators for *outputs* (rendering-ui.md) complement task buttons:
  buttons for triggered work, spinners for render-time work.

## Further reading

- Non-blocking operations (the canonical article):
  <https://shiny.posit.co/py/docs/nonblocking.html>
- `reactive.extended_task`:
  <https://shiny.posit.co/py/api/core/reactive.extended_task.html>
- Managing long-running operations in Shiny (Joe Cheng, Posit Open Source
  2024): <https://opensource.posit.co/resources/videos/2024-05-15_joe-cheng-managing-long-running-operations-in-shiny-posit/>
