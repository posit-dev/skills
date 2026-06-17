# Posit Developer Skills

General-purpose developer skills useful across any language, project type, or context. These skills help with common development tasks like code review and architecture documentation, regardless of whether you're working on open-source packages, internal tools, or proprietary applications.

## Skills

- **[critical-code-reviewer](./critical-code-reviewer/)** - Rigorous, adversarial code review across Python, R, JavaScript/TypeScript, SQL, and front-end code
- **[review-testing](./review-testing/)** - Review test code for quality, design, and completeness after implementing a feature or fixing a bug, covering assertion completeness, mocking boundaries, fixture design, test smells, and coverage gaps
- **[describe-design](./describe-design/)** - Research a codebase and create architectural documentation with Mermaid diagrams
- **[implement](./implement/)** - Orchestrates implementation of a plan file by delegating work to subagents in parallel
- **[new-work](./new-work/)** - Create a todo tracking document for a new feature, bug, or task; keeps it updated with decisions, plans, and progress for the rest of the session
- **[working-on](./working-on/)** - Sets an existing tracking document as the source of truth for the current session, keeping it updated with decisions and progress

## Work Tracking Lifecycle

These three skills provide a lightweight way to bridge sessions: a todo document holds enough context that any fresh session can pick up exactly where the last one left off, without re-explaining the problem or re-deriving decisions.

Three skills work together to track a piece of work from start to finish:

1. **`/new-work`** — Start here. Creates a todo document in `_dev/todos/pending/` and keeps it updated for the rest of the session. Write your plan here; it becomes the persistent record.

2. **`/working-on <path>`** — Resume here in a new session. Point it at an existing todo document and it picks up the same live-update behavior: decisions, plans, and commits all flow back into the file.

3. **`/implement <path>`** — Execute here. Takes a plan file (which can be the todo document itself, or a separate plan written into it) and orchestrates implementation by delegating to parallel subagents.

A typical flow:

```
/new-work          → gather context and plan in the todo document
   --- new session ---
/implement <todo>  → execute the plan, update the document
   --- new session ---
/working-on <todo> → continue tracking progress
```

## Contributing

See the main [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines on adding new skills to this category.
