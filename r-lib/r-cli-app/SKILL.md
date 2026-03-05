---
name: r-cli-app
description: >
  Build command-line applications (CLIs) in R using the Rapp package.
  Use this skill when a user wants to create a CLI tool written in R,
  turn an R script into a command-line app, add argument parsing to an
  R script, ship a CLI tool as part of an R package, or understand how
  to use Rapp (the alternative Rscript front-end). Also use when the
  user mentions shebang scripts, exec/ in an R package, installing R
  CLIs on PATH, or subcommand-based R tools.
metadata:
  author: Garrick Aden-Buie (@gadenbuie)
  version: "1.0"
license: MIT
---

# Building CLI Apps with Rapp

Rapp (v0.3.0, December 2025) is an R package that provides an alternative
front-end to R — a drop-in replacement for `Rscript` — that automatically
parses command-line arguments into R values. It turns simple R scripts into
polished CLI apps with argument parsing, generated help text, and subcommand
support, with zero boilerplate.

**Minimum R version:** R ≥ 4.1.0
**Author:** Tomasz Kalinowski (Posit, PBC)
**CRAN:** `install.packages("Rapp")`
**GitHub:** https://github.com/r-lib/Rapp

---

## Installation

```r
# Install from CRAN
install.packages("Rapp")

# Install the Rapp launcher on your PATH
Rapp::install_pkg_cli_apps("Rapp")
```

After calling `install_pkg_cli_apps("Rapp")`, the `Rapp` executable is placed
in a directory on (or added to) your PATH. The default install locations are:

- **macOS/Linux:** `~/.local/bin` (typically already on PATH if it exists)
- **Windows:** `%LOCALAPPDATA%\Programs\R\Rapp\bin` (auto-added to PATH)

You can override the install directory with the `RAPP_INSTALL_DIR` environment
variable or the `destdir` argument.

> **Note on shell restart:** On macOS/Linux, `~/.local/bin` is added to PATH
> at login. If `install_pkg_cli_apps()` created that directory for the first
> time, you may need to restart your shell before `Rapp` is found.

Development version:
```r
pak::pak("r-lib/Rapp")
# or
remotes::install_github("r-lib/Rapp")
```

---

## Core Concept: Scripts Are the Spec

Rapp works by scanning the **top-level expressions** of your R script and
converting specific patterns into CLI constructs. This means:

1. The same script runs identically in an interactive R session (`source()`)
   and as a CLI tool.
2. You write normal R code — Rapp infers the CLI from what you write.
3. Default values in your R code become the CLI defaults.

The pattern recognition happens at the **top level** only. Assignments inside
functions, loops, or conditional blocks are not parsed as CLI arguments.

---

## Pattern Recognition: R → CLI Mapping

| R Top-Level Expression | CLI Surface | Notes |
|---|---|---|
| `foo <- "text"` | `--foo <value>` | String option |
| `foo <- 1L` | `--foo <int>` | Integer option |
| `foo <- 3.14` | `--foo <float>` | Float option |
| `foo <- TRUE` or `foo <- FALSE` | `--foo` / `--no-foo` | Boolean toggle |
| `foo <- NA_integer_` | `--foo <int>` | Optional integer (NA = not set) |
| `foo <- NA_character_` | `--foo <str>` | Optional string (NA = not set) |
| `foo <- NULL` | positional arg | Required by default |
| `foo... <- NULL` | variadic positional | Collects zero or more values |
| `foo <- c()` | repeatable `--foo` | Multiple values as character strings |
| `foo <- list()` | repeatable `--foo` | Multiple values parsed as YAML/JSON |
| `switch("", cmd1={}, cmd2={})` | subcommands | `app cmd1`, `app cmd2` |
| `switch(cmd <- "", ...)` | subcommands | Same; assigns the command name to `cmd` |

### Important Notes on Types

- **Non-string scalars** at the CLI are parsed as YAML/JSON and coerced to the
  R type matching the default. So `n <- 5L` means `--n 10` gives integer 10L.
- **NA defaults** (`NA_integer_`, `NA_character_`, etc.) signal optional
  arguments. If the user doesn't supply the flag, the R variable stays `NA`.
  Test for presence with `!is.na(myvar)`.
- **Snake case** variable names automatically map to kebab-case at the CLI:
  `n_flips` → `--n-flips`.

---

## Script Structure

### The Shebang Line

```r
#!/usr/bin/env Rapp
```

Place this as the first line to make the script directly executable on
macOS/Linux (`chmod +x myscript.R` then `./myscript.R`). On Windows, call
`Rapp myscript.R` explicitly — Windows doesn't support shebang natively.

### Front Matter Metadata

Hash-pipe comments (`#|`) at the top of the file (before any non-comment
code) set script-level metadata:

```r
#!/usr/bin/env Rapp
#| name: my-app
#| description: |
#|   A short description of what this app does.
#|   Can span multiple lines using the YAML block scalar `|`.
#| title: My App
```

The `name:` field sets the app name in help output. If omitted, Rapp
derives it from the filename. The `description:` is shown in `--help`.

### Per-Argument Annotations

Place `#|` comments immediately before the assignment they annotate:

```r
#| description: Number of coin flips
#| short: 'n'
flips <- 1L
```

All annotation fields for options and positional args:

| Field | Purpose |
|---|---|
| `description:` | Help text shown in `--help` |
| `title:` | Display title (for subcommands especially) |
| `short:` | Single-letter short alias, e.g. `'n'` creates `-n` |
| `required:` | `true` or `false` — for positional args only |
| `val_type:` | Override inferred type: `string`, `integer`, `float`, `bool`, `any` |
| `arg_type:` | Override inferred CLI type: `option`, `switch`, `positional` |
| `action:` | For repeatable options: `replace` or `append` |

---

## Built-in Help

Every Rapp automatically gets two help flags:

- `--help` — Human-readable usage, description, and option list
- `--help-yaml` — Machine-readable YAML metadata spec

These work with subcommands too: `myapp list --help` shows only the `list`
subcommand's options plus global options.

---

## Options: Named Arguments

Scalar literal assignments at the top level become named options.

```r
# String option (default "world")
name <- "world"

# Integer option (default 1)
count <- 1L

# Float option (default 0.5)
threshold <- 0.5

# Optional integer — NA means "not provided"
seed <- NA_integer_
if (!is.na(seed)) {
  set.seed(seed)
}

# Optional string — NA means "not provided"
output_file <- NA_character_
if (!is.na(output_file)) {
  sink(output_file)
}
```

### Value Syntax at CLI

Options accept values with `=` or space:
```sh
myapp --name Alice
myapp --name=Alice
myapp --count 5
myapp --count=5
```

---

## Boolean Switches

Assignments to `TRUE` or `FALSE` become toggle switches:

```r
verbose <- FALSE
wrap <- TRUE
```

All of these set the value to `TRUE`:
```sh
myapp --verbose
myapp --verbose=yes
myapp --verbose=true
myapp --verbose=1
```

All of these set the value to `FALSE`:
```sh
myapp --no-verbose
myapp --verbose=no
myapp --verbose=false
myapp --verbose=0
```

---

## Repeatable Options

Use `c()` (raw strings) or `list()` (YAML/JSON-parsed values) for options
that can be supplied multiple times:

```r
# Collects raw strings
pattern <- c()
# myapp --pattern '*.csv' --pattern 'sales-*'
# Result: pattern = c("*.csv", "sales-*")

# Collects YAML/JSON-parsed values
threshold <- list()
# myapp --threshold 5 --threshold '[10, 20, 30]'
# Result: threshold = list(5L, c(10L, 20L, 30L))
```

Control the accumulation behavior with `#| action: append` (default) or
`#| action: replace` (last value wins).

---

## Positional Arguments

Assign `NULL` to declare a positional argument. Positional args are
**required by default** in Rapp 0.3.0+.

```r
#| description: The input file to process.
input_file <- NULL
# Called as: myapp data.csv
# Result: input_file = "data.csv"

# Make optional with:
#| required: false
output_file <- NULL
# Called as: myapp data.csv
# Result: output_file = NULL (not provided)
```

Positional args always arrive as **character strings** — convert with
`as.integer()`, `as.numeric()`, etc. if needed.

### Variable-Length Positional Args (`...`)

Use `...` as a suffix or prefix in the variable name to declare a
collector for any number of positional args:

```r
pkgs... <- c()
# Called as: install-pkgs dplyr ggplot2 tidyr
# Result: pkgs... = c("dplyr", "ggplot2", "tidyr")
```

If you use `NULL` with `...`:
```r
files... <- NULL
# Collects zero or more files as character vector
```

---

## Subcommands

Use a `switch()` statement with a character scalar (or assignment
expression) as its first argument to declare subcommands. Each branch
is a subcommand.

```r
switch(
  command <- "",

  #| title: Display the todos
  #| description: Print the contents of the todo list.
  list = {
    #| description: Maximum number of entries to display (-1 for all).
    limit <- 30L
    # ... code for list subcommand
  },

  #| title: Add a new todo
  #| description: Append a task description to the todo list.
  add = {
    #| description: Task description to add.
    task <- NULL
    # ... code for add subcommand
  },

  #| title: Mark a task as completed
  done = {
    #| description: Index of the task to complete.
    #| short: i
    index <- 1L
    # ... code for done subcommand
  }
)
```

- Options declared before the `switch()` are **global** and appear in
  `--help` for all subcommands.
- Options declared inside a branch are local to that subcommand.
- Help is scoped: `myapp --help` lists commands; `myapp list --help`
  shows list-specific options plus global ones.
- Subcommands can be **nested** by placing another `switch()` inside a
  branch.

The `command <- ""` pattern assigns the selected subcommand name to the
variable `command` so your code can reference it.

---

## Interactive Development

During development, use `Rapp::run()` to test apps from within an R session
without leaving the REPL:

```r
# Run with --help to see the CLI spec
Rapp::run("path/to/myapp.R", c("--help"))

# Run with specific arguments
Rapp::run("path/to/myapp.R", c("--name", "Alice", "--count", "5"))

# Use browser() in your app for debugging
# (breakpoints work during Rapp::run())
```

`Rapp::run()` invisibly returns the evaluation environment where the app's
expressions ran, which is useful for testing and inspection. It returns
`NULL` when `--help` is used (since the app exits early).

---

## Complete Examples

### Example 1: Coin Flipper

```r
#!/usr/bin/env Rapp
#| name: flip-coin
#| description: |
#|   Flip a coin.

#| description: Number of coin flips
#| short: 'n'
flips <- 1L

sep <- " "
wrap <- TRUE

seed <- NA_integer_
if (!is.na(seed)) {
  set.seed(seed)
}

cat(sample(c("heads", "tails"), flips, TRUE), sep = sep, fill = wrap)
```

Usage:
```sh
flip-coin            # heads
flip-coin -n 3       # heads tails heads
flip-coin --flips=30 --no-wrap --sep __
flip-coin --seed 42 -n 5
flip-coin --help
```

Auto-generated help:
```
Usage: flip-coin [OPTIONS]

Flip a coin.

Options:
  -n, --flips <FLIPS>  Number of coin flips [default: 1] [type: integer]
      --sep <SEP>      [default: " "] [type: string]
      --wrap / --no-wrap  [default: true]
      --seed <SEED>    [default: NA] [type: integer]
```

### Example 2: Todo List Manager (Subcommands)

```r
#!/usr/bin/env Rapp
#| name: todo
#| title: Todo manager
#| description: Manage a simple todo list.

#| description: Path to the todo list file.
#| short: s
store <- ".todo.yml"

switch(
  command <- "",

  #| title: Display the todos
  #| description: Print the contents of the todo list.
  list = {
    #| description: Maximum number of entries to display (-1 for all).
    limit <- 30L

    tasks <- if (file.exists(store)) yaml::read_yaml(store) else list()
    if (!length(tasks)) {
      cat("No tasks yet.\n")
    } else {
      if (limit >= 0L) tasks <- head(tasks, limit)
      writeLines(sprintf("%2d. %s\n", seq_along(tasks), tasks))
    }
  },

  #| title: Add a new todo
  #| description: Append a task description to the todo list.
  add = {
    #| description: Task description to add.
    task <- NULL

    tasks <- if (file.exists(store)) yaml::read_yaml(store) else list()
    tasks[[length(tasks) + 1L]] <- task
    yaml::write_yaml(tasks, store)
    cat("Added:", task, "\n")
  },

  #| title: Mark a task as completed
  #| description: Remove a task from the todo list using its index.
  done = {
    #| description: Index of the task to complete.
    #| short: i
    index <- 1L

    tasks <- if (file.exists(store)) yaml::read_yaml(store) else list()
    task <- tasks[[as.integer(index)]]
    tasks[[as.integer(index)]] <- NULL
    yaml::write_yaml(tasks, store)
    cat("Completed:", task, "\n")
  }
)
```

Usage:
```sh
todo add "Write quarterly report"
todo add "Review PR #42"
todo list
todo list --limit 5
todo done 1
todo --store /tmp/work.yml list
todo --help
todo add --help
```

### Example 3: Deduplication Filter (stdin/stdout + Optional Positional)

```r
#!/usr/bin/env Rapp
#| description: |
#|   Remove duplicate values from a file or input

#| description: remove duplicates in reverse order
from_last <- FALSE

#| description: Filepath. If omitted, output is written to stdout.
output <- NA_character_

#| description: Filepath. If omitted, input is read from stdin.
#| required: false
input <- NULL

if (is.null(input)) {
  input <- file("stdin")
}

if (is.na(output)) {
  output <- stdout()
}

readLines(input) |>
  unique(fromLast = from_last) |>
  writeLines(output)
```

Usage:
```sh
cat data.txt | unique.R
unique.R data.txt
unique.R data.txt --output deduped.txt
unique.R data.txt --from-last
```

### Example 4: Variadic Args (install-pkg style)

```r
#!/usr/bin/env Rapp

library(remotes)

force <- FALSE
Ncpus <- 4L

pkgs... <- c()

options("Ncpus" = Ncpus)

install <- function(pkg, ...) {
  if (grepl("^[./]", pkg)) return(install_local(pkg, ...))
  if (grepl("/", pkg, fixed = TRUE)) return(install_github(pkg, ...))
  install_cran(pkg, ...)
}

for (pkg in pkgs...) {
  install(pkg, force = force)
}
```

Usage:
```sh
install-pkg dplyr ggplot2 tidyr
install-pkg r-lib/rlang --force
install-pkg --Ncpus 8 dplyr ggplot2
```

### Example 5: Interactive Fallback (magic-8-ball style)

```r
#!/usr/bin/env Rapp
#| name: magic-8-ball
#| description: |
#|   Ask a yes-no question and get your answer.

#| description: The question you want to ask.
question <- NULL

# If question not provided on CLI, fall back to interactive prompt
if (is.null(question)) {
  question <- if (interactive()) {
    readline("question: ")
  } else {
    cat("question: ")
    readLines(file("stdin"), 1)
  }
} else {
  cat("question:", question, "\n")
}

cat("answer:", sample(c("Yes.", "No.", "Ask again later."), 1), "\n")
```

---

## Shipping CLIs in an R Package

### Directory Layout

Place CLI scripts in the `exec/` directory of your package:

```
mypkg/
├── DESCRIPTION
├── R/
├── exec/
│   ├── myapp       # script with #!/usr/bin/env Rapp shebang
│   └── myapp2      # another app
└── man/
```

Scripts in `exec/` are automatically marked executable when the package
is installed via `R CMD INSTALL`.

### DESCRIPTION Dependency

Add `Rapp` to your package's `Imports` or `Depends` in DESCRIPTION:

```
Imports:
    Rapp
```

### User Installation

After installing your package, users install the CLI launchers:

```r
Rapp::install_pkg_cli_apps("mypkg")
```

This scans `mypkg/exec/` for scripts with Rapp or Rscript shebangs and
writes lightweight shell launchers (`.bat` on Windows) to the user's PATH.

### Exporting a Convenience Installer

Expose an installer function so users don't need to remember the Rapp call:

```r
#' Install mypkg CLI apps
#' @export
install_mypkg_cli <- function(destdir = NULL) {
  Rapp::install_pkg_cli_apps(package = "mypkg", destdir = destdir)
}
```

Then users just run `mypkg::install_mypkg_cli()`.

### Package Default Packages

By default, launchers set `--default-packages=base,<pkg>`, so only
`base` and your package are loaded automatically. Use `library()` calls
inside the script for any other dependencies.

---

## API Reference

### `Rapp::run(app, args = commandArgs(TRUE))`

Run an Rapp from within R. Useful for development, testing, and debugging.

- `app`: File path to an Rapp script.
- `args`: Character vector of CLI args. Defaults to `commandArgs(TRUE)`,
  which means it works when called at the top level too.
- Returns: The evaluation environment (invisibly) for inspection.
  Returns `NULL` when the app exits early (e.g., `--help`).
- Supports `browser()` for interactive debugging.

```r
env <- Rapp::run("exec/myapp", c("--count", "5"))
ls(env)  # inspect variables set by the app
```

### `Rapp::install_pkg_cli_apps(package, destdir, lib.loc, overwrite)`

Install CLI launchers for scripts in a package's `exec/` directory.

- `package`: Package name(s). Defaults to calling package inside a
  package; all installed packages when called outside.
- `destdir`: Where to write launchers. Resolution order:
  `RAPP_INSTALL_DIR` env var → `XDG_BIN_HOME` → `XDG_DATA_HOME/../bin`
  → `~/.local/bin` (macOS/Linux) or `%LOCALAPPDATA%\Programs\R\Rapp\bin`
  (Windows).
- `lib.loc`: Additional library paths for finding package scripts.
- `overwrite`: `TRUE` always overwrites; `FALSE` never; `NA` (default)
  prompts interactively (skips in non-interactive sessions).
- Returns: Invisibly, paths of launchers that were written.

### `Rapp::uninstall_pkg_cli_apps(package, destdir)`

Remove launchers previously installed by `install_pkg_cli_apps()`.

---

## Launcher Customization (`#| launcher:`)

The front matter can include a `launcher:` block that customizes how the
launcher invokes R. This is only relevant for scripts shipped in packages.

```r
#!/usr/bin/env Rapp
#| description: About this app
#| launcher:
#|   vanilla: true
#|   default-packages: [base, utils, mypkg]
```

Supported launcher options map to `Rscript`/`Rapp` flags:
- `vanilla: true` — equivalent to `--vanilla`
- `no-environ: true` — equivalent to `--no-environ`
- `default-packages: [base, mypkg]` — controls which packages are
  auto-loaded (overrides the Rapp default of `base,<pkg>`)

---

## PATH Setup

### macOS/Linux

Add `~/.local/bin` to PATH if not already there (in `~/.bashrc` or
`~/.zshrc`):

```sh
export PATH="$HOME/.local/bin:$PATH"
```

Alternatively, add a package's `exec/` directory directly:

```sh
export PATH="$(Rscript -e 'cat(normalizePath(system.file("exec", package = "Rapp")))'):$PATH"
```

Or use the `RAPP_INSTALL_DIR` env var to control where launchers are
written:

```sh
export RAPP_INSTALL_DIR="$HOME/bin"
```

### Windows

On Windows:
- `install_pkg_cli_apps()` creates `.bat` wrappers
- The install directory is automatically added to `PATH` (unless
  `RAPP_NO_MODIFY_PATH=1` is set)
- For scripts outside packages, invoke directly:
  ```bat
  Rapp path\to\myapp.R --count 5
  ```

---

## Working with stdin/stdout

Rapp scripts can read from stdin and write to stdout, making them
composable Unix-style tools:

```r
# Read from stdin if no file arg provided
input_file <- NA_character_
con <- if (is.na(input_file)) file("stdin") else file(input_file, "r")
lines <- readLines(con)

# Write to stdout (default) or a file
output_file <- NA_character_
out <- if (is.na(output_file)) stdout() else file(output_file, "w")
writeLines(lines, out)
```

---

## Exit Codes

Use `quit(status = N)` to exit with a specific code:

```r
if (length(errors) > 0) {
  cat("Errors encountered\n", file = stderr())
  quit(status = 1)
}
```

Use `message()` or `cat(..., file = stderr())` to write to stderr.

---

## Comparison with Alternatives

| Package | Approach | Notes |
|---|---|---|
| **Rapp** | Zero-boilerplate, patterns from R code | No separate spec needed |
| **docopt** | Docstring-based spec | Explicit, familiar to Python devs |
| **optparse** | Explicit option declarations | Verbose, similar to Python's optparse |
| **argparse** | Explicit (wraps Python's argparse) | Requires Python |
| **argparser** | Explicit | Pure R |
| **littler** | Minimal front-end, pairs with above | Not argument-parsing itself |

---

## Common Patterns and Tips

### Testing Your Script
Make scripts executable and test from the terminal:

```sh
chmod +x myapp.R
./myapp.R --help
./myapp.R --myopt value
```

Or test from R during development:

```r
Rapp::run("myapp.R", c("--help"))
Rapp::run("myapp.R", c("--myopt", "value"))
```

### Accessing the Built-in Examples

```r
system.file("examples", package = "Rapp")
# Lists: flip-coin.R, install-pkg.R, magic-8-ball.R, todo.R, unique.R

# Read an example
readLines(system.file("examples/flip-coin.R", package = "Rapp"))
```

### Using rig

If users have `rig` installed, they can run package scripts without
installing launchers:

```sh
rig run mypkg::myapp --count 5
```

### Checking if Running as CLI vs Interactive

```r
if (interactive()) {
  # Running in an R session / IDE
} else {
  # Running as a CLI script
}
```

### Handling Errors Gracefully

```r
tryCatch({
  result <- do_work()
}, error = function(e) {
  cat("Error:", conditionMessage(e), "\n", file = stderr())
  quit(status = 1)
})
```

### Snake Case → Kebab Case Mapping

Variable names with underscores automatically map to kebab-case options:

```r
output_file <- "out.csv"   # → --output-file
max_count <- 100L          # → --max-count
from_last <- FALSE         # → --from-last / --no-from-last
```

### When to Use `NA` vs `NULL` for Optional Arguments

- Use `NA_integer_`, `NA_character_`, etc. for **optional named options**.
  The option flag exists but doesn't need to be supplied. Test with
  `!is.na(myvar)`.
- Use `NULL` + `#| required: false` for **optional positional args**.
  Test with `!is.null(myvar)` (or `is.null(myvar)` for "not provided").

---

## Registering in a Package's `marketplace.json`

When shipping this skill via the posit-dev skills repo, add to the
`r-lib` plugin's `skills` array in `.claude-plugin/marketplace.json`:

```json
"./r-lib/r-cli-app"
```
