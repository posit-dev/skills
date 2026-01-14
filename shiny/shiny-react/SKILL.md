---
name: shiny-react
description: >
  Build Shiny applications with React frontends using the @posit/shiny-react library.
  Use when: (1) Creating new Shiny apps with React UI, (2) Adding React components to
  existing Shiny apps, (3) Creating reusable React widgets using custom web elements,
  (4) Using shadcn/ui or other React component libraries with Shiny, (5) Understanding
  useShinyInput/useShinyOutput hooks, (6) Setting up bidirectional communication between
  React and R/Python Shiny backends, (7) Building modern data dashboards with React and
  Shiny, (8) Implementing dynamic widget rendering with insertUI/removeUI. Supports both
  R and Python Shiny backends.
---

# shiny-react

Build Shiny applications with React frontends. The `@posit/shiny-react` library provides React hooks for bidirectional communication between React components and Shiny servers (R or Python).

## Quick Start

Create a new app:

```bash
npx create-shiny-react-app myapp
cd myapp
npm install
npm run dev  # Builds frontend and starts Shiny app on port 8000
```

## Core Concepts

### Data Flow

Communication is bidirectional:
- **React → Shiny**: Use `useShinyInput` to send values to the server (appears as `input$id` in R or `input.id()` in Python)
- **Shiny → React**: Use `useShinyOutput` to receive reactive values from server outputs (`output$id`)

```
React Component ──[useShinyInput]──> Shiny Server (R/Python)
                                           │
                                     Process Data
                                           │
React Component <──[useShinyOutput]── Shiny Server
```

### TypeScript Hooks

```typescript
import { useShinyInput, useShinyOutput } from "@posit/shiny-react";

function MyComponent() {
  // Send data TO Shiny (like input$my_input in R)
  const [value, setValue] = useShinyInput<string>("my_input", "default");

  // Receive data FROM Shiny (from output$my_output)
  const [result, recalculating] = useShinyOutput<string>("my_output", undefined);

  return (
    <div>
      <input value={value} onChange={(e) => setValue(e.target.value)} />
      <div>{recalculating ? "Loading..." : result}</div>
    </div>
  );
}
```

### Backend (R)

```r
library(shiny)
source("shinyreact.R", local = TRUE)

server <- function(input, output, session) {
  output$my_output <- render_json({
    toupper(input$my_input)
  })
}

shinyApp(ui = page_react(title = "My App"), server = server)
```

### Backend (Python)

```python
from shiny import App, Inputs, Outputs, Session
from shinyreact import page_react, render_json

def server(input: Inputs, output: Outputs, session: Session):
    @render_json
    def my_output():
        return input.my_input().upper()

app = App(page_react(title="My App"), server)
```

## Writing React Components for Shiny

When writing React components that communicate with Shiny:

1. **Use `useShinyInput` for any value that needs to reach the server** - This replaces direct state when the server needs to react to changes.

2. **Use `useShinyOutput` for any data coming from the server** - Always handle the `undefined` initial state and the `recalculating` boolean for loading states.

3. **Match IDs exactly** - The string ID in `useShinyInput("foo", ...)` must match `input$foo` (R) or `input.foo()` (Python) exactly.

4. **Choose appropriate debounce values**:
   - Text inputs: 100-300ms (default is 100ms)
   - Sliders/continuous: 50-100ms
   - Buttons: Use `priority: "event"` with no debounce
   - Expensive server operations: 500ms+

5. **Button clicks need event priority** to ensure each click triggers the server:
   ```typescript
   const [clicks, setClicks] = useShinyInput<number>("btn", 0, { priority: "event" });
   <button onClick={() => setClicks(clicks + 1)}>Click</button>
   ```

6. **Handle loading states** - The second return value from `useShinyOutput` indicates recalculation:
   ```typescript
   const [data, isLoading] = useShinyOutput<Data>("result", undefined);
   if (isLoading) return <Spinner />;
   ```

7. **Use namespaces for multiple widget instances** - When embedding multiple instances of the same React widget, wrap them in `ShinyModuleProvider` to prevent ID conflicts:
   ```typescript
   import { ShinyModuleProvider } from "@posit/shiny-react";

   <ShinyModuleProvider namespace="widget1">
     <MyWidget />
   </ShinyModuleProvider>
   ```

8. **Create reusable widgets with custom web elements** - For self-contained React widgets that can be embedded in Shiny apps, use custom web elements. See the "Custom Web Element Pattern" section below for the recommended approach.

## Shiny Module Namespaces

When to use namespaces:

- **Multiple widget instances** - Same React component used multiple times on one page
- **Shiny module integration** - React widgets inside Shiny modules (`moduleServer` in R, `@module.server` in Python)
- **Reusable components** - Creating widget libraries that work like standard Shiny UI components

### Client-Side Pattern

```typescript
import { ShinyModuleProvider } from "@posit/shiny-react";

// Wrap the widget in ShinyModuleProvider
<ShinyModuleProvider namespace={namespace}>
  <CounterWidget />
</ShinyModuleProvider>

// All hooks inside automatically namespace their IDs
function CounterWidget() {
  const [count, setCount] = useShinyInput<number>("count", 0);
  // If namespace="counter1", this becomes "counter1-count"
}
```

### Server-Side Pattern

Use standard Shiny module patterns. The `post_message()` function automatically namespaces messages:

**R:**
```r
counter_ui <- function(id, title = "Counter") {
  card(
    card_header(title),
    tags$tag("counter-widget", list(`data-namespace` = id))
  )
}

counter_server <- function(id) {
  moduleServer(id, function(input, output, session) {
    # input$count is automatically namespaced by Shiny
    output$serverCount <- render_json({ input$count * 2 })

    # post_message automatically applies session$ns()
    post_message(session, "notification", list(text = "Updated!"))

    # Return reactive for use elsewhere
    reactive({ input$count })
  })
}
```

**Python:**
```python
def counter_ui(id: str, title: str = "Counter"):
    return ui.card(
        ui.card_header(title),
        ui.HTML(f'<counter-widget data-namespace="{id}"></counter-widget>')
    )

@module.server
def counter_server(input, output, session):
    @render_json
    def serverCount():
        return input.count() * 2

    # post_message automatically applies resolve_id()
    await post_message(session, "notification", {"text": "Updated!"})

    @reactive.calc
    def count():
        return input.count() if input.count() is not None else 0

    return count  # Return reactive for use elsewhere
```

### Custom Web Element Pattern (Recommended)

For self-contained React widgets embedded in standard Shiny apps, **use custom web elements** that handle their own lifecycle:

```typescript
// main.tsx - define a custom web element
class CounterWidgetElement extends HTMLElement {
  private root: Root | null = null;

  connectedCallback() {
    // Read attributes using dataset and pass them as props to React component
    const namespace = this.id;
    const title = this.dataset.title || "Counter";
    const initialValue = parseInt(this.dataset.initialValue || "0");

    this.root = createRoot(this);
    this.root.render(
      <StrictMode>
        <ShinyModuleProvider namespace={namespace}>
          <CounterWidget title={title} initialValue={initialValue} />
        </ShinyModuleProvider>
      </StrictMode>
    );
  }

  disconnectedCallback() {
    // Clean up React root when element is removed
    if (this.root) {
      this.root.unmount();
      this.root = null;
    }
  }
}

// Register the custom element
customElements.define("counter-widget", CounterWidgetElement);
```

**Benefits of custom web elements:**
- **Pass configuration via HTML attributes**: Read attributes in `connectedCallback()` and pass them as props to your React component
- **Automatic initialization**: React initializes when element is added to DOM
- **Automatic cleanup**: React unmounts when element is removed from DOM
- **Dynamic rendering support**: Works seamlessly with `insertUI()`/`removeUI()` (R) or `ui.insert_ui()`/`ui.remove_ui()` (Python)
- **Semantic HTML**: `<counter-widget>` is more readable than `<div data-widget>`
- **Self-contained**: All initialization logic lives in one place
- **No event listener dependencies**: No need to wait for `DOMContentLoaded`

**Using the widget in Shiny:**

R:
```r
counter_ui <- function(id, title = "Counter", initial_value = 0) {
  card(
    card_header(title),
    tag("counter-widget", list(
      id = id,
      `data-title` = title,
      `data-initial-value` = initial_value
    ))
  )
}
```

Python:
```python
def counter_ui(id: str, title: str = "Counter", initial_value: int = 0):
    return ui.card(
        ui.card_header(title),
        ui.HTML(f'<counter-widget id="{id}" data-title="{title}" data-initial-value="{initial_value}"></counter-widget>')
    )
```

**Key Pattern:** Use `data-*` attributes to pass configuration from Shiny to React. Write the custom element to read these via `this.dataset` in `connectedCallback()` and pass them as props to your React component.

This pattern allows React widgets to be used like native Shiny components, with clean APIs that follow Shiny conventions. The custom element automatically handles React lifecycle, making widgets work correctly even when dynamically added or removed.

See `examples/8-modules/app-standard.R` and `app-standard.py` in the shiny-react repository for a complete working example with dynamic widget rendering.

## Decision Tree

1. **New app from scratch?** → Use `npx create-shiny-react-app`
2. **Creating reusable React widgets for Shiny?** → Use custom web elements (see "Custom Web Element Pattern" above)
3. **Need multiple instances of same widget?** → Use `ShinyModuleProvider` with namespacing (see "Shiny Module Namespaces" above)
4. **Need TypeScript API details?** → Read `references/typescript-api.md`
5. **Setting up R backend?** → Read `references/r-backend.md`
6. **Setting up Python backend?** → Read `references/python-backend.md`
7. **Using shadcn/ui or Tailwind?** → Read `references/shadcn-setup.md`
8. **Understanding internals?** → Read `references/internals.md`

## Project Structure

Standard shiny-react project layout:

```
myapp/
├── package.json          # npm dependencies and scripts
├── tsconfig.json         # TypeScript configuration
├── srcts/                # React TypeScript source
│   ├── main.tsx          # Entry point (renders to #root)
│   ├── App.tsx           # Main React component
│   └── styles.css        # CSS styles
├── r/                    # R Shiny backend
│   ├── app.R             # Shiny app
│   ├── shinyreact.R      # Utility functions (page_react, render_json)
│   └── www/              # Built JS/CSS (auto-generated)
└── py/                   # Python Shiny backend
    ├── app.py            # Shiny app
    ├── shinyreact.py     # Utility functions
    └── www/              # Built JS/CSS (auto-generated)
```

## Essential Patterns

### Input with Debouncing

```typescript
const [value, setValue] = useShinyInput<string>("search", "", {
  debounceMs: 300,  // Wait 300ms after typing stops (default: 100)
});
```

### Typed Outputs

```typescript
interface Stats { mean: number; median: number; max: number; }
const [stats, loading] = useShinyOutput<Stats>("statistics", undefined);
```

### Server-to-Client Messages

React:
```typescript
useShinyMessageHandler("notification", (msg: { text: string }) => {
  showToast(msg.text);
});
```

R:
```r
post_message(session, "notification", list(text = "Data updated!"))
```

Python:
```python
await post_message(session, "notification", {"text": "Data updated!"})
```

### Plot/Image Output

```typescript
import { ImageOutput } from "@posit/shiny-react";

<ImageOutput id="myplot" width="100%" height="400px" />
```

R backend uses standard `renderPlot()` - the ImageOutput automatically handles sizing.

### Data Frames (Column-Major JSON)

Data frames serialize as column arrays:
```json
{"mpg": [21, 21, 22.8], "cyl": [6, 6, 4], "disp": [160, 160, 108]}
```

R:
```r
output$table_data <- render_json({ mtcars[1:10, ] })
```

TypeScript:
```typescript
const [data] = useShinyOutput<Record<string, number[]>>("table_data", undefined);
```

## Build System

Uses esbuild for fast bundling. Key scripts in package.json:

```json
{
  "scripts": {
    "dev": "concurrently \"npm run watch\" \"npm run shinyapp\"",
    "build": "esbuild srcts/main.tsx --bundle --minify --outfile=r/www/main.js",
    "watch": "esbuild srcts/main.tsx --bundle --outfile=r/www/main.js --watch"
  }
}
```

Entry point (`srcts/main.tsx`):
```typescript
import { createRoot } from "react-dom/client";
import App from "./App";
import "./styles.css";

const container = document.getElementById("root");
if (container) {
  createRoot(container).render(<App />);
}
```

## Examples & Utilities

### Official Examples

The [shiny-react repository](https://github.com/wch/shiny-react) includes example apps in `examples/`:

| Example | Description |
|---------|-------------|
| `1-hello-world` | Basic bidirectional communication |
| `2-inputs` | Various input types (text, number, checkbox, slider, etc.) |
| `3-outputs` | JSON data and plot outputs |
| `4-messages` | Server-to-client messages with toast notifications |
| `5-shadcn` | Modern UI with shadcn/ui and Tailwind CSS |
| `6-dashboard` | Full analytics dashboard with charts and tables |
| `7-chat` | AI chat app with streaming responses |
| `8-modules` | Shiny module namespaces with multiple widget instances (see two variants: full React app and standard Shiny app) |

Each example includes complete R and Python backends.

### Utility Files (shinyreact.R / shinyreact.py)

Each shiny-react app requires utility files that provide `page_react()`, `render_json()`, and `post_message()`. These are **not installed as packages** - copy them, or just the functions that you need, into your project or package.

**Ready-to-use utility files are included in this skill:**
- `assets/shinyreact.R` - For R apps or packages
- `assets/shinyreact.py` - For Python apps or packages

The utilities are documented in `references/r-backend.md` and `references/python-backend.md`.

## Common Issues

**Hooks not working**: Ensure `page_react()` is used in the UI - it includes the `<div id="root">` element.

**Values not updating**: Check that input/output IDs match exactly between React and R/Python.

**TypeScript errors**: Install types: `npm install -D @types/react @types/react-dom`

**Build output location**: esbuild outputs to `r/www/` or `py/www/` - ensure paths match in package.json scripts.

**Python: Mutable objects not triggering updates**: Python Shiny uses object identity (not equality) for reactivity. Copy mutable objects before modifying:
```python
# Wrong - same object identity, no update triggered
items.append(new_item)
reactive_value.set(items)

# Correct - new object identity triggers update
new_items = items[:]  # or list(items)
new_items.append(new_item)
reactive_value.set(new_items)
```

## Anti-Patterns to Avoid

- **Don't mix `useState` and `useShinyInput` for the same value** - Use `useShinyInput` if the server needs the value, `useState` for local-only UI state.
- **Don't create circular dependencies** - Avoid patterns where an output triggers an input that triggers the same output.
- **Don't forget loading states** - Always handle `recalculating` from `useShinyOutput` to show users when data is stale.
- **Don't use `useShinyInput` for high-frequency updates without debouncing** - Mouse movements, scroll positions, etc. should have high debounce values or be kept local.
