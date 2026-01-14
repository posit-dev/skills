# TypeScript API Reference

Complete API reference for `@posit/shiny-react` hooks and components.

## Table of Contents

- [useShinyInput](#useshinyinput)
- [useShinyOutput](#useshinyoutput)
- [useShinyMessageHandler](#useshinymessagehandler)
- [useShinyInitialized](#useshinyinitialized)
- [ImageOutput Component](#imageoutput-component)
- [ShinyReactComponentElement](#shinyreactcomponentelement)

## useShinyInput

Send data from React to Shiny server.

```typescript
function useShinyInput<T>(
  id: string,
  defaultValue: T,
  options?: {
    debounceMs?: number;   // Debounce delay (default: 100ms)
    priority?: EventPriority;  // "deferred" | "event" | "immediate"
  }
): [T, (value: T) => void]
```

### Parameters

- `id`: Shiny input ID (accessed as `input$id` in R or `input.id()` in Python)
- `defaultValue`: Initial value before any user interaction
- `options.debounceMs`: Milliseconds to wait after value changes before sending to server
- `options.priority`: Event priority for Shiny's reactive system

### Returns

Tuple of `[currentValue, setValue]` similar to React's useState.

### Examples

```typescript
// Basic text input
const [text, setText] = useShinyInput<string>("user_text", "");

// Number with longer debounce
const [count, setCount] = useShinyInput<number>("counter", 0, { debounceMs: 500 });

// Button clicks with immediate priority
const [clicks, setClicks] = useShinyInput<number>("button_clicks", 0, {
  priority: "event"
});
```

### Behavior Notes

- Value is sent to Shiny via `window.Shiny.setInputValue()` after debounce
- Multiple components can share the same input ID - they'll stay synchronized
- The hook preserves values across component remounts

## useShinyOutput

Receive reactive data from Shiny server outputs.

```typescript
function useShinyOutput<T>(
  outputId: string,
  defaultValue?: T
): [T | undefined, boolean]
```

### Parameters

- `outputId`: Shiny output ID (set via `output$id` in R or `@output` in Python)
- `defaultValue`: Value to use before first server update

### Returns

Tuple of `[value, recalculating]`:
- `value`: Current output value from server
- `recalculating`: `true` while server is computing new value

### Examples

```typescript
// Simple string output
const [message, loading] = useShinyOutput<string>("status_message", "");

// Complex typed output
interface ChartData {
  labels: string[];
  values: number[];
}
const [chartData, isLoading] = useShinyOutput<ChartData>("chart_data", undefined);

// Show loading state
{isLoading ? <Spinner /> : <Chart data={chartData} />}
```

### Data Format Patterns

**Strings and numbers**: Pass through directly

**Data frames** (R/Python): Serialize as column-major JSON objects
```typescript
// R: output$df <- render_json({ mtcars })
type DataFrame = Record<string, (string | number | boolean | null)[]>;
const [df] = useShinyOutput<DataFrame>("df", undefined);

// Access: df?.mpg[0], df?.cyl[1], etc.
```

**Lists/Dicts**: Serialize as JSON objects
```typescript
interface Stats { mean: number; sd: number; n: number; }
const [stats] = useShinyOutput<Stats>("statistics", undefined);
```

**Arrays**: Serialize as JSON arrays
```typescript
const [items] = useShinyOutput<string[]>("item_list", []);
```

## useShinyMessageHandler

Handle custom messages sent from Shiny server via `post_message()`.

```typescript
function useShinyMessageHandler<T>(
  messageType: string,
  handler: (data: T) => void
): void
```

### Parameters

- `messageType`: Message type identifier (must match `type` in `post_message()`)
- `handler`: Callback function invoked when message is received

### Examples

```typescript
// Toast notifications
useShinyMessageHandler("toast", (msg: { text: string; type: string }) => {
  showToast(msg.text, msg.type);
});

// Progress updates
useShinyMessageHandler("progress", (data: { percent: number }) => {
  setProgress(data.percent);
});

// Streaming data (e.g., LLM responses)
useShinyMessageHandler("stream_chunk", (chunk: { text: string; done: boolean }) => {
  if (chunk.done) {
    setStreaming(false);
  } else {
    appendToResponse(chunk.text);
  }
});
```

### Behavior Notes

- Handler is automatically cleaned up when component unmounts
- Re-registering with same messageType replaces the previous handler
- Handler should be wrapped in `useCallback` if it has dependencies

## useShinyInitialized

Check if Shiny has finished initializing.

```typescript
function useShinyInitialized(): boolean
```

### Returns

`true` once `window.Shiny.initializedPromise` resolves.

### Use Cases

```typescript
const shinyReady = useShinyInitialized();

if (!shinyReady) {
  return <div>Connecting to server...</div>;
}

return <MainApp />;
```

## ImageOutput Component

Display Shiny plot/image outputs with automatic sizing.

```typescript
function ImageOutput(props: {
  id: string;           // Shiny output ID (from renderPlot/renderImage)
  className?: string;   // CSS class for the <img> element
  width?: string;       // CSS width (e.g., "100%", "300px")
  height?: string;      // CSS height (e.g., "400px", "50vh")
  debounceMs?: number;  // Resize debounce (default: 400ms)
  onRecalculating?: (isRecalculating: boolean) => void;
}): JSX.Element
```

### Key Features

- Automatically sends dimensions to Shiny for server-side plot generation
- Uses ResizeObserver to update dimensions on resize
- Handles Shiny's recalculating state

### Examples

```typescript
// Fixed height, responsive width
<ImageOutput id="myplot" width="100%" height="400px" />

// Full viewport height
<ImageOutput id="fullplot" width="100%" height="100vh" />

// With loading callback
<ImageOutput
  id="chart"
  width="100%"
  height="300px"
  onRecalculating={(loading) => setIsLoading(loading)}
/>
```

### CSS-Controlled Sizing

```typescript
// Use CSS class for sizing
<ImageOutput id="plot" className="dashboard-plot" />
```

```css
.dashboard-plot {
  width: 100%;
  height: 100%;
  min-height: 300px;
}
```

### Backend (R)

```r
output$myplot <- renderPlot({
  # Plot code - dimensions come from ImageOutput automatically
  ggplot(data, aes(x, y)) + geom_point()
})
```

### Backend (Python)

```python
@render.plot
def myplot():
    fig, ax = plt.subplots()
    ax.scatter(data['x'], data['y'])
    return fig
```

## ShinyReactComponentElement

Base class for creating custom web elements that render React components with automatic Shiny integration.

```typescript
class ShinyReactComponentElement extends HTMLElement {
  // Set on subclass to define the React component to render
  static component: React.ComponentType<Record<string, unknown>> | null;

  // Protected properties
  protected root: Root | null;
  protected slotContents: Map<string, Node[]>;

  // Protected methods
  protected getConfig(): Record<string, unknown>;
  protected captureSlots(selector?: string): Map<string, Node[]>;
  protected mountSlot(slotName: string, container: HTMLElement | null): Promise<void>;
  protected get onSlotMount(): (slotName: string, el: HTMLElement | null) => Promise<void>;
  protected get namespace(): string | undefined;
  protected render(): React.ReactNode;
  protected clearContent(): void;

  // Lifecycle
  connectedCallback(): void;
  disconnectedCallback(): void;
}
```

### Features

- **Automatic namespace support**: Wraps in `ShinyModuleProvider` if element has an `id`
- **Config parsing**: `getConfig()` parses `data-*` attributes with JSON auto-parsing
- **Slot preservation**: Captures `[data-slot]` children for blended React+Shiny content
- **Default slot**: If no `data-slot` elements, all children go to `__children__` slot
- **Shiny lifecycle**: Automatic `bindAll`/`unbindAll` management

### Simple Widget Example

```typescript
import { ShinyReactComponentElement } from "@posit/shiny-react";
import { MyWidget } from "./MyWidget";

class MyWidgetElement extends ShinyReactComponentElement {
  static component = MyWidget;
}

if (!customElements.get("my-widget")) {
  customElements.define("my-widget", MyWidgetElement);
}
```

The component receives parsed `data-*` attributes as props automatically.

### Blended Component Example

For React layouts containing Shiny content:

```typescript
class MySidebarElement extends ShinyReactComponentElement {
  protected render() {
    const config = this.getConfig();
    return (
      <SidebarLayout
        {...config}
        onSlotMount={this.onSlotMount}
      />
    );
  }
}
```

In your React component, call `onSlotMount(slotName, containerEl)` after the container renders to move Shiny content into place.

### Key Methods

#### getConfig()

Parses `data-*` attributes into a props object with JSON auto-parsing:

```html
<my-widget data-count="5" data-items="[1,2,3]" data-title="Hello">
```

Returns: `{ count: 5, items: [1,2,3], title: "Hello" }`

- Numbers/booleans parsed from JSON
- Arrays/objects parsed from JSON
- Invalid JSON stays as string

#### captureSlots(selector?)

Called automatically in `connectedCallback()`. Captures children matching selector (default `[data-slot]`).

If no matching elements found and element has children, all children are stored under the `__children__` slot.

#### mountSlot(slotName, container)

Moves captured slot content into the container element and calls `Shiny.bindAll()`.

#### onSlotMount

Getter that returns `mountSlot.bind(this)` - pass this to React components as a callback.

#### clearContent()

Clears `innerHTML` before React renders. Override with no-op to preserve existing content:

```typescript
protected clearContent() {} // Keep existing content
```

### Override Points

- **`render()`**: Customize what React renders (default renders `static component` with `getConfig()` props)
- **`getConfig()`**: Customize attribute parsing
- **`clearContent()`**: Override to preserve innerHTML
- **`captureSlots()`**: Override with custom selector

### HTML Structure

R:
```r
tag("my-widget", list(
  id = "widget1",              # Used for namespace
  `data-title` = "My Title",   # Becomes props.title
  `data-count` = 5             # Becomes props.count (number)
))
```

Python:
```python
ui.HTML('<my-widget id="widget1" data-title="My Title" data-count="5"></my-widget>')
```
