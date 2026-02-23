---
name: create-adr
description: Architecture Decision Records (ADR) management. Creates, documents, and manages ADRs using the MADR format. Use when the user says "create adr", "document decision", "make an adr", or wants to formally capture architectural decisions. Supports three modes - creating from a plan, converting an active plan, or interviewing for past decisions.
compatibility: Designed for Claude Code
metadata:
  author: Posit
  version: "1.0"
license: MIT
---

# Architecture Decision Records (ADR) Skill

This skill helps create and manage Architecture Decision Records (ADRs) using the MADR (Markdown Any Decision Record) format. ADRs document important architectural decisions with their context, alternatives considered, and consequences.

## Available Commands

This skill provides three slash commands for different ADR creation scenarios:

| Command | When to Use | Description |
|---------|-------------|-------------|
| `/adr-create` | You have a plan to document | Create an ADR from a plan provided by the user |
| `/adr-from-current` | Claude has an active plan | Convert Claude's current working plan into an ADR |
| `/adr-interview` | Documenting a past decision | Interactive interview to capture a decision already made |

## Command: /adr-create

Create an Architecture Decision Record from a plan provided by the user.

### Workflow

1. **Determine repository root and ADR location**

   - Find the git repository root using `git rev-parse --show-toplevel`
   - If not a git repo, use the current working directory
   - Check if `adr/` directory exists at this location
   - If `adr/` doesn't exist or is empty, ask: "I don't see any existing ADRs in `adr/`. Is there a different location where ADRs are stored in this project, or should I initialize the ADR system in `adr/`?"
   - Store the confirmed ADR location for use in subsequent steps

2. **Initialize ADR system if needed**

   If the user wants to initialize in a new location, ask for consent: "I'll initialize the ADR system by creating:
   - `{location}/` directory
   - `{location}/README.md` with documentation
   - `{location}/_template.md` with the MADR template

   Should I proceed?"

   If yes:
   - Create the directory
   - Copy README from skill's `references/README-example.md` (customize with project name)
   - Copy template from skill's `references/_template.md`

3. **Get the plan from the user**

   Ask the user: "Please describe the decision or plan you want to document as an ADR. Include:
   - What problem are you solving?
   - What options did you consider?
   - What did you decide and why?"

4. **Read the template**

   Read `{adr_location}/_template.md` to understand the expected format.
   If not found, use the template from skill's `references/_template.md`.

5. **Determine the next ADR number**

   - List existing ADRs in the confirmed location
   - Find files matching pattern `NNNN-*.md`
   - Check that the next number doesn't already exist (validation)
   - If no ADRs exist, use `0001`
   - Otherwise, increment from the highest existing number

6. **Extract information from the plan**

   From the user's input, identify and map to ADR sections:

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

7. **Validate and fill in any gaps**

   Validate the title:
   - Check it's in kebab-case format
   - Check it's under 50 characters
   - Check the filename `NNNN-{title}.md` doesn't already exist

   If the user's plan is missing information, ask clarifying questions:
   - "Who are the deciders for this decision?"
   - "What alternatives did you consider besides [chosen option]?"
   - "What are the potential downsides of this approach?"

8. **Generate the ADR**

   Create the ADR file at `{adr_location}/NNNN-<kebab-case-title>.md` using the template.

   Set the status to "proposed" unless the user indicates it's already accepted.

9. **Update the index**

   - Read `{adr_location}/README.md`
   - If README doesn't exist, create one using `references/README-example.md` as template
   - Find the "## Index" section
   - If Index section doesn't exist, add it at the end
   - Add entry: `- [ADR-NNNN: Title](NNNN-title.md) - Brief description`
   - Check for duplicate entries before adding
   - Write the updated README

10. **Present the result**

    Show the user the full created ADR file content and ask if any changes are needed.

### Example Interaction

**User**: I want to document our decision to use MADR format for ADRs.

**Claude**: I'll create an ADR for that. Let me gather some details:
- Who should be listed as deciders?
- What other formats did you consider (e.g., Y-statements, Nygard format)?
- What drove the decision to choose MADR?

**User**: The team decided. We considered plain markdown and Y-statements. MADR was chosen for its comprehensive structure and wide adoption.

**Claude**: *Creates `adr/0001-use-madr-format-for-adrs.md`*

### Notes

- Always use kebab-case for the filename
- Set today's date in YYYY-MM-DD format
- Link to relevant GitHub issues if mentioned
- Keep the title concise (under 50 characters ideally)

## Command: /adr-from-current

Convert Claude's currently active plan (PLAN.md or todo list) into an Architecture Decision Record.

### Workflow

1. **Determine repository root and ADR location**

   - Find the git repository root using `git rev-parse --show-toplevel`
   - If not a git repo, use the current working directory
   - Check if `adr/` directory exists at this location
   - If `adr/` doesn't exist or is empty, ask about location (same as `/adr-create`)
   - Initialize if needed (with user consent)

2. **Locate the current plan**

   Check for an active plan in these locations (in order):
   - `PLAN.md` in the repository root
   - Active todo list from the current session
   - Recent planning discussion in the conversation

   If no plan is found, inform the user and suggest using `/adr-create` or `/adr-interview` instead.

3. **Read the template**

   Read `{adr_location}/_template.md` to understand the expected format.
   If not found, use the template from skill's `references/_template.md`.

4. **Determine the next ADR number**

   - List existing ADRs in the confirmed location
   - Validate the next number doesn't already exist
   - Use `0001` if no ADRs exist, otherwise increment from highest

5. **Analyze the plan**

   Extract from the current plan:
   - **Problem Statement**: What issue is the plan addressing?
   - **Proposed Solution**: What approach does the plan take?
   - **Implementation Steps**: These often reveal decision drivers
   - **Alternatives**: Any options mentioned or implied

6. **Transform into ADR format**

   Map plan elements to ADR sections:

   | Plan Element | → | ADR Section |
   |--------------|---|-------------|
   | Plan title | → | Title (concise, use kebab-case for filename) |
   | Overview/why this is needed | → | Context and Problem Statement |
   | Goals/requirements mentioned | → | Decision Drivers |
   | Implementation approach | → | Decision Outcome (the "what", not the "how") |
   | Alternative approaches mentioned | → | Considered Options |
   | Benefits/rationale | → | Positive Consequences |
   | Trade-offs/concerns | → | Negative Consequences |
   | Related issues/PRs | → | Technical Story + Links section |

   **Key transformation principle**: Plans describe "how to implement", ADRs describe "what we decided and why".

7. **Validate and fill gaps with the user**

   Validate the title (kebab-case, under 50 chars, no duplicate filename).

   Plans often lack some ADR elements. Ask the user:
   - "What alternatives did you consider before this plan?"
   - "Who should be listed as deciders?"
   - "What are the potential downsides of this approach?"

   **Status determination**:
   - If the plan is actively being implemented → status is "accepted"
   - If the plan is awaiting approval → status is "proposed"
   - If unclear, ask: "Is this decision already approved, or awaiting review?"

8. **Generate the ADR**

   Create `{adr_location}/NNNN-<title>.md` based on the transformed plan.

9. **Update the index**

   Update `{adr_location}/README.md` with the new ADR entry (create README if needed).

10. **Present the result**

    Show the user the full created ADR file content.

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

## Command: /adr-interview

Guide the user through an interactive interview to document a past architectural decision.

### Purpose

Sometimes decisions were made in the past without formal documentation. This command helps retroactively capture those decisions through a structured conversation.

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

Then move to the next option.

If they only mention one option: "Was there ever any discussion of doing it differently? Even approaches that were quickly dismissed?"

#### Phase 4: Understand the Decision

**Question 6**: "Which option did you ultimately choose?"

**Question 7**: "What were the main reasons for choosing this approach over the others?"

#### Phase 5: Capture Real-World Consequences

Now that we've covered the theoretical pros/cons of each option, capture the actual outcomes:

**Question 8**: "Now that this decision has been in place, what positive outcomes have you observed? How has it helped?"

**Question 9**: "Have there been any negative consequences or challenges that resulted from this choice?"

**Question 10**: "Were there any unexpected trade-offs or surprises - things you didn't anticipate when making the decision?"

**Question 11**: "If you were making this decision again today, would you decide differently? Why or why not?"

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
   - Map interview responses to MADR sections

5. **Create the file at `{adr_location}/NNNN-<title>.md`**

6. **Update index**
   - Update or create `{adr_location}/README.md` with new entry

**Present the draft**: "Here's the ADR I've created based on our conversation. Please review it:"

*Show the full ADR file content*

**Ask**: "Would you like me to make any changes before we finalize it?"

#### Phase 7: Finalize

After any revisions:
- Save the final ADR
- Set status to "accepted" (since this is a past decision already in effect)
- Confirm: "ADR created at `adr/NNNN-title.md`. The decision has been documented!"

### Interview Tips

- **Be patient**: Let the user think and recall details
- **Probe gently**: If answers are vague, ask follow-up questions
- **Validate understanding**: Summarize back to confirm accuracy
- **Accept uncertainty**: "I don't remember" is a valid answer
- **Note gaps**: If information is missing, note it in the ADR

### Notes

- Past decisions should typically have status "accepted"
- If a decision has since been reversed, note it as "superseded" or "deprecated"
- Link to any related PRs or issues if the user can recall them
- It's okay to have some sections less detailed for older decisions

## General ADR Guidelines

### File Structure

ADRs should be stored in an `adr/` directory at the project root with this structure:

```
adr/
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

Always update `adr/README.md` when creating a new ADR. Add an entry under the Index section:

```markdown
## Index

- [ADR-0001: Use ADR System](0001-use-adr-system.md) - Adopt MADR format for documenting decisions
- [ADR-0002: Adopt Express Mode](0002-adopt-express-mode.md) - Simplify single-file Shiny apps
```

## Important Rules

1. **ALWAYS read the project's ADR template** (`adr/_template.md`) if it exists before creating new ADRs
2. **ALWAYS update the index** in `adr/README.md` when creating new ADRs
3. **ALWAYS use kebab-case** for ADR filenames
4. **ALWAYS set today's date** in YYYY-MM-DD format
5. **NEVER skip the template structure** - all sections should be present even if brief
6. **ALWAYS link related issues/PRs** if they exist
7. **ALWAYS ask clarifying questions** if information is missing rather than guessing
8. **ALWAYS show the user the draft** before finalizing

## Error Handling and Edge Cases

**No `adr/` directory exists or is empty:**
1. Ask user: "I don't see any existing ADRs in `adr/`. Is there a different location where ADRs are stored in this project, or should I initialize the ADR system in `adr/`?"
2. If user provides different location, use that location for all operations
3. If user wants initialization, request consent: "I'll create the directory, README.md, and _template.md. Proceed?"
4. If yes, create:
   - Directory at specified location
   - README.md using `references/README-example.md` as template
   - _template.md copying from `references/_template.md`

**No template found at `{adr_location}/_template.md`:**
Use the MADR template from skill's `references/_template.md` as fallback.

**README.md doesn't exist:**
Create one using `references/README-example.md`, customizing the project name if detectable.

**README.md exists but no Index section:**
Add "## Index" section at the end with the new ADR entry.

**Duplicate ADR number:**
Check if `NNNN-*.md` already exists. If yes, increment to next available number.

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
- `_template.md` - Official MADR template (fallback if project has none)
- `README-example.md` - Template for creating new ADR directories
- `example-adr.md` - Fully worked example showing proper ADR structure
