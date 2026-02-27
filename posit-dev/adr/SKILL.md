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

**Detailed interview script**: See `references/interview-flow.md` for the complete phase-by-phase interview questions and workflow.

#### High-Level Workflow

1. **Conduct structured interview** (7 phases covering context, alternatives, outcome, and consequences)
   - See `references/interview-flow.md` for complete question script

2. **Setup ADR system** (see "Common Setup Steps")

3. **Synthesize answers into ADR format**
   - Map interview responses to MADR sections
   - Set status to "accepted" (past decisions already in effect)

4. **Generate and present the ADR** (see "Common Generation Steps")

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

## Guidelines and Best Practices

For complete guidelines including:
- File structure and naming conventions
- ADR status lifecycle
- When to write an ADR
- Template placeholder replacement rules
- Important rules to follow
- Error handling and edge cases

See `references/guidelines.md`

**Key reminders:**
- Always use kebab-case for filenames (e.g., `0001-use-typescript.md`)
- Always update the index in README.md
- Always ask clarifying questions rather than guessing
- Always show the user the file content using Read tool before finalizing

## Reference Files

The skill includes reference files in the `references/` directory:
- `_template.md` - Official MADR template (fallback if project has none)
- `README-example.md` - Example README structure for initializing new ADR directories
- `example-adr.md` - Fully worked example ADR showing proper MADR structure and content
- `guidelines.md` - Complete ADR guidelines, naming conventions, template placeholders, and error handling
- `interview-flow.md` - Detailed interview script with all phases and questions for Flow C
