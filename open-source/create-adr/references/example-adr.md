# Use MADR Format for Architecture Decision Records

* Status: accepted
* Deciders: Core Team, Technical Lead
* Date: 2024-01-15

Technical Story: As the project grows, we need a consistent way to document significant architectural decisions for future reference and to help onboard new contributors.

## Context and Problem Statement

The team needs a standardized format for documenting architectural decisions. Currently, important decisions are scattered across pull requests, GitHub issues, and meeting notes, making it difficult to understand the reasoning behind current architecture. How should we document architectural decisions in a way that's accessible, searchable, and maintainable?

## Decision Drivers

* Must be easy to write in plain text (developer-friendly)
* Should work well with version control (git-friendly)
* Must be searchable and browsable without special tools
* Should provide sufficient structure without being overly complex
* Should be well-adopted in the open-source community with good examples
* Need to capture alternatives considered, not just the final decision

## Considered Options

* MADR (Markdown Any Decision Record)
* Y-statements (minimal format)
* Plain markdown files with no template
* Michael Nygard's original ADR format

## Decision Outcome

Chosen option: "MADR (Markdown Any Decision Record)", because it provides comprehensive structure while remaining simple to use, has good tooling support, and is widely adopted in the open-source community. It strikes the best balance between completeness and ease of use.

### Positive Consequences

* Consistent structure across all ADRs makes them easy to read and compare
* Encourages thorough consideration of alternatives before deciding
* Well-documented format with many examples available
* Active community support and tooling
* Captures both the "what" and the "why" of decisions
* Optional sections allow flexibility for simple vs complex decisions

### Negative Consequences

* More verbose than minimal formats like Y-statements
* Requires discipline to fill out all relevant sections
* May seem like overhead for very small decisions
* Team needs to learn the format (though it's straightforward)

## Pros and Cons of the Options

### MADR (Markdown Any Decision Record)

Full-featured ADR format with comprehensive sections for context, options, decision outcome, and consequences.

* Good, because it provides comprehensive structure that covers all important aspects
* Good, because it's widely adopted in open-source projects (many examples available)
* Good, because it has good documentation and templates
* Good, because it encourages thorough analysis of alternatives
* Good, because optional sections allow adapting to decision complexity
* Bad, because it can be verbose for very simple decisions
* Bad, because it requires more time to write than minimal formats

### Y-statements

Minimal one-line format: "In context X, facing concern Y, we decided for option Z to achieve quality Q, accepting downside D"

* Good, because it's very concise and forces focus on essentials
* Good, because it's extremely quick to write
* Good, because it captures the core decision in one sentence
* Bad, because it lacks detail for complex decisions
* Bad, because it doesn't capture full pros/cons of alternatives
* Bad, because it's hard to search and browse multiple decisions
* Bad, because it may omit important context

### Plain markdown with no template

Freeform markdown files without a prescribed structure or template.

* Good, because it's completely flexible
* Good, because there's no learning curve
* Good, because writers can adapt to each decision's needs
* Bad, because consistency is difficult to maintain
* Bad, because important details might be accidentally omitted
* Bad, because new contributors don't know what to include
* Bad, because comparing decisions across time is harder

### Michael Nygard's Original ADR Format

The original ADR format with sections: Title, Status, Context, Decision, and Consequences.

* Good, because it's the original and well-known format
* Good, because it's simpler than MADR (fewer sections)
* Good, because it captures the essential information
* Bad, because it doesn't explicitly capture alternatives considered
* Bad, because it lacks the detail needed for complex decisions
* Bad, because MADR is an evolution with more community adoption now

## Links

* [MADR Project](https://adr.github.io/madr/)
* [ADR GitHub Organization](https://adr.github.io/)
* [Original ADR article by Michael Nygard](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
