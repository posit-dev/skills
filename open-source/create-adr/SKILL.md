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

1. **Get the plan from the user**

   Ask the user: "Please describe the decision or plan you want to document as an ADR. Include:
   - What problem are you solving?
   - What options did you consider?
   - What did you decide and why?"

2. **Read the template**

   Read `adr/_template.md` to understand the expected format.

3. **Determine the next ADR number**

   List existing ADRs in `adr/` and find the next sequence number:
   - If no ADRs exist, use `0001`
   - Otherwise, increment from the highest existing number

4. **Extract information from the plan**

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

5. **Fill in any gaps**

   If the user's plan is missing information, ask clarifying questions:
   - "Who are the deciders for this decision?"
   - "What alternatives did you consider besides [chosen option]?"
   - "What are the potential downsides of this approach?"

6. **Generate the ADR**

   Create the ADR file at `adr/NNNN-<kebab-case-title>.md` using the template.

   Set the status to "proposed" unless the user indicates it's already accepted.

7. **Update the index**

   Add a link to the new ADR in `adr/README.md` under the Index section.

8. **Present the result**

   Show the user the created ADR and ask if any changes are needed.

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

1. **Locate the current plan**

   Check for an active plan in these locations (in order):
   - `PLAN.md` in the repository root
   - Active todo list from the current session
   - Recent planning discussion in the conversation

   If no plan is found, inform the user and suggest using `/adr-create` or `/adr-interview` instead.

2. **Read the template**

   Read `adr/_template.md` to understand the expected format.

3. **Determine the next ADR number**

   List existing ADRs in `adr/` and find the next sequence number.

4. **Analyze the plan**

   Extract from the current plan:
   - **Problem Statement**: What issue is the plan addressing?
   - **Proposed Solution**: What approach does the plan take?
   - **Implementation Steps**: These often reveal decision drivers
   - **Alternatives**: Any options mentioned or implied

5. **Transform into ADR format**

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

6. **Fill gaps with the user**

   Plans often lack some ADR elements. Ask the user:
   - "What alternatives did you consider before this plan?"
   - "Who should be listed as deciders?"
   - "What are the potential downsides of this approach?"

   **Status determination**:
   - If the plan is actively being implemented → status is "accepted"
   - If the plan is awaiting approval → status is "proposed"
   - If unclear, ask: "Is this decision already approved, or awaiting review?"

7. **Generate the ADR**

   Create `adr/NNNN-<title>.md` based on the transformed plan.

8. **Handle the plan file**

   Ask the user: "The plan has been converted to ADR. Would you like me to:
   - Keep PLAN.md as-is (for continued implementation tracking)
   - Delete PLAN.md (if implementation is complete)
   - Archive PLAN.md somewhere else"

9. **Update the index**

   Add a link to the new ADR in `adr/README.md`.

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

#### Phase 3: Explore Alternatives

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

**Question 7**: "What were the main reasons for choosing this approach?"

**Question 8**: "Were there any trade-offs you accepted? Things you gave up or risks you took on?"

#### Phase 5: Capture Consequences

**Question 9**: "Looking back, what were the positive outcomes of this decision?"

**Question 10**: "Were there any negative consequences or challenges that resulted?"

**Question 11**: "If you were making this decision again today, would you decide differently? Why or why not?"

#### Phase 6: Generate the ADR

1. Read `adr/_template.md`
2. Determine the next ADR number from `adr/`
3. Synthesize interview answers into ADR format
4. Create the file at `adr/NNNN-<title>.md`
5. Update `adr/README.md` index

**Present the draft**: "Here's the ADR I've created based on our conversation. Please review it:"

*Show the full ADR content*

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

## Error Handling

**No `adr/` directory exists:**
Inform the user and ask if they want to initialize an ADR system:
- Create `adr/` directory
- Create `adr/README.md` with documentation
- Create `adr/_template.md` with the MADR template
- Then proceed with ADR creation

**No template found:**
Use a standard MADR template as a fallback.

**Unclear information:**
Don't guess - always ask the user for clarification. It's better to have an incomplete ADR that's accurate than a complete one with assumptions.

## Reference Files

The skill includes reference files in the `resources/` directory with detailed workflows for each command:
- `adr-create.md` - Creating ADRs from user plans
- `adr-from-current.md` - Converting active plans to ADRs
- `adr-interview.md` - Interactive interview for past decisions
