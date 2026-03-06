# Render a set of markdown files to HTML using commonmark
# Currently hardcoded for my blog posts directory

library(commonmark)

input_dir <- "posts/"
output_dir <- "public/"
template <- "template.html"
recursive <- TRUE

files <- list.files(input_dir, pattern = "\\.md$", recursive = recursive, full.names = TRUE)

cat("Processing", length(files), "files...\n")

for (f in files) {
  html_body <- markdown_html(readLines(f, warn = FALSE) |> paste(collapse = "\n"))

  if (file.exists(template)) {
    page <- readLines(template, warn = FALSE) |> paste(collapse = "\n")
    page <- gsub("{{BODY}}", html_body, page, fixed = TRUE)
    page <- gsub("{{TITLE}}", tools::file_path_sans_ext(basename(f)), page, fixed = TRUE)
  } else {
    page <- html_body
  }

  rel_path <- sub(input_dir, "", f, fixed = TRUE)
  out_path <- file.path(output_dir, sub("\\.md$", ".html", rel_path))
  dir.create(dirname(out_path), recursive = TRUE, showWarnings = FALSE)
  writeLines(page, out_path)
  cat("  ", f, "->", out_path, "\n")
}

cat("Done.\n")
