#!/usr/bin/env Rscript
# launch_app_dev.R — launch a Shiny app for deterministic agent inspection.
#
# Usage:  Rscript launch_app_dev.R [path/to/app] [port]
# Defaults: app ".", port 7654. Run in the background and CAPTURE its
# stdout/stderr — that stream is the source of truth for server errors.
# Your browser attaches to http://127.0.0.1:<port>; no system browser opens.

if (!requireNamespace("shiny", quietly = TRUE)) {
  stop("Package 'shiny' is required. Install with install.packages('shiny').", call. = FALSE)
}

args <- commandArgs(trailingOnly = TRUE)
app_dir <- if (length(args) >= 1) args[[1]] else "."
port    <- if (length(args) >= 2) as.integer(args[[2]]) else 7654L

options(
  shiny.port           = port,
  shiny.host           = "127.0.0.1",
  shiny.fullstacktrace = TRUE,   # full server traceback on error
  shiny.sanitize.errors = FALSE  # show real error text in dev
)
shiny::devmode(TRUE)             # client-side error console + dev defaults

# Determinism: pin anything the app might pull from the environment.
set.seed(1)
Sys.setenv(TZ = "UTC")

message(sprintf("Launching '%s' on http://127.0.0.1:%d", app_dir, port))
shiny::runApp(app_dir, launch.browser = FALSE)
