# ADR Guidelines and Best Practices

## File Structure

ADRs are typically stored in a dedicated directory at the project root (commonly `adr/` but can be customized) with this structure:

```
{adr_location}/
├── README.md          # Index and documentation
├── _template.md       # Template for new ADRs
├── 0001-title.md     # Individual ADRs
├── 0002-title.md
└── ...
```

## Naming Convention

ADRs follow the naming pattern:

```
NNNN-<kebab-case-title>.md
```

Where:
- `NNNN` is a 4-digit sequence number (0001, 0002, etc.)
- `<kebab-case-title>` is a short, descriptive title

Examples:
- `0001-use-adr-system.md`
- `0002-adopt-express-mode.md`
- `0003-vendor-bslib-assets.md`

## ADR Status Lifecycle

```
proposed → accepted → [deprecated | superseded]
    ↓
 rejected
```

- **proposed**: Initial state, under review
- **accepted**: Decision approved and in effect
- **rejected**: Decision not approved
- **deprecated**: Decision no longer relevant
- **superseded**: Replaced by a newer ADR (link to the new one)

## When to Write an ADR

Write an ADR when:

- Adding a new major feature or component
- Changing existing architectural patterns
- Making technology or dependency choices
- Establishing new conventions or standards
- Deprecating or removing significant functionality

You probably don't need an ADR for:

- Bug fixes
- Minor refactoring
- Documentation updates
- Routine dependency updates

## Index Management

Always update `{adr_location}/README.md` when creating a new ADR. Add an entry under the Index section:

```markdown
## Index

- [ADR-0001: Use ADR System](0001-use-adr-system.md) - Adopt MADR format for documenting decisions
- [ADR-0002: Adopt Express Mode](0002-adopt-express-mode.md) - Simplify single-file Shiny apps
```

The format is: `- [ADR-NNNN: Title](NNNN-title.md) - One-line summary`

## Template Placeholder Replacement

When generating any ADR, replace ALL bracketed placeholders in the MADR template with actual content:

**Header section:**
- `[short title of solved problem and solution]` → Actual ADR title
- `[proposed | rejected | ...]` → Actual status (proposed, accepted, rejected, deprecated, superseded)
- `[list everyone involved in the decision]` → Comma-separated list of decider names
- `[YYYY-MM-DD when the decision was last updated]` → Today's date or decision date
- `[description | ticket/issue URL]` → Technical story text or issue link

**Body sections:**
- `[Describe the context...]` → Actual context description
- `[driver 1, e.g., a force, facing concern, …]` → Actual decision drivers
- `[option 1]`, `[option 2]`, etc. → Actual option names
- `[justification...]` → Actual justification for chosen option
- `[e.g., improvement of quality attribute...]` → Actual consequences
- `[example | description | pointer to more information | …]` → Actual option description
- `[argument a]`, `[argument b]`, etc. → Actual pros/cons

**General rules:**
- Remove ALL square brackets
- Remove HTML comments like `<!-- optional -->`
- For optional sections with no content: use "N/A" or remove the section entirely
- Ensure the "## Pros and Cons of the Options" section has a `### [Option Name]` subsection for each alternative with its specific pros/cons listed as bullet points

## Important Rules

1. **ALWAYS read the project's ADR template** (`{adr_location}/_template.md`) if it exists before creating new ADRs
2. **ALWAYS update the index** in `{adr_location}/README.md` when creating new ADRs
3. **ALWAYS use kebab-case** for ADR filenames
4. **ALWAYS set today's date** in YYYY-MM-DD format
5. **ALWAYS replace template placeholders** with actual content (including removing brackets and HTML comments)
6. **NEVER skip the template structure** - all sections should be present even if brief
7. **ALWAYS link related issues/PRs** if they exist
8. **ALWAYS ask clarifying questions** if information is missing rather than guessing
9. **ALWAYS show the user the file content** using the Read tool before considering the ADR finalized

## Error Handling and Edge Cases

**No ADR directory exists or is empty:**
1. Ask user: "I don't see any existing ADRs in `adr/`. Is there a different location where ADRs are stored in this project, or should I initialize the ADR system in `adr/`?"
2. If user provides different location, use that location (`{adr_location}`) for all subsequent operations
3. If user wants initialization, request consent: "I'll create the directory, README.md, and _template.md. Proceed?"
4. If yes, create:
   - Directory at specified location
   - README.md using the structure from `references/README-example.md`
   - _template.md copying content from `references/_template.md`

**No template found at `{adr_location}/_template.md`:**
Use the MADR template from skill's `references/_template.md` as fallback.

**README.md doesn't exist:**
Create one using the structure from `references/README-example.md`.

**README.md exists but no Index section:**
Add "## Index" section at the end of the file (before any "Contributing" or "License" sections if they exist) with the new ADR entry.

**Duplicate ADR number:**
Check if `NNNN-*.md` already exists. If yes, increment to next available number. Use glob pattern `[0-9][0-9][0-9][0-9]-*.md` to match only 4-digit numbered ADRs.

**Title validation failures:**
- Not kebab-case: Suggest converting (e.g., "Use TypeScript" → "use-typescript")
- Too long (>50 chars): Ask user to shorten
- Already exists: Suggest alternative title

**Not a git repository:**
Use current working directory as the base path for ADR location.

**Unclear or missing information:**
Don't guess - always ask the user for clarification. It's better to have an incomplete ADR that's accurate than a complete one with assumptions.
