# Rapp Advanced Reference

## Table of Contents

- [API Reference](#api-reference)
- [Launcher Customization](#launcher-customization)
- [PATH Setup](#path-setup)
- [Additional Examples](#additional-examples)

---

## API Reference

### `Rapp::run(app, args = commandArgs(TRUE))`

Run an Rapp script from within R. Returns the evaluation environment
(invisibly) for inspection. Returns `NULL` when `--help` is used.

```r
env <- Rapp::run("exec/myapp", c("--count", "5"))
ls(env)  # inspect variables set by the app
```

### `Rapp::install_pkg_cli_apps(package, destdir, lib.loc, overwrite)`

Install CLI launchers for scripts in a package's `exec/` directory.

- `package`: Package name(s). Defaults to all installed packages when
  called outside a package.
- `destdir`: Where to write launchers. Resolution order:
  `RAPP_INSTALL_DIR` env var → `XDG_BIN_HOME` → `~/.local/bin`
  (macOS/Linux) or `%LOCALAPPDATA%\Programs\R\Rapp\bin` (Windows).
- `overwrite`: `TRUE` always; `FALSE` never; `NA` (default) prompts
  interactively.
- Returns: Invisibly, paths of launchers written.

### `Rapp::uninstall_pkg_cli_apps(package, destdir)`

Remove launchers previously installed by `install_pkg_cli_apps()`.

---

## Launcher Customization

Scripts shipped in packages can customize their launcher via `#| launcher:`
front matter:

```r
#!/usr/bin/env Rapp
#| description: About this app
#| launcher:
#|   vanilla: true
#|   default-packages: [base, utils, mypkg]
```

Options map to `Rscript`/`Rapp` flags:
- `vanilla: true` → `--vanilla`
- `no-environ: true` → `--no-environ`
- `default-packages: [base, mypkg]` → controls auto-loaded packages

---

## PATH Setup

### macOS/Linux

Add `~/.local/bin` to PATH in `~/.bashrc` or `~/.zshrc`:

```sh
export PATH="$HOME/.local/bin:$PATH"
```

Override the install directory:

```sh
export RAPP_INSTALL_DIR="$HOME/bin"
```

### Windows

- `install_pkg_cli_apps()` creates `.bat` wrappers
- The install directory is auto-added to PATH (unless
  `RAPP_NO_MODIFY_PATH=1` is set)
- For standalone scripts: `Rapp path\to\myapp.R --count 5`

---

## Additional Examples

### Deduplication Filter (stdin/stdout + Optional Positional)

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

```sh
cat data.txt | unique.R
unique.R data.txt
unique.R data.txt --output deduped.txt
unique.R data.txt --from-last
```

### Variadic Args (install-pkg style)

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

```sh
install-pkg dplyr ggplot2 tidyr
install-pkg r-lib/rlang --force
install-pkg --Ncpus 8 dplyr ggplot2
```

### Interactive Fallback (magic-8-ball style)

```r
#!/usr/bin/env Rapp
#| name: magic-8-ball
#| description: |
#|   Ask a yes-no question and get your answer.

#| description: The question you want to ask.
question <- NULL

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
