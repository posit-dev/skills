# Interview Flow for Past Decisions

This document provides the detailed interview script for capturing past architectural decisions.

## Phase 1: Set the Stage

Start with: "I'll help you document a past architectural decision as an ADR. Let's start with the basics."

**Question 1**: "What decision would you like to document? Give me a brief title or description."

*Wait for response before continuing.*

## Phase 2: Understand the Context

**Question 2**: "When was this decision made? (Approximate date is fine)"

**Question 3**: "Who was involved in making this decision?"

**Question 4**: "What was the situation that led to needing this decision? What problem were you trying to solve?"

*Summarize back*: "So if I understand correctly, [summary of context]. Is that right?"

## Phase 3: Explore Alternatives and Their Trade-offs

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

## Phase 4: Understand the Decision Outcome

**Question 6**: "Which option did you ultimately choose?"

**Question 7**: "What were the main reasons for choosing this approach over the others?"

**Question 8**: "What was the expected outcome or goal when you made this decision? What were you hoping to achieve?"

## Phase 5: Capture Real-World Consequences

Now that we've covered the options, their pros/cons, and the expected outcome, capture what actually happened:

**Question 9**: "Now that this decision has been in place, what positive outcomes have you observed? How has it helped?"

**Question 10**: "Have there been any negative consequences or challenges that resulted from this choice?"

**Question 11**: "Were there any unexpected trade-offs or surprises - things you didn't anticipate when making the decision?"

**Question 12**: "If you were making this decision again today, would you decide differently? Why or why not?"

## Phase 6: Generate the ADR

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

## Phase 7: Finalize

If user requests changes:
- Make the requested edits to the ADR file
- Save the updated version
- Show the updated content again if changes were substantial

After any revisions (or if no changes requested):
- Ensure status is set to "accepted" (since this is a past decision already in effect)
- Confirm: "ADR created at `{adr_location}/NNNN-title.md`. The decision has been documented!"

## Interview Tips

- **Be patient**: Let the user think and recall details
- **Probe gently**: If answers are vague, ask follow-up questions
- **Validate understanding**: Summarize back to confirm accuracy
- **Accept uncertainty**: "I don't remember" is a valid answer
- **Note gaps**: If information is missing, note it in the ADR

## Notes

- Past decisions (documented via interview) should have status "accepted" since they're already in effect
- If a decision has since been reversed, set status to "superseded" or "deprecated" instead
- Link to any related PRs or issues if the user can recall them
- It's okay to have some sections less detailed for older decisions
