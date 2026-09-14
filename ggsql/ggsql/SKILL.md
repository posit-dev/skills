---
name: ggsql
description: Write ggsql queries — a grammar of graphics for SQL. Use when the user wants to create, modify, or understand a ggsql visualization query.
allowed-tools: Bash(ggsql:*)
metadata:
  author: George Stagg (@georgestagg)
  version: "1.1"
license: MIT
---

# ggsql Query Writer

ggsql is a SQL extension for declarative data visualization based on Grammar of Graphics principles, combining SQL data queries with a visualization spec in one composable syntax. When the user describes a visualization, write a valid query using ONLY the syntax documented below — NEVER invent clauses, settings, aesthetics, or layer types.

## Query structure

A query has an optional SQL part and a required VISUALISE part (begins with `VISUALISE`, or `VISUALIZE`).

**Pattern A — SELECT → VISUALISE**: the last SQL statement is a SELECT (bare, `WITH...SELECT`, or `UNION`/`INTERSECT`/`EXCEPT`); its result set flows into VISUALISE, which has no `FROM`.

```ggsql
SELECT name, score_a, score_b FROM 'dataset.csv' WHERE value > 50
VISUALISE score_a AS x, score_b AS y
[DRAW / PLACE / SCALE / FACET / PROJECT / LABEL clauses]
```

**Pattern B — VISUALISE FROM**: VISUALISE supplies its own data source — a table, file, CTE, or built-in dataset — directly, without a trailing SELECT.

```ggsql
VISUALISE score_a AS x, score_b AS y FROM 'dataset.csv'
DRAW point
```

```ggsql
WITH summary AS (SELECT category, COUNT(*) AS n FROM 'dataset.csv' GROUP BY category)
VISUALISE category AS x, n AS y FROM summary
DRAW bar
```

## Data sources

Usable in `VISUALISE ... FROM` or `DRAW ... MAPPING ... FROM`:

- **Table/CTE** (unquoted): `FROM sales`, `FROM my_cte`
- **File path** (single-quoted string): `FROM 'data.parquet'`, `FROM 'data.csv'`
- **Built-in datasets**: `FROM ggsql:penguins`, `FROM ggsql:airquality`

## VISUALISE clause

Starts the visualization; optionally defines global mappings inherited by every layer.

```
VISUALISE <mapping>, ... FROM <data-source>
```

Mapping forms:
- **Explicit**: `column AS aesthetic` — e.g. `revenue AS y`
- **Implicit**: `column` — name must match the aesthetic, e.g. `x` maps to `x`
- **Wildcard**: `*` — all columns whose names match an aesthetic
- **Constant**: `'red' AS fill`, `42 AS size`

```ggsql
VISUALISE bill_len AS x, bill_dep AS y, species AS fill FROM ggsql:penguins
VISUALISE * FROM my_table
VISUALISE FROM ggsql:penguins
```

## DRAW clause

Defines a layer. Multiple DRAW clauses stack (first = bottom, last = top). All subclauses are optional if VISUALISE already provides global mappings and data.

```
DRAW <layer-type>
  MAPPING <mapping>, ... FROM <data-source>
  REMAPPING <stat-property> AS <aesthetic>, ...
  SETTING <param> => <value>, ...
  FILTER <condition>
  PARTITION BY <column>, ...
  ORDER BY <column>, ...
```

### MAPPING

Same forms as VISUALISE. Layer mappings merge with global mappings (layer wins) and can add a layer-specific `FROM`. Use `null` to block inheriting a global mapping: `MAPPING null AS color`.

### REMAPPING

For statistical layers (`histogram`, `density`, `boxplot`, `violin`, `smooth`, `bar` without y): maps a computed stat to an aesthetic. Each layer documents its own stats and default remapping.

```ggsql
DRAW histogram
  MAPPING body_mass AS x
  REMAPPING density AS y  -- use density instead of default count
```

### SETTING

Sets literal aesthetic values or layer parameters. Aesthetics set this way bypass scales.

```ggsql
DRAW point SETTING size => 5, opacity => 0.7, stroke => 'red'
```

**Position adjustment** (a special setting): `'identity'` (no adjustment, default for most), `'stack'` (default for bar/histogram/area), `'dodge'` (default for boxplot/violin), `'jitter'` (random offset).

**Aggregate** collapses each group — `PARTITION BY` columns plus all discrete mappings — to one row, replacing every numeric mapping in place with its aggregated value. Supported by `point`, `line`, `path`, `bar`, `area`, `ribbon`, `range`, `segment`, `rule`, `text`, `tile`; not by layers with their own stats (`histogram`, `density`, `smooth`, `boxplot`, `violin`).

```ggsql
SETTING aggregate => '<spec>'                -- single
SETTING aggregate => ('<spec>', '<spec>', …) -- list
```

Each `<spec>` is **untargeted** (`'<func>'`, applies to every numeric mapping without an explicit target — at most two untargeted defaults, the first for lower-side aesthetics like `x`/`xmin` plus all non-range layers, the second for upper-side like `xend`/`xmax`) or **targeted** (`'<aes>:<func>'`, applies only to that aesthetic, overriding any untargeted default for it).

Functions: reductions `count, sum, prod, min, max, range (max−min), mid ((min+max)/2), mean, median, geomean, harmean, rms, sdev, var, iqr, se, p05–p95`; positional (rely on an upstream `ORDER BY`) `first, last, diff (last−first)`; band `<offset>±[<mult>]<expansion>`, e.g. `'mean+1.96sdev'`, `'median-iqr'` — offsets `mean/median/geomean/harmean/rms/sum/prod/min/max/mid/p05–p95`, expansions `sdev/se/var/iqr/range`.

**Explosion** — targeting one aesthetic with multiple functions emits one row per function per group, tagged by a synthetic `aggregate` column (drive another aesthetic from it via `REMAPPING aggregate AS <aes>`). Aesthetics exploded to the same length explode in lockstep (row 1 = each target's first function, etc.); single-function targets repeat on every row. Mixing target lengths > 1 is an error.

```ggsql
-- min/max envelope as two lines per group, coloured by function
DRAW line
  MAPPING Date AS x, Temp AS y
  REMAPPING aggregate AS color
  SETTING aggregate => ('y:min', 'y:max')
  PARTITION BY Year
```

**Scale interaction** — for an aesthetic *targeted* by aggregate, `SCALE BINNED <aes>` runs after aggregation (otherwise diff/mean etc. would cancel within a bin); untargeted `SCALE BINNED` still bins pre-aggregate so bins can drive grouping. Continuous censoring (`SCALE <aes> FROM (lo, hi)`) and discrete OOB filtering defer to post-aggregate whenever the aesthetic is being aggregated.

### FILTER

SQL WHERE condition applied to layer data, passed straight to the database:

```ggsql
DRAW point FILTER sex = 'female' AND body_mass > 4000
```

### PARTITION BY

Extra grouping columns beyond mapped discrete aesthetics:

```ggsql
DRAW line MAPPING Day AS x, Temp AS y PARTITION BY Month
```

### ORDER BY

Controls record order (matters for `path` layers): `DRAW path ORDER BY timestamp`

## PLACE clause

Annotation layer with literal values only, no data mapping. Supports tuples for multiple annotations.

```
PLACE <layer-type> SETTING <aesthetic/param> => <value>, ...
```

```ggsql
PLACE point SETTING x => 5, y => 10, color => 'red'
PLACE rule SETTING y => 70, linetype => 'dotted'
PLACE text SETTING x => (34, 44), y => (66, 49), label => ('Mean = 34', 'Mean = 44')
```

## SCALE clause

Controls how data values map to aesthetic output. Sensible defaults always apply.

```
SCALE <type> <aesthetic> FROM <input-range> TO <output-range> VIA <transform>
  SETTING <param> => <value>, ...
  RENAMING <value> => <label>, ...
```

Everything except `aesthetic` is optional.

**Types** (placed before the aesthetic; inferred from data if omitted): `CONTINUOUS`, `DISCRETE`, `BINNED` (bin continuous data into discrete groups — never auto-selected), `ORDINAL` (ordered discrete — never auto-selected), `IDENTITY` (pass through unchanged, no legend).

**Aesthetic names** — base name only: `x`, `y`, `fill`, `stroke`, `color` (sets both fill and stroke), `opacity`, `size`, `linewidth`, `linetype`, `shape`, `panel` (facet), `row`, `column`. Position families (xmin/xmax/xend/ymin/ymax/yend) scale via the base name, e.g. `SCALE x ...`.

**FROM** (input range): continuous `FROM (min, max)`, `null` infers from data (`FROM (0, null)`); discrete `FROM ('A', 'B', 'C')` sets order and nulls omitted values, or include null explicitly (`FROM ('Torgersen', 'Biscoe', null)`).

**TO** (output range): value array (`TO ('red', 'blue', 'green')`, `TO (1, 6)`) or a named palette (`TO viridis`, `TO dark2`, `TO tableau10`).

**VIA** (transform) — continuous: `linear, log, log2, ln, exp10, exp2, exp, sqrt, square, asinh, pseudo_log, pseudo_log2, pseudo_ln, integer`; temporal (auto-chosen for date/datetime/time columns): `date, datetime, time`; discrete: `string, bool`.

```ggsql
SCALE x VIA date        -- treat x as temporal
SCALE y VIA log         -- log transform
SCALE size VIA square   -- scale by radius not area
```

**SETTING** — continuous/binned: `expand` (factor, scalar or `(mult, add)`, default `0.05`, x/y only), `oob` (`'keep'` default for x/y, `'censor'` default for others, `'squish'`), `breaks` (count, value array, or interval string like `'2 months'`), `pretty` (bool, default `true`, Wilkinson's algorithm), `reverse` (bool, default `false`). Continuous only: `minor_breaks` (unlabelled subdivisions per interval — count, `0` to remove, value array, or interval string; Vega-Lite ignores it). Binned only: `closed` (`'left'` default / `'right'`). Discrete/ordinal: `reverse` (bool).

```ggsql
SCALE x SETTING breaks => '2 months'
SCALE y FROM (0, 100) SETTING oob => 'squish'
SCALE BINNED x SETTING breaks => 10, pretty => false
```

**RENAMING** — direct renaming, wildcard formatting, or both (direct wins):

```ggsql
RENAMING 'Adelie' => 'Pygoscelis adeliae', 'adelie' => null  -- direct / suppress
RENAMING * => '{} mm'                -- string interpolation
RENAMING * => '{:Title}'             -- formatters: Title, UPPER, lower, time %B %Y, num %.1f
```

## FACET clause

Splits data into small multiples.

```
FACET <column> BY <column>
  SETTING <param> => <value>, ...
```

1D `FACET region` (wrap layout, aesthetic `panel`); 2D `FACET region BY category` (grid layout, aesthetics `row`/`column`).

Settings: `free` (`null` default/fixed, `'x'`, `'y'`, or `('x', 'y')`), `missing` (`'repeat'` default, or `'null'`), `ncol`/`nrow` (1D layout, only one allowed).

Customize strip labels or filter panels via SCALE on the facet aesthetic:

```ggsql
FACET region
SCALE panel RENAMING 'N' => 'North', 'S' => 'South'
```

```ggsql
FACET island
SCALE panel FROM ('Biscoe', 'Dream')
```

## PROJECT clause

Controls the coordinate system.

```
PROJECT <aesthetic>, ... TO <coord-type>
  SETTING <param> => <value>, ...
```

**cartesian** (default) — aesthetics `x`, `y`; settings `clip` (bool, default true), `ratio` (aspect ratio or null).

**polar** — aesthetics `radius` (primary), `angle` (secondary); settings `clip`, `start`/`end` (degrees, default `0`/`start+360`), `inner` (0-1 donut hole, default `0`).

Swap aesthetic order to flip axes (`PROJECT y, x TO cartesian`). Without PROJECT, coordinate type is inferred from mappings (x/y → cartesian, radius/angle → polar).

```ggsql
PROJECT TO polar SETTING inner => 0.5              -- donut chart
PROJECT TO polar SETTING start => -90, end => 90   -- half-circle gauge
```

## LABEL clause

Overrides default axis/legend labels and adds titles.

```
LABEL <aesthetic/title> => <string>, ...
```

Labels: `title`, `subtitle`, `caption`, or any aesthetic name (axis/legend title). `null` suppresses a label: `fill => null`.

```ggsql
LABEL
  title => 'Sales by Region',
  subtitle => 'Q4 2024 data',
  x => 'Date', y => 'Revenue (USD)', fill => 'Region',
  caption => 'Source: internal sales database'
```

---

## Layer types

### point
Scatterplot. Required: x, y. Optional: size, colour, stroke, fill, opacity, shape.

### line
Line plot sorted along the primary axis. Required: x, y. Optional: colour/stroke, opacity, linewidth, linetype. Settings: `position`, `orientation` (`'aligned'`/`'transposed'`).

### path
Like line but connects points in data order (not sorted). Same aesthetics as line.

### bar
Bar chart, auto-counts if y not provided. Optional: x (categories), y (height), fill, colour, stroke. Stats: `count`, `proportion`. Properties: `weight`. Settings: `position` (default `'stack'`), `width` (0-1). Orientation inferred from mapping (categories on x = vertical, on y = horizontal).

```ggsql
DRAW bar MAPPING species AS x                              -- auto-count
DRAW bar MAPPING species AS x, total AS y                  -- pre-computed
DRAW bar MAPPING species AS x, sex AS fill                 -- stacked (default)
  SETTING position => 'dodge'                              -- side by side
```

### histogram
Bins continuous data. Required: x. Stats: `count`, `density`. Default remapping: `count AS <secondary>`. Settings: `position` (default `'stack'`), `bins` (default 30), `binwidth`, `closed` (`'left'`/`'right'`).

```ggsql
DRAW histogram MAPPING body_mass AS x SETTING binwidth => 100
DRAW histogram MAPPING body_mass AS x REMAPPING density AS y  -- density instead of count
```

### density
Kernel density estimation. Required: x. Stats: `density`, `intensity`. Settings: `position` (default `'identity'`), `bandwidth`, `adjust` (default 1), `kernel` (`'gaussian'` default, `'epanechnikov'`, `'triangular'`, `'rectangular'`, `'biweight'`, `'cosine'`).

### boxplot
Five-number summary with outliers. Required: x (categorical), y (continuous). Stats: `type`, `value`. Settings: `position` (default `'dodge'`), `outliers` (default true), `coef` (whisker IQR multiple, default 1.5), `width` (default 0.9), `hinge` (whisker cap width in points, default null/hidden).

### violin
Mirrored kernel density for groups. Required: x (categorical), y (continuous). Stats: `density`, `intensity`. Default remapping: `density AS offset`. Settings: `position` (default `'dodge'`), `bandwidth`, `adjust`, `kernel` (same as density), `width` (default 0.9), `side` (`'both'`/`'left'`/`'bottom'`/`'right'`/`'top'`), `tails` (number or null, default 3).

### smooth
Trendline. Required: x, y. Stats: `intensity`. Settings: `method` (`'nw'` default, `'ols'`, `'tls'`), `bandwidth`, `adjust`, `kernel` (same as density, nw only).

### area
Area chart anchored at zero. Required: x, y. Settings: `position` (default `'stack'`), `orientation`, `total` (normalize stacks), `center` (boolean, for steamgraph).

### ribbon
Like area but with explicit ymin/ymax (unanchored). Required: x, ymin, ymax.

### segment
Line segments between two endpoints. Required: x, y, xend, yend. For axis-aligned intervals where one coordinate is shared between start and end, use `range` instead.

### rule
Reference lines spanning the full panel. Required: x or y. Optional: `slope` (for diagonal: `y = a + slope * x`).

### text
Text labels. Required: x, y, label. Settings: `offset` (number or `(h, v)`), `format` (string interpolation like RENAMING), `parse` (boolean, default `true`: read the label as markdown — `**bold**`, `*italic*`, `~~strike~~`, `` `code` ``, `{.red span}` — set `false` to draw it literally; not Vega-Lite, which has no rich text). `hjust`: `'left'`/`'right'`/`'centre'` or 0-1. `vjust`: `'top'`/`'bottom'`/`'middle'` or 0-1.

### rect
Rectangles. Required: pick 2 per axis from center (x/y), min (xmin/ymin), max (xmax/ymax), width, height. Or just center (defaults width/height to 1).

### polygon
Closed shapes from ordered coordinates. Required: x, y. Use PARTITION BY to separate distinct polygons.

### range
Range/interval display between two values along the secondary axis. Required: x, ymin, ymax. Settings: `hinge` (hinge width in points, default 10, null to hide).

All layers accept common optional aesthetics (colour/stroke, fill, opacity, linewidth, linetype) and `position` setting where applicable.

---

## Named color palettes

- **Discrete**: `ggsql10` (default), `tableau10`, `category10`, `set1`, `set2`, `set3`, `dark2`, `paired`, `pastel1`, `pastel2`, `accent`, `kelly22`
- **Sequential**: `sequential` (default), `viridis`, `plasma`, `magma`, `inferno`, `cividis`, `blues`, `greens`, `oranges`, `reds`, `purples`, `greys`, `ylgnbu`, `ylorbr`, `ylorrd`, `batlow`, `hawaii`, `lajolla`, `turku`, and more
- **Diverging**: `vik`/`diverging`, `rdbu`, `rdylbu`, `rdylgn`, `spectral`, `brbg`, `prgn`, `piyg`, `puor`, `berlin`, `roma`, and more
- **Cyclic**: `romao`/`cyclic`, `bamo`, `broco`, `corko`, `viko`

---

## Common patterns

```ggsql
-- Pie chart: bar layer projected to polar coordinates
VISUALISE species AS fill FROM ggsql:penguins
DRAW bar
PROJECT TO polar

-- Multi-series line chart
VISUALISE Date AS x
DRAW line MAPPING Temp AS y, 'Temperature' AS color
DRAW line MAPPING Ozone AS y, 'Ozone' AS color
SCALE x VIA date

-- Lollipop chart
SELECT ROUND(bill_dep) AS bill_dep, COUNT(*) AS n FROM ggsql:penguins GROUP BY 1
VISUALISE bill_dep AS x
DRAW range MAPPING 0 AS ymin, n AS ymax SETTING hinge => null
DRAW point MAPPING n AS y

-- Ridgeline / joy plot
VISUALISE Temp AS x, Month AS y FROM ggsql:airquality
DRAW violin SETTING width => 4, side => 'top'
SCALE ORDINAL y

-- Bar labels
SELECT island, COUNT(*) AS n FROM ggsql:penguins GROUP BY island
VISUALISE island AS x, n AS y
DRAW bar
DRAW text MAPPING n AS label SETTING vjust => 'top', offset => (0, -11), fill => 'white'

-- CTEs with separate layer data
WITH temps AS (SELECT Date, Temp as value FROM ggsql:airquality),
ozone AS (SELECT Date, Ozone as value FROM ggsql:airquality WHERE Ozone IS NOT NULL)
VISUALISE
DRAW line MAPPING Date AS x, value AS y, 'Temperature' AS color FROM temps
DRAW point MAPPING Date AS x, value AS y, 'Ozone' AS color FROM ozone
SCALE x VIA date

-- Per-week summary: open/close range, weekly temperature change (binned post-aggregate)
VISUALISE Date AS x, Temp AS ymin, Temp AS ymax, Temp AS color
  FROM ggsql:airquality
DRAW range
  SETTING aggregate => ('x:first', 'ymin:first', 'ymax:last', 'color:diff'),
          hinge => null
  PARTITION BY Week
SCALE BINNED color

-- Mean ± 1.96·sdev band per group, drawn as a ribbon
VISUALISE Day AS x, Temp AS ymin, Temp AS ymax FROM ggsql:airquality
DRAW ribbon
  SETTING aggregate => ('mean-1.96sdev', 'mean+1.96sdev')
  PARTITION BY Month
```

---

## CLI

The `ggsql` CLI should be on the PATH. Subcommands: `exec <QUERY>`, `run <FILE>`, `validate <QUERY>`, `parse <QUERY>`, `view <QUERY>` (native window, blocks until closed). Common options: `--reader <URI>` (default `duckdb://memory`), `--writer <FORMAT>` (default `vegalite`), `--output <PATH>` (extension picks the writer when `--writer` is omitted), `-D key=value` (writer settings), `-v` (verbose). Writers: `vegalite`, `svg`, `pdf`, `hep` (no GPU needed) and `png`, `jpeg`, `tiff`, `webp` (rasterise on the GPU, not in every build).

**Do not run `ggsql view` unless the user asked for a window** — it blocks until a person closes it, and you cannot close it yourself. Write a file with `--output` and look at that instead.

**Prefer `svg` or `pdf` when you need a picture**, since they need no GPU adapter (the raster writers do, and discover it only at render time). `ggsql exec --help` lists the writers this build has and names the feature that would add a missing one; it cannot tell you whether an adapter is present.

```bash
ggsql validate "VISUALISE x, y FROM data DRAW point"
ggsql exec "VISUALISE bill_len AS x, bill_dep AS y FROM ggsql:penguins DRAW point" -v
ggsql run query.sql --output chart.vl.json
ggsql exec "VISUALISE species AS fill FROM ggsql:penguins DRAW bar" -o chart.svg
```

---

## Additional References

* https://ggsql.org/syntax/index.llms.md — Online documentation with the latest syntax

---

## Instructions for responding

1. Write a complete, valid ggsql query matching the user's request.
2. Use SQL CTEs/queries before VISUALISE when data shaping is needed.
3. Choose the simplest layer types and settings that achieve the goal.
4. Include SCALE clauses when the defaults are insufficient (e.g. date formatting, custom palettes, range limits).
5. Include LABEL for titles when the context warrants it.
6. Briefly explain your choices after the query.
7. NEVER invent syntax, settings, aesthetics, layer types, or palette names not documented above — if unsure whether a feature exists, say so rather than guessing.
8. Use `ggsql:penguins` or `ggsql:airquality` as example data when no specific data is mentioned.
9. When the user wants to validate a query, use `ggsql validate "<query>"`. When the user wants to see the output, use `ggsql exec "<query>" -v`.
