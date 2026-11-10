# Running the shiny-py-optimize evals

Protocol for running eval iterations against the fixture apps. The goal is
that the agent under test sees **only** what a real user would have: the app
files, a Python environment, and their prompt. Nothing that reveals the
planted problems, the assertions, or the existence of an eval.

## Configurations

The skill's advice depends on the installed shiny version (1.9.0 made
reactive effects run concurrently), so run each eval against both versions:

| Configuration | Skill | shiny |
|---|---|---|
| `with_skill` | current skill | 1.9.0 (or latest) |
| `with_skill_shiny18` | current skill | 1.8.0 |
| `old_skill` (when changing the skill) | the skill before the change | 1.9.0 (or latest) |
| `old_skill_shiny18` (when the change is about 1.8.0 behavior) | the skill before the change | 1.8.0 |

## Isolation rules

1. **Never run evals from the repo, the skill directory, or the workspace
   root.** Those trees contain `evals/GRADING.md`, `evals/evals.json` (full
   assertion list), and other iterations' completed solutions — any of which
   is an answer key if it is in the agent's working directory or reachable
   via parent directories.
2. **Create a fresh temp directory per run** and populate it with only the
   fixture app files, from a clean export rather than the working tree. Then
   generate the data and give the run its own `.venv`:

   ```sh
   TMPRUN=$(mktemp -d)
   git -C <repo-root> archive HEAD shiny/shiny-py-optimize-workspace/apps/sales-dashboard \
     | tar -x -C "$TMPRUN" --strip-components=4
   cd "$TMPRUN"
   uv venv -q .venv --python 3.12
   VIRTUAL_ENV=.venv uv pip install -q "shiny==1.9.0" pandas numpy matplotlib jinja2 playwright
   .venv/bin/python generate_data.py   # sales-dashboard and model-explorer only
   ```

   A `git archive` export also guarantees no `.git` directory is reachable,
   so the agent cannot recover the answer key from commit history. Create
   the `.venv` in the run's final location: moving it afterwards breaks the
   `.venv/bin/shiny` script.
3. **Export the skill the same way, to a separate temp directory** (e.g.
   `git archive <ref> shiny/shiny-py-optimize`), and give the agent that path.
   Use the base ref of the change for `old_skill`.
4. **Give the agent only the temp dir path, the skill path, and the eval
   prompt.** Ask it to write `report.md` in the app directory when done.
   Some harnesses block subagents from writing report files; if so, save
   the report from the agent's final message yourself. Do
   not mention the skill workspace, `evals/`, `GRADING.md`, or other
   iterations.
5. **Write `eval_metadata.json` for an eval only after its runs complete.**
   If it sits in the run tree during execution, it hands the agent the
   verbatim assertion list.
6. **Copy deliverables into `outputs/` and delete the temp directory.** Copy
   the app files (not `.venv` or the generated CSV) to `outputs/app/` and
   `report.md` to `outputs/`.
7. **Treat other evals' outputs as answer keys too.** Evals 0 and 2 share a
   fixture, so a completed eval-0 `outputs/app/app.py` is a solution for
   eval 2. Never let a run read from another eval's directory.

## After the runs

1. Capture `timing.json` in each run directory immediately from the
   completion notification (tokens/duration are not persisted elsewhere).
2. Grade against `eval_metadata.json` assertions; write `grading.json`
   per run (fields: `text`, `passed`, `evidence`). For eval 3, grade
   version-dependent assertions against the shiny version that run used.
3. Aggregate with skill-creator's `aggregate_benchmark.py`; note that
   `runs_per_configuration` must reflect reality (record 1 run as 1 run).
4. Record `analyst_notes.json`, then launch the review viewer.
