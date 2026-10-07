# Running the shiny-r-optimize evals

Protocol for running eval iterations against the fixture apps. The goal is
that the agent under test sees **only** what a real user would have: the app
files and their prompt. Nothing that reveals the planted problems, the
assertions, or the existence of an eval.

## Isolation rules

1. **Never run evals from the repo, the skill directory, or the workspace
   root.** Those trees contain `evals/GRADING.md`, `evals/evals.json` (full
   assertion list), and other iterations' completed solutions — any of which
   is an answer key if it is in the agent's working directory or reachable
   via parent directories.
2. **Create a fresh temp directory per run** and populate it with only the
   fixture app files, e.g. from a clean export rather than the working tree:

   ```sh
   TMPRUN=$(mktemp -d)
   git -C <repo-root> archive HEAD shiny/shiny-r-optimize-workspace/apps/sales-dashboard \
     | tar -x -C "$TMPRUN" --strip-components=4
   ```

   A `git archive` export also guarantees no `.git` directory is reachable,
   so the agent cannot recover the answer key from commit history (the
   leak-removal commits describe exactly what was leaked and where).
3. **Give the agent only the temp dir path** and the eval prompt. Do not
   mention the skill workspace, evals/, GRADING.md, or other iterations.
4. **Write `eval_metadata.json` for an eval only after its runs complete.**
   If it sits in the run tree during execution, it hands the agent the
   verbatim assertion list.
5. **Delete scratch/working directories after copying deliverables into
   `outputs/`.** Iteration-3's with-skill run lost cited artifacts (and
   operated with the answer key reachable) because it worked in-place.
6. **Treat other evals' outputs as answer keys too.** eval-0 and eval-2 share
   a fixture, so a completed eval-0 `outputs/app/app.R` is a solution for
   eval-2. Never let a run read from another eval's directory.

## After the runs

1. Capture `timing.json` in each run directory immediately from the
   completion notification (tokens/duration are not persisted elsewhere).
2. Grade against `eval_metadata.json` assertions; write `grading.json`
   per run (fields: `text`, `passed`, `evidence`).
3. Aggregate with skill-creator's `aggregate_benchmark.py`; note that
   `runs_per_configuration` must reflect reality (record 1 run as 1 run).
4. Record `analyst_notes.json`, then launch the review viewer.
