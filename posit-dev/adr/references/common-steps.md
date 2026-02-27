# Common Steps (Shared Across All Flows)

These are the standard procedures used across all three ADR creation workflows.

## Common Setup Steps

### Determine repository root and ADR location

1. Find the git repository root using `git rev-parse --show-toplevel`
2. If not a git repo, use the current working directory
3. Check if `adr/` directory exists at this location
4. If `adr/` doesn't exist or is empty, ask: "I don't see any existing ADRs in `adr/`. Is there a different location where ADRs are stored in this project, or should I initialize the ADR system in `adr/`?"
5. Store the confirmed ADR location as `{adr_location}` for use in subsequent steps

### Initialize ADR system if needed

If the user wants to initialize in a new location, ask for consent: "I'll initialize the ADR system by creating:
- `{adr_location}/` directory
- `{adr_location}/README.md` with documentation
- `{adr_location}/_template.md` with the MADR template

Should I proceed?"

If yes:
- Create the directory
- Create `{adr_location}/README.md` using the structure from skill's `references/README-example.md`
- Create `{adr_location}/_template.md` copying content from skill's `references/_template.md`

### Read the template

Read `{adr_location}/_template.md` to understand the expected format. If not found, use the template from skill's `references/_template.md`.

### Determine the next ADR number

- List existing ADRs in the confirmed location
- Find files matching pattern `[0-9][0-9][0-9][0-9]-*.md` (excludes _template.md, README.md)
- If no ADRs exist, use `0001`
- Otherwise, increment from the highest existing number

## Common Validation Steps

### Validate title

- Check it's in kebab-case format (e.g., "use-typescript" not "Use TypeScript")
- Check it's under 50 characters
- Check if filename `NNNN-{title}.md` already exists in `{adr_location}` (prevent duplicates)
- If validation fails, ask user to provide a corrected title

## Common Generation Steps

### Generate the ADR file

1. Create the ADR file at `{adr_location}/NNNN-<kebab-case-title>.md` using the template
2. Replace ALL template placeholders with actual content (see `guidelines.md` for template placeholder replacement rules)
3. Set today's date in YYYY-MM-DD format
4. Use comma-separated decider names as provided by user
5. Ensure "## Pros and Cons of the Options" section has subsections for each option with their specific pros/cons

### Update the index

1. Read `{adr_location}/README.md`
2. If README doesn't exist, create one using the structure from `references/README-example.md`
3. Find the "## Index" section
4. If Index section doesn't exist, add it at the end of the README (before any "Contributing" or "License" sections if they exist)
5. Generate one-line summary from the Decision Outcome section
6. Add entry format: `- [ADR-NNNN: Title](NNNN-title.md) - One-line summary`
7. Check for duplicate entries before adding
8. Write the updated README

### Present the result

Use the Read tool to show the user the full created ADR file content and ask if any changes are needed.
