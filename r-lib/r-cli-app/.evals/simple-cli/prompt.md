Read @../../SKILL.md

Create an R CLI tool called `csv-summary` (save it as `csv-summary.R`) that takes a CSV file path, reads it, and prints summary statistics. It should have:

- A `--columns` option to specify which columns to summarize (comma-separated string, defaults to all columns if omitted)
- A `--verbose` flag that, when set, also prints the number of rows and columns before the summary
- An `--output` option to optionally write the summary to a file instead of stdout (if omitted, print to stdout)

The positional argument should be the path to the CSV file.
