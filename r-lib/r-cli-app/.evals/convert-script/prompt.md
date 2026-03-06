Read @../../SKILL.md

I have an R script at `input-script.R` that renders markdown files to HTML. It works fine but all the paths and options are hardcoded. Convert it into a proper CLI app using Rapp and save the result as `md-render.R`.

The hardcoded values that should become CLI arguments:
- `input_dir` — should be a positional argument (required)
- `output_dir` — should be a positional argument (required)
- `template` — should be an optional named option (not always needed)
- `recursive` — should be a boolean flag (default TRUE)

Keep the core logic the same, just make it configurable from the command line.
