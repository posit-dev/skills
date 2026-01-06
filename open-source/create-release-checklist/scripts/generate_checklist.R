#!/usr/bin/env Rscript
# Generate a release checklist for an R package
#
# Usage:
#   Rscript generate_checklist.R <new_version> [github_url]
#
# Arguments:
#   new_version: Target version for the release (e.g., "1.2.0")
#   github_url: (Optional) Full GitHub repository URL (e.g., "https://github.com/owner/repo")
#
# Output:
#   Markdown-formatted release checklist printed to stdout
#   Informational messages are printed to stderr
#
# Examples:
#   Rscript generate_checklist.R "1.2.0" "https://github.com/tidyverse/dplyr"
#   Rscript generate_checklist.R "1.2.0"

args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) {
  cat("usage: Rscript generate_checklist.R <new_version> [github_url]\n", file = stderr())
  quit(status = 1)
}

if (!requireNamespace("usethis", quietly = TRUE)) {
  cat("Error: usethis package is not installed\n")
  cat("Install it with: install.packages('usethis')\n")
  quit(status = 1)
}

new_version <- args[1]
url <- if (length(args) >= 2) args[2] else NULL
on_cran <- !is.null(usethis:::cran_version())

target_repo <- if (!is.null(url)) list(url = url) else NULL
checklist <- usethis:::release_checklist(new_version, on_cran, target_repo)
cat(checklist, sep = "\n")
