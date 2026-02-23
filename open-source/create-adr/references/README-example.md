# Architecture Decision Records (ADRs)

This directory contains Architecture Decision Records (ADRs) for this project.

## What is an ADR?

An Architecture Decision Record captures an important architectural decision made along with its context and consequences. ADRs help teams:

- **Document** significant decisions for future reference
- **Communicate** decisions to team members and stakeholders
- **Understand** the reasoning behind existing architecture
- **Onboard** new contributors by explaining "why" things are the way they are

## ADR Format

We use the [MADR](https://adr.github.io/madr/) (Markdown Any Decision Record) format. Each ADR includes:

- **Status**: proposed, accepted, rejected, deprecated, or superseded
- **Context**: The situation and problem being addressed
- **Decision Drivers**: Factors influencing the choice
- **Options Considered**: Alternatives that were evaluated
- **Decision Outcome**: The chosen option and its justification
- **Consequences**: Both positive and negative outcomes

See [`_template.md`](_template.md) for the full template.

## Naming Convention

ADRs follow the naming pattern:

```
NNNN-<kebab-case-title>.md
```

Where:
- `NNNN` is a 4-digit sequence number (0001, 0002, etc.)
- `<kebab-case-title>` is a short, descriptive title

Examples:
- `0001-use-rest-api.md`
- `0002-adopt-microservices.md`
- `0003-use-postgresql.md`

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

## ADR Lifecycle

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

## Index

<!-- Add links to ADRs here as they are created -->

*No ADRs yet. Create the first one!*
