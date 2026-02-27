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

All three workflows share standard procedures for setup, validation, and generation. See `references/common-steps.md` for complete details on:
- **Setup**: Determining ADR location, initializing system, reading template, numbering
- **Validation**: Title format, length, and duplicate checking
- **Generation**: Creating ADR file, updating index, presenting results

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
- `common-steps.md` - Standard setup, validation, and generation procedures used across all workflows
- `guidelines.md` - Complete ADR guidelines, naming conventions, template placeholders, and error handling
- `interview-flow.md` - Detailed interview script with all phases and questions for Flow C
