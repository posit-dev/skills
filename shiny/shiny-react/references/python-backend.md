# Python Backend Reference

Complete guide for building shiny-react apps with Python Shiny backends.

## Table of Contents

- [Setup](#setup)
- [shinyreact.py Functions](#shinyreactpy-functions)
- [Rendering Patterns](#rendering-patterns)
- [Message Handling](#message-handling)
- [Complete Example](#complete-example)

## Setup

### File Structure

```
myapp/
├── py/
│   ├── app.py           # Main Shiny application
│   ├── shinyreact.py    # Utility functions (copy from template)
│   └── www/             # Built JS/CSS from esbuild
│       ├── main.js
│       └── main.css
```

### Minimal app.py

```python
from shiny import App, Inputs, Outputs, Session
from shinyreact import page_react, render_json
from pathlib import Path

def server(input: Inputs, output: Outputs, session: Session):
    # Your server logic here
    pass

app = App(
    page_react(title="My App"),
    server,
    static_assets=str(Path(__file__).parent / "www"),
)
```

**Note:** The `static_assets` parameter is required to serve the built JS/CSS files.

## shinyreact.py Functions

### page_react()

Creates the HTML page shell for React apps.

```python
def page_react(
    *args,                    # Additional UI elements
    title: str | None = None, # Page title
    js_file: str | None = "main.js",   # JavaScript bundle
    css_file: str | None = "main.css", # CSS file
    lang: str = "en"          # HTML lang attribute
) -> ui.Tag
```

**Example:**
```python
ui = page_react(
    title="My Dashboard",
    js_file="main.js",
    css_file="main.css"
)
```

### @render_json

Decorator for rendering arbitrary Python objects as JSON.

```python
class render_json(Renderer[Jsonifiable]):
    """Render any JSON-serializable data to React."""
```

**Examples:**

```python
# Simple values
@render_json
def greeting():
    return f"Hello, {input.name()}"

# Dictionaries become JSON objects
@render_json
def stats():
    return {
        "mean": float(df["mpg"].mean()),
        "std": float(df["mpg"].std()),
        "count": len(df)
    }

# DataFrames - convert to column-major format
@render_json
def table_data():
    return df.head(input.num_rows()).to_dict(orient="list")

# Lists become JSON arrays
@render_json
def items():
    return ["apple", "banana", "cherry"]
```

**Important:** For pandas DataFrames, use `.to_dict(orient="list")` to get column-major format matching React expectations.

### post_message()

Send custom messages from server to React (async function).

```python
async def post_message(
    session: Session,
    type: str,        # Message type (matches useShinyMessageHandler)
    data: JsonifiableIn  # Any JSON-serializable data
)
```

**Examples:**

```python
# Toast notification
await post_message(session, "toast", {
    "text": "File saved successfully",
    "type": "success"
})

# Progress update
await post_message(session, "progress", {
    "percent": 75,
    "message": "Processing..."
})
```

## Rendering Patterns

### Reactive Data with Shiny Core

```python
from shiny import App, Inputs, Outputs, Session, reactive
from shinyreact import page_react, render_json
import pandas as pd

mtcars = pd.read_csv("mtcars.csv")

def server(input: Inputs, output: Outputs, session: Session):
    @reactive.calc
    def filtered_data():
        df = mtcars.copy()
        df = df[df["cyl"] >= input.min_cyl()]
        df = df[df["mpg"] >= input.min_mpg()]
        return df

    @render_json
    def table():
        return filtered_data().to_dict(orient="list")

    @render_json
    def summary():
        df = filtered_data()
        return {
            "count": len(df),
            "avg_mpg": round(df["mpg"].mean(), 1),
            "avg_hp": round(df["hp"].mean(), 0)
        }

app = App(page_react(title="Data Explorer"), server)
```

### Multiple Related Outputs

```python
@render_json
def chart_data():
    return {
        "x": mtcars["wt"].tolist(),
        "y": mtcars["mpg"].tolist(),
        "labels": mtcars.index.tolist()
    }

@render_json
def chart_options():
    return {
        "title": input.chart_title(),
        "showLegend": input.show_legend(),
        "colorScheme": input.color_scheme()
    }
```

### Plots with @render.plot

```python
from shiny import render
import matplotlib.pyplot as plt

@render.plot
def myplot():
    fig, ax = plt.subplots()
    ax.scatter(mtcars["wt"], mtcars["mpg"])
    ax.set_xlabel("Weight")
    ax.set_ylabel("MPG")
    return fig
```

## Message Handling

### Reactive Effects with Messages

```python
from shiny import reactive

@reactive.effect
@reactive.event(input.submit)
async def handle_submit():
    # Long computation
    result = expensive_calculation()

    await post_message(session, "complete", {
        "success": True,
        "message": "Calculation finished",
        "result": result
    })
```

### Periodic Updates

```python
from shiny import reactive
import asyncio

@reactive.effect
async def heartbeat():
    while True:
        await asyncio.sleep(5)  # Every 5 seconds
        await post_message(session, "heartbeat", {
            "time": datetime.now().isoformat(),
            "status": "connected"
        })
        reactive.invalidate_later(5)
```

### Streaming Data

```python
@reactive.effect
@reactive.event(input.start_stream)
async def stream_data():
    for i in range(100):
        await post_message(session, "stream", {
            "progress": i + 1,
            "data": generate_chunk(i)
        })
        await asyncio.sleep(0.1)

    await post_message(session, "stream", {
        "progress": 100,
        "done": True
    })
```

## Complete Example

### app.py

```python
from shiny import App, Inputs, Outputs, Session, reactive, render
from shinyreact import page_react, render_json, post_message
from pathlib import Path
import pandas as pd

# Load data
mtcars = pd.read_csv("mtcars.csv")

def server(input: Inputs, output: Outputs, session: Session):
    @reactive.calc
    def filtered():
        df = mtcars.copy()
        cylinders = input.cylinders()
        if cylinders:
            df = df[df["cyl"].isin(cylinders)]
        df = df[df["mpg"] >= input.min_mpg()]
        return df

    @render_json
    def car_data():
        return filtered().to_dict(orient="list")

    @render_json
    def summary():
        df = filtered()
        return {
            "total": len(df),
            "avg_mpg": round(df["mpg"].mean(), 1) if len(df) > 0 else 0,
            "avg_hp": round(df["hp"].mean(), 0) if len(df) > 0 else 0
        }

    @render.plot
    def scatter():
        import matplotlib.pyplot as plt
        df = filtered()
        fig, ax = plt.subplots()
        for cyl in df["cyl"].unique():
            subset = df[df["cyl"] == cyl]
            ax.scatter(subset["wt"], subset["mpg"], label=f"{cyl} cyl")
        ax.set_xlabel("Weight")
        ax.set_ylabel("MPG")
        ax.legend()
        return fig

    @reactive.effect
    async def warn_on_few_results():
        if len(filtered()) < 5:
            await post_message(session, "warning", {
                "text": "Very few cars match your filters"
            })

app = App(
    page_react(title="Car Explorer"),
    server,
    static_assets=str(Path(__file__).parent / "www"),
)
```

## Running the App

### Development

```bash
cd py
shiny run app.py --reload --port 8000
```

### With npm scripts (recommended)

```json
{
  "scripts": {
    "shinyapp-py": "cd py && shiny run app.py --reload --port ${PY_PORT:-8001}"
  }
}
```

```bash
npm run shinyapp-py
# or
PY_PORT=8002 npm run shinyapp-py
```

## Type Hints

The `shinyreact.py` module includes proper type hints:

```python
from typing import Mapping, Sequence, Union

JsonifiableIn = Union[
    str, int, float, bool, None,
    Sequence["JsonifiableIn"],
    Mapping[str, "JsonifiableIn"]
]
```

Use these types for better IDE support when working with message data.

## Python-Specific Gotchas

### Object Identity vs Equality

Python Shiny uses **object identity** (not equality) to determine if a reactive value changed. Mutating an object in place won't trigger updates:

```python
# WRONG - same object identity, no reactivity triggered
@reactive.effect
def update_list():
    current = items.get()
    current.append(new_item)  # Mutates in place
    items.set(current)  # Same object - no update!

# CORRECT - create new object with new identity
@reactive.effect
def update_list():
    current = items.get()
    new_list = current[:]  # Copy creates new identity
    new_list.append(new_item)
    items.set(new_list)  # New object - triggers update
```

For dicts, use `dict(current)` or `{**current, "key": value}`. For lists, use `list(current)` or `current[:]`.

### Preventing Dependency Loops

Use `@reactive.event` to explicitly declare triggers, or `reactive.isolate()` to read values without creating dependencies:

```python
# Only runs when submit button clicked, not when count changes
@reactive.effect
@reactive.event(input.submit)
def handle_submit():
    # Read count without creating dependency
    with reactive.isolate():
        current_count = count.get()
    # Process...
```
