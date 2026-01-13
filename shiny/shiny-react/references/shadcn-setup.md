# shadcn/ui Integration

Guide for using shadcn/ui components and Tailwind CSS with shiny-react.

## Table of Contents

- [Overview](#overview)
- [Project Setup](#project-setup)
- [Build Configuration](#build-configuration)
- [Adding Components](#adding-components)
- [Using Components with shiny-react](#using-components-with-shiny-react)
- [Theming](#theming)

## Overview

shadcn/ui provides beautiful, accessible React components built with Tailwind CSS. Components are copied into your project (not installed as dependencies), giving you full control over customization.

## Project Setup

### 1. Initialize Project Structure

```
myapp/
├── package.json
├── tsconfig.json
├── components.json          # shadcn/ui configuration
├── build.ts                 # Custom build script
├── srcts/
│   ├── main.tsx
│   ├── globals.css          # Tailwind directives + CSS variables
│   ├── css.d.ts             # CSS module types
│   ├── lib/
│   │   └── utils.ts         # cn() utility function
│   └── components/
│       ├── ui/              # shadcn/ui components go here
│       │   ├── button.tsx
│       │   ├── card.tsx
│       │   └── input.tsx
│       └── App.tsx          # Your app components
├── r/
│   └── ...
└── py/
    └── ...
```

### 2. package.json Dependencies

```json
{
  "devDependencies": {
    "@types/react": "^19.1.12",
    "@types/react-dom": "^19.1.9",
    "chokidar": "^4.0.3",
    "concurrently": "^9.0.1",
    "esbuild": "^0.25.9",
    "esbuild-plugin-tailwindcss": "^1.2.4",
    "react": "^19.1.1",
    "react-dom": "^19.1.1",
    "tailwindcss": "^4.1.6",
    "typescript": "^5.9.2"
  },
  "dependencies": {
    "@posit/shiny-react": "^0.0.16",
    "@radix-ui/react-slot": "^1.0.2",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.1.0",
    "lucide-react": "^0.462.0",
    "tailwind-merge": "^2.2.0"
  }
}
```

### 3. tsconfig.json with Path Aliases

```json
{
  "compilerOptions": {
    "target": "es2022",
    "module": "es2022",
    "noEmit": true,
    "moduleResolution": "node",
    "lib": ["es2022", "DOM", "DOM.Iterable"],
    "jsx": "react-jsx",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "isolatedModules": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./srcts/*"]
    }
  },
  "include": ["srcts/**/*.ts", "srcts/**/*.tsx", "srcts/**/*.d.ts"]
}
```

### 4. components.json

```json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "new-york",
  "rsc": false,
  "tsx": true,
  "tailwind": {
    "config": "",
    "css": "src/styles/globals.css",
    "baseColor": "neutral",
    "cssVariables": true,
    "prefix": ""
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils",
    "ui": "@/components/ui",
    "lib": "@/lib",
    "hooks": "@/hooks"
  },
  "iconLibrary": "lucide"
}
```

### 5. srcts/lib/utils.ts

```typescript
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

### 6. srcts/globals.css

```css
@import "tailwindcss";

@layer base {
  :root {
    --background: oklch(1 0 0);
    --foreground: oklch(0.145 0 0);
    --card: oklch(1 0 0);
    --card-foreground: oklch(0.145 0 0);
    --popover: oklch(1 0 0);
    --popover-foreground: oklch(0.145 0 0);
    --primary: oklch(0.205 0 0);
    --primary-foreground: oklch(0.985 0 0);
    --secondary: oklch(0.97 0 0);
    --secondary-foreground: oklch(0.205 0 0);
    --muted: oklch(0.97 0 0);
    --muted-foreground: oklch(0.556 0 0);
    --accent: oklch(0.97 0 0);
    --accent-foreground: oklch(0.205 0 0);
    --destructive: oklch(0.577 0.245 27.325);
    --destructive-foreground: oklch(0.577 0.245 27.325);
    --border: oklch(0.922 0 0);
    --input: oklch(0.922 0 0);
    --ring: oklch(0.708 0 0);
    --radius: 0.625rem;
  }

  .dark {
    --background: oklch(0.145 0 0);
    --foreground: oklch(0.985 0 0);
    /* ... dark mode values */
  }
}

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground;
  }
}
```

### 7. srcts/css.d.ts

```typescript
declare module "*.css" {
  const content: { [className: string]: string };
  export default content;
}
```

## Build Configuration

### build.ts (with Tailwind processing)

```typescript
import chokidar from "chokidar";
import * as esbuild from "esbuild";
import tailwindPlugin from "esbuild-plugin-tailwindcss";

const production = process.argv.includes("--production");
const watch = process.argv.includes("--watch");

async function main() {
  const config: esbuild.BuildOptions = {
    entryPoints: ["srcts/main.tsx"],
    outfile: "r/www/main.js",  // or py/www/main.js
    bundle: true,
    format: "esm",
    minify: production,
    sourcemap: production ? undefined : "linked",
    alias: { react: "react" },
    logLevel: "info",
    plugins: [tailwindPlugin()],
  };

  if (watch) {
    const context = await esbuild.context(config);
    await context.rebuild();

    chokidar.watch(["srcts/", "tailwind.config.js"], {
      ignored: ["**/node_modules/**"],
      ignoreInitial: true,
    }).on("all", async () => {
      await context.rebuild();
    });
  } else {
    await esbuild.build(config);
  }
}

main();
```

### package.json Scripts

```json
{
  "scripts": {
    "build": "npx tsx build.ts --production",
    "watch": "npx tsx build.ts --watch",
    "dev": "concurrently \"npm run watch\" \"npm run shinyapp-r\""
  }
}
```

## Adding Components

### Install via CLI

```bash
# Add individual components
npx shadcn@latest add button card input badge

# Add all components
npx shadcn@latest add --all
```

Components are installed to `srcts/components/ui/`.

### Manual Installation

Copy component code from [ui.shadcn.com](https://ui.shadcn.com/docs/components) to `srcts/components/ui/`.

## Using Components with shiny-react

### Example: Card with Input

```typescript
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { useShinyInput, useShinyOutput } from "@posit/shiny-react";

export function TextInputCard() {
  const [text, setText] = useShinyInput<string>("user_text", "");
  const [processed, loading] = useShinyOutput<string>("processed_text", "");
  const [length] = useShinyOutput<number>("text_length", 0);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Text Input</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <Input
          placeholder="Type something..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
        <div className="bg-muted p-3 rounded-md">
          <pre className="text-sm">{processed || "No text yet"}</pre>
        </div>
        <Badge variant="secondary">Length: {length}</Badge>
      </CardContent>
    </Card>
  );
}
```

### Example: Button with Event Priority

```typescript
import { Button } from "@/components/ui/button";
import { useShinyInput, useShinyOutput } from "@posit/shiny-react";

export function ClickCounter() {
  const [clicks, setClicks] = useShinyInput<number>("button_clicks", 0, {
    priority: "event",  // Immediate handling for buttons
  });
  const [serverCount] = useShinyOutput<number>("click_count", 0);

  return (
    <div className="space-y-4">
      <Button onClick={() => setClicks(clicks + 1)}>
        Click Me
      </Button>
      <p className="text-muted-foreground">
        Server confirmed: {serverCount} clicks
      </p>
    </div>
  );
}
```

### Example: Plot in Card

```typescript
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ImageOutput } from "@posit/shiny-react";
import { useState } from "react";

export function PlotCard() {
  const [loading, setLoading] = useState(false);

  return (
    <Card>
      <CardHeader>
        <CardTitle>
          {loading ? "Generating Plot..." : "Data Visualization"}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <ImageOutput
          id="myplot"
          width="100%"
          height="300px"
          onRecalculating={setLoading}
          className="rounded-md"
        />
      </CardContent>
    </Card>
  );
}
```

## Theming

### Customizing Colors

Edit CSS variables in `globals.css`:

```css
:root {
  --primary: oklch(0.6 0.25 250);  /* Blue primary */
  --primary-foreground: oklch(1 0 0);
  /* ... */
}
```

### Dark Mode

Add dark class to root element:

```typescript
// Toggle dark mode
document.documentElement.classList.toggle("dark");
```

### Using Brand Colors

Combine with brand.yml by mapping brand colors to CSS variables:

```css
:root {
  --primary: var(--brand-primary, oklch(0.205 0 0));
  --accent: var(--brand-accent, oklch(0.97 0 0));
}
```

## Common Patterns

### Loading States

```typescript
const [data, loading] = useShinyOutput<Data>("data", undefined);

return (
  <Card>
    <CardContent>
      {loading ? (
        <Skeleton className="h-[200px] w-full" />
      ) : (
        <DataDisplay data={data} />
      )}
    </CardContent>
  </Card>
);
```

### Form Layout

```typescript
<Card>
  <CardHeader>
    <CardTitle>Settings</CardTitle>
  </CardHeader>
  <CardContent className="space-y-4">
    <div className="grid gap-4 md:grid-cols-2">
      <div className="space-y-2">
        <Label htmlFor="name">Name</Label>
        <Input id="name" value={name} onChange={...} />
      </div>
      <div className="space-y-2">
        <Label htmlFor="email">Email</Label>
        <Input id="email" type="email" value={email} onChange={...} />
      </div>
    </div>
    <Button type="submit">Save</Button>
  </CardContent>
</Card>
```

### Dashboard Layout

```typescript
export function App() {
  return (
    <div className="min-h-screen bg-background p-6">
      <div className="max-w-6xl mx-auto space-y-6">
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <Separator />
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          <MetricCard />
          <ChartCard />
          <TableCard />
        </div>
      </div>
    </div>
  );
}
```
