# shiny-react Internals

Deep dive into how shiny-react works under the hood. For advanced developers building custom components or debugging.

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Registry System](#registry-system)
- [Input Binding Mechanism](#input-binding-mechanism)
- [Output Binding Mechanism](#output-binding-mechanism)
- [Message System](#message-system)
- [Initialization Flow](#initialization-flow)
- [Extending shiny-react](#extending-shiny-react)

## Architecture Overview

shiny-react bridges React's component model with Shiny's reactive system through a four-layer architecture:

1. **React Components Layer**: Your app uses hooks (`useShinyInput`, `useShinyOutput`, `useShinyMessageHandler`) to communicate with Shiny.

2. **Registry Layer**: Three registries manage the connection between React and Shiny:
   - `InputRegistry` - Tracks all inputs and their React state setters
   - `OutputRegistry` - Manages output subscriptions and hidden DOM elements
   - `MessageRegistry` - Routes custom messages to registered handlers

3. **Shiny JavaScript API Layer**: The registries translate React operations into Shiny's native API:
   - Inputs call `Shiny.setInputValue()` with debouncing
   - Outputs use a custom `OutputBinding` class registered with Shiny
   - Messages use `Shiny.addCustomMessageHandler()`

4. **Shiny Server Layer**: Your R or Python backend receives inputs (`input$id`), sends outputs (`output$id <- render_*()`), and can push messages (`post_message()`).

```
React Hooks (useShinyInput, useShinyOutput, useShinyMessageHandler)
        │
        ▼
Registries (InputRegistry, OutputRegistry, MessageRegistry)
        │
        ▼
Shiny JS API (setInputValue, OutputBinding, addCustomMessageHandler)
        │
        ▼
Shiny Server R/Python (input$id, output$id, post_message)
```

## Registry System

### ReactRegistry (react-registry.ts)

Central registry that holds references to input and output registries:

```typescript
export interface ShinyReactRegistry {
  inputs: InputRegistry;
  outputs: OutputRegistry;
}

// Attached to window.Shiny.reactRegistry
function initializeReactRegistry() {
  const shiny = getShiny();
  shiny.reactRegistry = {
    inputs: new InputRegistry(),
    outputs: new OutputRegistry(),
  };
}
```

### InputRegistry (input-registry.ts)

Manages all React-to-Shiny input bindings:

```typescript
class InputRegistry {
  private inputs: Map<string, InputRegistryEntry<any>> = new Map();

  getOrCreate<T>(inputId: string, value: T): InputRegistryEntry<T>;
  get<T>(inputId: string): InputRegistryEntry<T> | undefined;
  has(inputId: string): boolean;
}
```

Each input has an `InputRegistryEntry`:

```typescript
class InputRegistryEntry<T> {
  id: string;
  value: T;
  useStateSetValueFns: Set<(value: T) => void>;  // React state setters
  shinySetInputValueDebounced: DebouncedFunction;
  opts: { priority?: EventPriority; debounceMs: number };

  setValue(value: T) {
    this.value = value;
    this.shinySetInputValueDebounced(value);  // Send to Shiny
    this.useStateSetValueFns.forEach(fn => fn(value));  // Update React
  }
}
```

Key behaviors:
- Multiple React components can share an input ID
- Values persist across component remounts
- Debouncing prevents excessive server calls

### OutputRegistry (output-registry.ts)

Manages Shiny-to-React output bindings:

```typescript
class OutputRegistry {
  private outputs: Map<string, OutputRegistryEntry<any>> = new Map();
  private container: HTMLElement;  // Hidden DOM container

  add<T>(outputId: string, setValue, setRecalculating);
  remove(outputId: string);
  has(outputId: string): boolean;
}
```

Each output has an `OutputRegistryEntry`:

```typescript
class OutputRegistryEntry<T> {
  id: string;
  private useStateSetValueFns: Set<(value: T) => void>;
  private useStateSetRecalculatingFns: Set<(value: boolean) => void>;

  setValue(value: T);       // Called by output binding
  setRecalculating(value: boolean);  // Called during recalculation
}
```

## Input Binding Mechanism

When `useShinyInput` is called:

```typescript
function useShinyInput<T>(id: string, defaultValue: T, options?) {
  // 1. Ensure registry is initialized
  ensureShinyReactInitialized();

  // 2. Get or create registry entry
  const reactRegistry = getReactRegistry();
  let startValue = defaultValue;
  const existingEntry = reactRegistry.inputs.get(id);
  if (existingEntry) {
    startValue = existingEntry.getValue();  // Preserve existing value
  }

  // 3. Create React state
  const [value, setValue] = useState<T>(startValue);

  // 4. Register this component's setState with the entry
  useEffect(() => {
    const entry = reactRegistry.inputs.getOrCreate(id, defaultValue);
    entry.addUseStateSetValueFn(setValue);

    return () => {
      entry.removeUseStateSetValueFn(setValue);
    };
  }, [id]);

  // 5. Return wrapped setter that goes through registry
  const setValueWrapped = useCallback((value: T) => {
    const entry = reactRegistry.inputs.get(id);
    entry?.setValue(value);  // Updates Shiny AND all React subscribers
  }, [id]);

  return [value, setValueWrapped];
}
```

**Data flow when value changes**: When the user calls the setter function, it triggers `InputRegistryEntry.setValue()`, which does two things in parallel: (1) sends the value to Shiny via a debounced `setInputValue()` call, updating `input$id` on the server, and (2) immediately updates all React components subscribed to this input, triggering re-renders.

```
setValue(newValue)
    │
    ├──> Shiny.setInputValue() ──> Server input$id
    │
    └──> React setState() ──> Component re-render
```

## Output Binding Mechanism

Outputs use Shiny's OutputBinding system with hidden DOM elements:

```typescript
function useShinyOutput<T>(outputId: string, defaultValue?) {
  const [value, setValue] = useState<T | undefined>(defaultValue);
  const [recalculating, setRecalculating] = useState(false);

  useEffect(() => {
    const reactRegistry = getReactRegistry();

    // Register with output registry
    // This creates a hidden <div id="outputId"> in the DOM
    reactRegistry.outputs.add(outputId, setValue, setRecalculating);

    return () => {
      reactRegistry.outputs.remove(outputId);
    };
  }, [outputId]);

  return [value, recalculating];
}
```

The custom OutputBinding:

```typescript
class ReactOutputBinding extends Shiny.OutputBinding {
  find(scope) {
    return $(scope).find(".shiny-react-output");
  }

  renderValue(el, data) {
    // Get registry entry and update React state
    const entry = Shiny.reactRegistry.outputs.get(el.id);
    entry?.setValue(data);
  }

  showProgress(el, show) {
    // Update recalculating state
    const entry = Shiny.reactRegistry.outputs.get(el.id);
    entry?.setRecalculating(show);
  }
}
```

Hidden DOM structure created by OutputRegistry:

```html
<div class="shiny-react-output-container" style="visibility: hidden">
  <div class="shiny-react-output" id="output1">...</div>
  <div class="shiny-react-output" id="output2">...</div>
</div>
```

**Data flow for outputs**: When the Shiny server sets an output value (e.g., `output$id <- render_json({...})`), the JSON data is sent to the browser via WebSocket. Shiny's binding system finds the hidden DOM element with matching ID and calls `ReactOutputBinding.renderValue()`, which retrieves the `OutputRegistryEntry` and calls `setValue()`. This updates all React components subscribed to that output via their setState functions.

```
Server output$id ──> WebSocket ──> OutputBinding.renderValue() ──> React setState()
```

## Message System

### MessageRegistry (message-registry.ts)

Manages custom message handlers:

```typescript
class ShinyMessageRegistry {
  private handlers: Map<string, Set<(data: any) => void>> = new Map();

  addHandler(type: string, handler: (data: any) => void);
  removeHandler(type: string, handler: (data: any) => void);
  dispatch(type: string, data: any);
}
```

Initialization registers with Shiny's custom message system:

```typescript
function initializeMessageRegistry() {
  const shiny = getShiny();
  shiny.messageRegistry = new ShinyMessageRegistry();

  // Register global handler for "shinyReactMessage" type
  Shiny.addCustomMessageHandler("shinyReactMessage", (message) => {
    shiny.messageRegistry.dispatch(message.type, message.data);
  });
}
```

Server-side `post_message()` wraps messages:

```r
# R
post_message <- function(session, type, data) {
  session$sendCustomMessage("shinyReactMessage", list(type = type, data = data))
}
```

## Initialization Flow

When shiny-react loads:

```typescript
let shinyReactInitialized = false;

function ensureShinyReactInitialized() {
  if (shinyReactInitialized) return;

  // 1. Create registries
  initializeReactRegistry();

  // 2. Register output binding with Shiny
  createReactOutputBinding();

  // 3. Set up message handler
  initializeMessageRegistry();

  shinyReactInitialized = true;
}
```

Timing with Shiny initialization:

```typescript
function useShinyInitialized(): boolean {
  const [initialized, setInitialized] = useState(false);

  useEffect(() => {
    const shiny = getShiny();
    shiny?.initializedPromise.then(() => {
      setInitialized(true);
    });
  }, []);

  return initialized;
}
```

## Extending shiny-react

### Custom Input Type

Create a hook for specialized input behavior:

```typescript
function useShinySlider(id: string, defaultValue: number, range: [number, number]) {
  const [value, setValue] = useShinyInput<number>(id, defaultValue, {
    debounceMs: 50,  // Fast updates for sliders
  });

  // Clamp value to range
  const setValueClamped = useCallback((v: number) => {
    setValue(Math.max(range[0], Math.min(range[1], v)));
  }, [setValue, range]);

  return [value, setValueClamped] as const;
}
```

### Custom Output Processor

Process output data before React receives it:

```typescript
function useProcessedOutput<T, R>(
  outputId: string,
  processor: (data: T) => R,
  defaultValue?: R
): [R | undefined, boolean] {
  const [raw, recalculating] = useShinyOutput<T>(outputId, undefined);

  const processed = useMemo(() => {
    return raw ? processor(raw) : defaultValue;
  }, [raw, processor, defaultValue]);

  return [processed, recalculating];
}

// Usage: Convert column-major to row-major
const [rows] = useProcessedOutput<ColMajor, Row[]>(
  "data",
  (data) => transpose(data),
  []
);
```

### Direct Registry Access

For advanced use cases:

```typescript
// Access registries directly
const shiny = window.Shiny as ShinyClassExtended;
const inputRegistry = shiny.reactRegistry.inputs;
const outputRegistry = shiny.reactRegistry.outputs;

// Manually trigger input update
inputRegistry.get("myInput")?.setValue(newValue);

// Check if output is registered
outputRegistry.has("myOutput");
```

### Debugging

```typescript
// Log all registered inputs
const shiny = window.Shiny as ShinyClassExtended;
for (const id of shiny.reactRegistry.inputs.keys()) {
  console.log(`Input: ${id}`, shiny.reactRegistry.inputs.get(id)?.getValue());
}

// Monitor Shiny WebSocket messages (dev tools)
// Network tab → WS → filter by "shiny"
```
