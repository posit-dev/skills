---
name: adr
description: Architecture Decision Records (ADR) management. Creates, documents, and manages ADRs using the MADR format. Use when the user says "create adr", "document decision", "make an adr", or wants to formally capture architectural decisions. Intelligently routes between three workflows - converting an active plan, creating from a user-provided plan or description, or conducting an interview for past decisions.
compatibility: Designed for Claude Code
metadata:
  author: Posit
  version: "1.0"
license: MIT
---

# Architecture Decision Records (ADR) Skill

This skill helps create and manage Architecture Decision Records (ADRs) using the MADR (Markdown Any Decision Record) format. ADRs document important architectural decisions with their context, alternatives considered, and consequences.

## Command: /adr

This skill provides a single `/adr` command that intelligently routes to the appropriate workflow based on the situation.

### Initial Routing Logic

When `/adr` is invoked:

1. **Check for active plan**: Look for Claude's current working plan (PLAN.md, active todo list, or recent planning discussion in conversation)

2. **Determine the scenario** and route accordingly:

   **Scenario A - Active Plan Exists**: If an active plan is detected → **Route to "Convert Current Plan" flow**

   **Scenario B - User Provides Context**: If no active plan but user mentions a decision/plan → **Route to "Create from Plan" flow**

   **Scenario C - Need More Information**: If neither applies → **Ask routing question**

3. **Routing Question** (when needed):

   "I'll help you create an ADR. Which scenario best describes what you need?

   1. **Document a plan or decision** - You have details about a decision to document
   2. **Interview me about a past decision** - Walk me through questions to capture a decision that was already made

   Which would you prefer?"

   - If user chooses option 1 → Route to "Create from Plan" flow
   - If user chooses option 2 → Route to "Interview" flow

### Flow A: Convert Current Plan

Convert Claude's currently active plan (PLAN.md or todo list) into an Architecture Decision Record.

**When to use**: Detected active plan in the conversation or project files.

#### Workflow

1. **Setup ADR System** (see "Common Setup Steps" section below)
   - Determine repository root and ADR location
   - Initialize if needed (with user consent)

2. **Locate the current plan**

   Check for an active plan in these locations (in order):
   - `PLAN.md` in the repository root
   - Active todo list from the current session
   - Recent planning discussion in the conversation

   If no plan is found, inform the user: "I don't see an active plan in this conversation. Would you like to:
   1. Provide a plan or describe a decision (I'll use the 'Create from Plan' flow)
   2. Walk through an interview about a past decision?"

   Route to the appropriate flow based on their choice.

3. **Read template and determine ADR number** (see "Common Setup Steps")

4. **Analyze the plan**

   Extract from the current plan:
   - **Problem Statement**: What issue is the plan addressing?
   - **Proposed Solution**: What approach does the plan take?
   - **Implementation Steps**: These often reveal decision drivers
   - **Alternatives**: Any options mentioned or implied

5. **Transform plan into ADR format**

   Plans often lack some ADR elements. Ask the user:
   - "What alternatives did you consider before this plan?"
   - "Who should be listed as deciders?"
   - "What are the potential downsides of this approach?"

   **Status determination**:
   - If the plan is actively being implemented → status is "accepted"
   - If the plan is awaiting approval → status is "proposed"
   - If unclear, ask: "Is this decision already approved, or awaiting review?"

7. **Generate and present the ADR** (see "Common Generation Steps")

8. **Handle the plan file**

    Ask the user: "The plan has been converted to ADR. Would you like me to:
    - Keep PLAN.md as-is (for continued implementation tracking)
    - Delete PLAN.md (if implementation is complete)
    - Archive PLAN.md somewhere else"

### Example Interaction

**User**: I want to document our decision to use MADR format for ADRs.

**Claude**: I'll create an ADR for that. Do you have a plan document or file I should read, or would you prefer to describe the decision directly?

**User**: Describe it directly.

**Claude**: Please describe the decision or plan you want to document as an ADR. Include:
- What problem are you solving?
- What options did you consider?
- What did you decide and why?

**User**: We needed a way to document architectural decisions. We considered Y-statements, plain markdown, and MADR. We chose MADR for its comprehensive structure.

**Claude**: Let me gather some more details:
- Who should be listed as deciders?
- For each option you considered, can you tell me the pros and cons?

**User**: The core team decided. Y-statements were concise but lacked detail. Plain markdown was flexible but inconsistent. MADR was comprehensive and well-documented.

**Claude**: *Creates `adr/0001-use-madr-format-for-adrs.md` and updates README*

*Uses Read tool to show:*
```markdown
# Use MADR Format for ADRs

* Status: proposed
* Deciders: Core team
* Date: 2026-02-23
...
```

Would you like me to make any changes to this ADR?

### Notes

- Always use kebab-case for the filename
- Set today's date in YYYY-MM-DD format
- Link to relevant GitHub issues if mentioned
- Keep the title concise (under 50 characters ideally)

### Flow B: Create from Plan

Create an Architecture Decision Record from a plan or decision description provided by the user.

**When to use**: User has a plan document or wants to describe a decision directly.

#### Workflow

1. **Setup ADR System** (see "Common Setup Steps" section below)

2. **Get the plan from the user**

   Ask: "Do you have a plan document or file I should read, or would you prefer to describe the decision directly?"

   If user provides a filename:
   - Read the file
   - Extract as much information as possible from the file content

   If no file or if file doesn't contain complete information, ask: "Please describe the decision or plan you want to document as an ADR. Include:
   - What problem are you solving?
   - What options did you consider?
   - What did you decide and why?"

3. **Read template and determine ADR number** (see "Common Setup Steps")

4. **Extract information from the plan**

   Map user's information to ADR sections:

   | User's Plan Info | → | ADR Section |
   |------------------|---|-------------|
   | Decision name | → | Title (concise, use kebab-case for filename) |
   | Situation/problem | → | Context and Problem Statement |
   | Requirements/constraints | → | Decision Drivers |
   | Alternatives considered | → | Considered Options |
   | Chosen approach | → | Decision Outcome |
   | Why this was chosen | → | Decision Outcome justification |
   | Benefits | → | Positive Consequences |
   | Drawbacks/risks | → | Negative Consequences |
   | Related issues/PRs | → | Technical Story + Links section |

5. **Validate and fill gaps** (see "Common Validation Steps")

   Ask clarifying questions if needed:
   - "Who are the deciders for this decision?"
   - "For each option, what were the pros and cons?"
   - "What are the potential downsides of this approach?"

6. **Generate and present the ADR** (see "Common Generation Steps")

   Create `{adr_location}/NNNN-<title>.md` based on the transformed plan.

   Replace template placeholders with actual content (see "Template Placeholder Replacement" section above for complete details).

9. **Update the index**

   Update `{adr_location}/README.md` with the new ADR entry (create README using `references/README-example.md` structure if needed).

   Add entry at the end: `- [ADR-NNNN: Title](NNNN-title.md) - One-line summary`

10. **Present the result**

    Use the Read tool to show the user the full created ADR file content.

11. **Handle the plan file**

    Ask the user: "The plan has been converted to ADR. Would you like me to:
    - Keep PLAN.md as-is (for continued implementation tracking)
    - Delete PLAN.md (if implementation is complete)
    - Archive PLAN.md somewhere else"

### Example

Given a `PLAN.md` like:

```markdown
# Add Reactive Polling to File Watcher

## Overview
Implement reactive polling for file system changes in Shiny apps.

## Implementation
1. Add watchdog dependency for file system events
2. Create reactive poll wrapper
3. Integrate with reactive graph
4. Add examples showing auto-reload patterns
```

Claude would:
1. Identify the problem: need reactive file system monitoring
2. Identify the decision: use watchdog library with reactive polling
3. Ask about alternatives considered (OS-native watchers, manual polling, etc.)
4. Generate an ADR capturing the file watching decision

### Notes

- The plan likely contains implementation details not needed in the ADR
- Focus on extracting the "why" and "what" rather than "how"
- ADRs are about decisions, plans are about execution
- Keep the ADR focused on the architectural choice, not implementation steps

### Flow C: Interview for Past Decision

Guide the user through an interactive interview to document a past architectural decision.

**When to use**: User wants to document a decision that was already made in the past.

**Purpose**: Sometimes decisions were made in the past without formal documentation. This flow helps retroactively capture those decisions through a structured conversation.

### Interview Flow

#### Phase 1: Set the Stage

Start with: "I'll help you document a past architectural decision as an ADR. Let's start with the basics."

**Question 1**: "What decision would you like to document? Give me a brief title or description."

*Wait for response before continuing.*

#### Phase 2: Understand the Context

**Question 2**: "When was this decision made? (Approximate date is fine)"

**Question 3**: "Who was involved in making this decision?"

**Question 4**: "What was the situation that led to needing this decision? What problem were you trying to solve?"

*Summarize back*: "So if I understand correctly, [summary of context]. Is that right?"

#### Phase 3: Explore Alternatives and Their Trade-offs

**Question 5**: "What options did you consider? Even briefly considered or rejected ideas count."

*Wait for response listing options.*

For each option mentioned, **immediately** ask:
- "Tell me about [option] - what were the pros?"
- "What were the cons or concerns about [option]?"
- *Summarize*: "So [option] was good for [pros] but had issues with [cons]. Is that right?"

**Note:** Store each option with its associated pros/cons. In Phase 6, these will map to individual option blocks in the "## Pros and Cons of the Options" section. Each option gets its own subsection with its specific good/bad points.

Then move to the next option.

If they only mention one option: "Was there ever any discussion of doing it differently? Even approaches that were quickly dismissed?"

**Handling many options:** If user lists 5+ options, continue through all of them systematically.
**Handling unclear memory:** If user can't remember details for some options, note what they do know and move on.
**Handling informal evaluation:** If options weren't formally evaluated, ask for their thoughts anyway and capture what they recall.

#### Phase 4: Understand the Decision Outcome

**Question 6**: "Which option did you ultimately choose?"

**Question 7**: "What were the main reasons for choosing this approach over the others?"

**Question 8**: "What was the expected outcome or goal when you made this decision? What were you hoping to achieve?"

#### Phase 5: Capture Real-World Consequences

Now that we've covered the options, their pros/cons, and the expected outcome, capture what actually happened:

**Question 9**: "Now that this decision has been in place, what positive outcomes have you observed? How has it helped?"

**Question 10**: "Have there been any negative consequences or challenges that resulted from this choice?"

**Question 11**: "Were there any unexpected trade-offs or surprises - things you didn't anticipate when making the decision?"

**Question 12**: "If you were making this decision again today, would you decide differently? Why or why not?"

#### Phase 6: Generate the ADR

1. **Determine repository root and ADR location**
   - Find git repo root or use working directory
   - Check for ADR location, initialize if needed (with consent)

2. **Read template**
   - Read `{adr_location}/_template.md` or use `references/_template.md`

3. **Determine and validate ADR number**
   - List existing ADRs, validate next number, use `0001` if none exist

4. **Synthesize interview answers into ADR format**
   - Validate title (kebab-case, under 50 chars, no duplicate)
   - Map interview responses to MADR sections:
     - Phase 1 (decision title) + Phase 2 (problem context) → Context and Problem Statement
     - Phase 2 (when decided) → Date
     - Phase 2 (who decided) → Deciders (comma-separated)
     - Phase 3 (options list) → Considered Options
     - Phase 3 (pros/cons for each option) → Pros and Cons of the Options (create subsection for each option with its specific good/bad points)
     - Phase 4 (chosen option, reasons, expected outcome) → Decision Outcome
     - Phase 5 (positive outcomes observed) → Positive Consequences
     - Phase 5 (negative outcomes, unexpected surprises) → Negative Consequences
   - Replace all template placeholders with actual content
   - For optional sections with no content: use "N/A" or remove if truly not applicable
   - Remove HTML comments

5. **Create and save the initial ADR file at `{adr_location}/NNNN-<title>.md`**

6. **Update index**
   - Update or create `{adr_location}/README.md` with new entry at the end
   - Entry format: `- [ADR-NNNN: Title](NNNN-title.md) - One-line summary`

**Present the draft**: "Here's the ADR I've created based on our conversation. Please review it:"

*Use the Read tool to show the full ADR file content*

**Ask**: "Would you like me to make any changes before we finalize it?"

#### Phase 7: Finalize

If user requests changes:
- Make the requested edits to the ADR file
- Save the updated version
- Show the updated content again if changes were substantial

After any revisions (or if no changes requested):
- Ensure status is set to "accepted" (since this is a past decision already in effect)
- Confirm: "ADR created at `{adr_location}/NNNN-title.md`. The decision has been documented!"

### Interview Tips

- **Be patient**: Let the user think and recall details
- **Probe gently**: If answers are vague, ask follow-up questions
- **Validate understanding**: Summarize back to confirm accuracy
- **Accept uncertainty**: "I don't remember" is a valid answer
- **Note gaps**: If information is missing, note it in the ADR

### Notes

- Past decisions (documented via interview) should have status "accepted" since they're already in effect
- If a decision has since been reversed, set status to "superseded" or "deprecated" instead
- Link to any related PRs or issues if the user can recall them
- It's okay to have some sections less detailed for older decisions

## Common Steps (Shared Across All Flows)

### Common Setup Steps

**Determine repository root and ADR location:**
1. Find the git repository root using `git rev-parse --show-toplevel`
2. If not a git repo, use the current working directory
3. Check if `adr/` directory exists at this location
4. If `adr/` doesn't exist or is empty, ask: "I don't see any existing ADRs in `adr/`. Is there a different location where ADRs are stored in this project, or should I initialize the ADR system in `adr/`?"
5. Store the confirmed ADR location as `{adr_location}` for use in subsequent steps

**Initialize ADR system if needed:**
If the user wants to initialize in a new location, ask for consent: "I'll initialize the ADR system by creating:
- `{adr_location}/` directory
- `{adr_location}/README.md` with documentation
- `{adr_location}/_template.md` with the MADR template

Should I proceed?"

If yes:
- Create the directory
- Create `{adr_location}/README.md` using the structure from skill's `references/README-example.md`
- Create `{adr_location}/_template.md` copying content from skill's `references/_template.md`

**Read the template:**
Read `{adr_location}/_template.md` to understand the expected format. If not found, use the template from skill's `references/_template.md`.

**Determine the next ADR number:**
- List existing ADRs in the confirmed location
- Find files matching pattern `[0-9][0-9][0-9][0-9]-*.md` (excludes _template.md, README.md)
- If no ADRs exist, use `0001`
- Otherwise, increment from the highest existing number

### Common Validation Steps

**Validate title:**
- Check it's in kebab-case format (e.g., "use-typescript" not "Use TypeScript")
- Check it's under 50 characters
- Check if filename `NNNN-{title}.md` already exists in `{adr_location}` (prevent duplicates)
- If validation fails, ask user to provide a corrected title

### Common Generation Steps

**Generate the ADR file:**
1. Create the ADR file at `{adr_location}/NNNN-<kebab-case-title>.md` using the template
2. Replace ALL template placeholders with actual content (see "Template Placeholder Replacement" section)
3. Set today's date in YYYY-MM-DD format
4. Use comma-separated decider names as provided by user
5. Ensure "## Pros and Cons of the Options" section has subsections for each option with their specific pros/cons

**Update the index:**
1. Read `{adr_location}/README.md`
2. If README doesn't exist, create one using the structure from `references/README-example.md`
3. Find the "## Index" section
4. If Index section doesn't exist, add it at the end of the README (before any "Contributing" or "License" sections if they exist)
5. Generate one-line summary from the Decision Outcome section
6. Add entry format: `- [ADR-NNNN: Title](NNNN-title.md) - One-line summary`
7. Check for duplicate entries before adding
8. Write the updated README

**Present the result:**
Use the Read tool to show the user the full created ADR file content and ask if any changes are needed.

## General ADR Guidelines

### File Structure

ADRs are typically stored in a dedicated directory at the project root (commonly `adr/` but can be customized) with this structure:

```
{adr_location}/
├── README.md          # Index and documentation
├── _template.md       # Template for new ADRs
├── 0001-title.md     # Individual ADRs
├── 0002-title.md
└── ...
```

### Naming Convention

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

### ADR Status Lifecycle

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

### When to Write an ADR

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

### Index Management

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

## Reference Files

The skill includes reference files in the `references/` directory:
- `_template.md` - Official MADR template from joelparkerhenderson/architecture-decision-record (fallback if project has none)
- `README-example.md` - Example README structure for initializing new ADR directories
- `example-adr.md` - Fully worked example ADR showing proper MADR structure and content
