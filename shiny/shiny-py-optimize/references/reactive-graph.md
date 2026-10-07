# The Reactive Graph: Computing Less Without Changing Behavior

Most "slow everywhere" apps are slow because the reactive graph does more work
than the user's actions require. Everything here changes *when* and *how often*
code runs, never what it computes.

## Why over-recomputation happens

Shiny works in **flush cycles**: receive changed inputs → invalidate everything
downstream → re-execute → send results. Three consequences:

1. Every read of a reactive source (`input.x()`, a `reactive.value`, a
   `@reactive.calc`) inside a reactive context registers a dependency; when
   the source invalidates, everything downstream re-executes — **even if the
   result would be identical**. Invalidation is all-or-nothing per node.
2. Dependencies are discovered at execution time, so conditional reads
   (`if input.mode() == "a": input.a()`) create conditional edges that can
   hide from you.
3. `@reactive.calc`s and outputs are **lazy**: an output that isn't requested
   (hidden, `req()`-failed) pulls nothing upstream. `@reactive.effect`s are
   eager — they re-run whenever dependencies change, whether or not anyone is
   looking.

## Compute once, consume twice: shared `@reactive.calc`

The single most common structural fix. Two outputs that each re-derive the same
thing pay for the derivation on every input change — twice. A `@reactive.calc`
is memoized: it runs once per invalidation no matter how many callers read it.

```python
# Before: duplicated computation
@render.text
def earnings():
    df = scorecard[
        (scorecard["state"] == input.state())
        & (scorecard["sat_avg"] >= input.sat())
    ]
    return fmt_dollars(df["earnings"].mean())

@render.plot
def earnings_plot():
    df = scorecard[
        (scorecard["state"] == input.state())
        & (scorecard["sat_avg"] >= input.sat())   # again!
    ]
    ...

# After: one shared calc, computed once per change
@reactive.calc
def filtered_data():
    return scorecard[
        (scorecard["state"] == input.state())
        & (scorecard["sat_avg"] >= input.sat())
    ]

@render.text
def earnings():
    return fmt_dollars(filtered_data()["earnings"].mean())

@render.plot
def earnings_plot():
    ...
```

A plain `@reactive.calc` remembers only its **latest** value within the
session; revisit a previous input state and it recomputes. For remembering
*previous* values or sharing across sessions, see caching.md.

## Gate with `req()`

`req(x)` raises a *silent* exception that stops the current reactive context
until the condition holds — the standard fix for "everything computes at
startup with empty inputs":

```python
@render.plot
def dist():
    req(input.state())        # blank until a state is chosen — nothing runs
    ...
```

- Falsy values (`None`, `""`, `0`, `False`, empty containers) halt; anything
  else passes through as its value.
- `req(x, cancel_output=True)` keeps the **last rendered output** visible
  instead of blanking it — often the better UX for transient invalid states.

## `reactive.isolate()`: read without depending

`with reactive.isolate():` evaluates immediately with no dependency
registration. Uses:

- **Breaking read/write loops**: an effect that reads and writes the same
  `reactive.value` loops forever without it.
- Reading values inside effects where staleness-until-next-event is intended.
  Never use it to paper over a dependency you don't understand.

(Inside `@reactive.event(...)` the non-event reads are already isolated —
see below.)

## Event-driven execution: `@reactive.event()`

`@reactive.event` restricts a reactive function's dependencies to the listed
events only; all other reactive reads inside the body are isolated.

```python
@render.plot
@reactive.event(input.go)      # decorator order: event goes BELOW the reactive
def results():                 # or render decorator, closer to the function
    return plot_model(input.x(), input.y())
```

- Place it **below** `@reactive.calc` / `@reactive.effect` / `@render.*` —
  it must wrap the plain function, not the reactive object (runtime
  `TypeError` otherwise).
- `ignore_none=True` (default) skips the `None`/`0` initial value of action
  buttons, so the function does not run at startup; `ignore_init=True` skips
  the initial run entirely.
- The classic use: expensive results users only sometimes want —
  `ui.input_action_button("go", "Compute")` + `@reactive.event(input.go)`,
  with the real inputs read (but not depended on) in the body.

Anti-pattern to remove when you see it — computing expensive results in a
`@reactive.effect` and storing them in a `reactive.value` so outputs can read
them:

```python
# Wrong: eager, computes whether or not anyone consumes it, and the value
# is stale the moment an input changes before the next go click
@reactive.effect
@reactive.event(input.go)
def _():
    results_val.set(expensive(input.x()))
```

Use the `@render.*` + `@reactive.event` form (or a `@reactive.calc` + event)
instead: it's lazy — nothing computes until an output actually reads it.

## Breaking update-fires-update loops

When an effect updates an input that downstream reactives read
(`ui.update_select("city", ...)` when `country` changes), downstream outputs
recompute with the *intermediate* state: new country, old city. Two options:

- **Gate the consumers too**: give the expensive output its own
  `@reactive.event` on the parent input so it re-runs once per actual change.
- **Freeze the input** (escape hatch, verified against Shiny 1.8):
  `input.city.freeze()` unsets the input's value without invalidating
  anyone; downstream reads raise the silent exception until the browser
  echoes the updated value back, so they recompute once with fully
  consistent inputs:
  ```python
  @reactive.effect
  def _():
      country = input.country()
      input.city.freeze()                        # readers stay quiet
      ui.update_select("city", choices=cities[country])
  ```
  Caveat: reads stay blocked until the client sends a new value for that
  input — if the update doesn't actually change the value, consumers may
  stay blank. This is the Python analogue of R's `freezeReactiveValue()`;
  it is an escape hatch, not a default.

## Rate-limit chatty inputs: debounce

Shiny for Python already debounces slider and text-input updates on the
client — those input bindings carry a built-in 250 ms rate policy — so an
ordinary drag or typing burst usually arrives as a single invalidation.
Bursts still happen: a slow drag or a long edit can outlast the client
window, and they're guaranteed to pile up when each change's downstream
computation takes longer than the gaps between changes. High-frequency
client events (continuous brush/hover streams from Plotly-style widgets)
are the clear-cut case. When you need explicit server-side rate limiting,
Shiny for Python has **no built-in debounce/throttle** (as of Shiny 1.8 — the
feature is tracked in py-shiny issues #564 and #1814). Options, best first:

1. **Gate on a button** — `@reactive.event(input.go)` (above). Simplest and
   most predictable.
2. **Debounce helper** — a small, tested pattern adapted from Joe Cheng's
   `ratelimit.py` gist. Declare it in session scope (inside `server()`, or
   at Express top level), wrap a *cheap* reactive read, and have expensive
   consumers read the debounced value:
   ```python
   import functools
   import time
   from shiny import reactive

   def debounce(fn, *, delay_secs=0.5):
       """Debounce a reactive read: downstream recomputes only after
       delay_secs of quiet time. Adapted from jcheng5/ratelimit.py."""
       when = reactive.value(None)     # deadline for committing
       trigger = reactive.value(0)

       @reactive.calc
       def cached():
           return fn()

       @reactive.effect(priority=102)
       def primer():                    # restart the clock on every change
           try:
               cached()
           except Exception:
               pass
           finally:
               when.set(time.time() + delay_secs)

       @reactive.effect(priority=101)
       def timer():
           deadline = when()
           if deadline is None:
               return
           remaining = deadline - time.time()
           if remaining <= 0:
               with reactive.isolate():
                   when.set(None)
                   trigger.set(trigger() + 1)
           else:
               reactive.invalidate_later(remaining)

       @reactive.calc
       @reactive.event(trigger, ignore_none=False)
       @functools.wraps(fn)
       def debounced():
           return cached()

       return debounced

   debounced_search = debounce(lambda: input.search(), delay_secs=0.5)

   @render.data_frame
   def results():        # re-runs once, ~0.5s after typing stops
       return search_big_index(debounced_search())
   ```
   Semantics that matter: debounce rate-limits the **invalidation signal**,
   not execution — wrap only a cheap read (a direct input read) when the
   *downstream* work is expensive. Timings are **minimums**: reactive code
   runs serially, so a slow downstream computation can exceed the window.
   Rely on the built-in client-side debouncing for ordinary sliders and text
   inputs; add the helper only when profiling shows an invalidation storm.

Source: <https://gist.github.com/jcheng5/427de09573816c4ce3a8c6ec1839e7c0>.

### When smoothing isn't enough: gate behind a button

Rate-limiting loses once changes compound — cascading `ui.update_*()` chains,
a long batch of settings, or downstream compute that outlasts every window.
Then stop smoothing the stream and make the expensive update wait for a
deliberate trigger:

- Gate the heavy work with `@reactive.event(input.go)` and use
  **`ui.input_task_button()`** in place of `ui.input_action_button()`: same
  click semantics, a **direct drop-in with no server-side changes and no
  `@reactive.extended_task` required**. On click it disables itself and shows
  a busy label until the server finishes dealing with the triggered
  reactivity, then reverts on its own — exactly the feedback a long or
  compounding update cycle needs (the shorter the cycle, the less it has
  to show). Users batch their input changes, click once, and the expensive
  update runs once.

## Timers

- **`reactive.invalidate_later()` at the *start* of a slow reactive is an
  infinite busy-loop**: the timer is scheduled immediately and re-fires the
  moment the reactive finishes. Schedule it at the **end** of the body (or in
  a `finally:`) so the delay starts after completion:
  ```python
  @reactive.effect
  def _():
      try:
          slow_step()
          another_step()
      finally:
          reactive.invalidate_later(0.5)
  ```
- **Polling external data on a timer invalidates all consumers on every tick,
  even when nothing changed.** `@reactive.poll()` runs the expensive body only
  when a *cheap* check value changes:
  ```python
  @reactive.poll(lambda: db_max_updated_at(), interval_secs=10)
  def live_data():
      return read_sales()          # runs only when max(updated_at) changes
  ```
  Keep the check function genuinely cheap — it runs every interval.
  `@reactive.file_reader(path)` is the file-mtime special case.
- In Express, declare `@reactive.poll`/`@reactive.file_reader` in an
  **imported module** (not `app.py` top level) so one poll and one cached
  result are shared across all sessions.

## Granularity: splitting state limits the blast radius

- Prefer `@reactive.calc` for derived values — memoized, lazy, read-only.
- Split monolithic state into several `reactive.value`s so each invalidates
  independently — one value written from many effects is a common storm
  source.
- `reactive.value.set()` compares by **identity** (`is`), not equality:
  setting the *same object* is a no-op, and setting an equal-but-new object
  invalidates. This is why **in-place mutation never triggers downstream
  updates** — `df.loc[0, "x"] = 1; val.set(df)` notifies no one, because the
  object is identical. Always build a new object:
  `val.set(val() + [item])`, `val.set({**val(), k: v})`, or `val.set(df.copy())`.
- Effects that write reactive values they also (transitively) read are where
  most loops originate. Prefer calc-derived data over "effect computes and
  stores into a reactive.value".

## Conditional and accidental dependencies

Two subtle shapes to check (traces from the OpenTelemetry reactivity level,
diagnosis.md, show the real graph):

1. **Conditional reads**: `if input.by_bracket(): input.bracket() else ...`
   depends on `input.bracket()` *only in flushes where the switch is on*. If
   an expensive consumer shouldn't re-run when a cosmetic input changes, move
   that read out of the shared path or isolate it.
2. **Accidental dependencies** via helper functions that read inputs deep in
   a call stack. The trace shows actual dependencies — trust it over your
   mental model.

## Further reading

- Reactive patterns:
  <https://shiny.posit.co/py/docs/reactive-patterns.html>
- `reactive.event`:
  <https://shiny.posit.co/py/api/core/reactive.event.html>
- `reactive.poll`:
  <https://shiny.posit.co/py/api/core/reactive.poll.html>
- Debounce/throttle feature request:
  <https://github.com/posit-dev/py-shiny/issues/564>
