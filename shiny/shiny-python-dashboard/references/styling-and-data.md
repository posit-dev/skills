# Styling and Data Loading

## Contents

- CSS inclusion
- Recommended CSS patterns
- Static data loading
- Live API data loading
- Pandas vs Polars

---

## CSS inclusion

Include CSS at the end of the page layout:

```python
# Core — as last arg inside ui.page_sidebar(...)
ui.include_css(app_dir / "styles.css")

# Express — at module level (after layout blocks)
ui.include_css(Path(__file__).parent / "styles.css")
```

---

## Recommended CSS patterns

### Minimal styles.css

```css
:root {
  --bslib-sidebar-main-bg: #f8f8f8;
}
```

Every template uses this sidebar background override.

### Hide Plotly toolbar

```css
.plotly .modebar-container {
  display: none !important;
}
```

Used in `nba-dashboard` and `stock-app` for a cleaner look.

---

## Chart sizing best practices

Always set explicit chart dimensions to prevent charts from rendering too small:

### Plotly

```python
fig.update_layout(
    height=400,    # explicit pixel height
    margin=dict(l=40, r=20, t=40, b=40),
)
```

### Matplotlib / Seaborn

```python
fig, ax = plt.subplots(figsize=(8, 4))  # width=8, height=4 inches
```

### Rules

- Always set `height` on Plotly figures (default can be too small in cards)
- Always use `figsize=(8, 4)` or similar for Matplotlib — never use the default
- Wrap charts in `ui.card(full_screen=True)` so users can expand them
- Handle missing data before plotting: `df.dropna(subset=[col])`

### Dark popover headers

```css
.popover {
  --bs-popover-header-bg: #222;
  --bs-popover-header-color: #fff;
}
.popover .btn-close {
  filter: var(--bs-btn-close-white-filter);
}
```

Used in `dashboard-tips` when `ui.popover()` is used for secondary inputs.

### General approach

No custom theme objects needed — rely on default bslib/Bootstrap theme with
CSS variable overrides. Keep `styles.css` minimal.

---

## Static data loading

Load CSVs in `shared.py` at module level — never inside the app file:

```python
# shared.py
from pathlib import Path
import pandas as pd  # or: import polars as pl

app_dir = Path(__file__).parent
df = pd.read_csv(app_dir / "data.csv")
```

Export computed constants that UI inputs need:

```python
bill_rng = (df["total_bill"].min(), df["total_bill"].max())
gp_max = df["GP"].max()
players_dict = dict(zip(df["person_id"], df["player_name"]))
```

---

## Live API data loading

Fetch live data inside `@reactive.calc` so it re-runs on input changes:

```python
@reactive.calc
def get_ticker():
    return yf.Ticker(input.ticker())

@reactive.calc
def get_data():
    dates = input.dates()
    return get_ticker().history(start=dates[0], end=dates[1])
```

Never fetch API data at module level — it would only run once at startup.

---

## Pandas vs Polars

Both are supported across templates. Choose based on ecosystem needs.

### Polars filtering (method chaining)

```python
tips.filter(
    pl.col("total_bill").is_between(bill[0], bill[1]),
    pl.col("time").is_in(input.time()),
)
```

### Pandas filtering (boolean indexing)

```python
idx = (df["GP"] >= games[0]) & (df["GP"] <= games[1])
return df[idx]
```

| Library | Used in |
|---|---|
| Polars | `dashboard-tips` |
| Pandas | `nba-dashboard`, `stock-app`, `basic-sidebar`, `basic-navigation` |
