---
name: r-cmd-check-cpu-time
description: Diagnose and fix the R CMD check NOTE "had CPU time N times elapsed time" for tests, examples or vignettes. Use when a CRAN submission or check reports that NOTE, when check output shows a [cpu/elapsed] ratio above ~1, or when you need to find out which test file or vignette in an R package is silently using multiple cores.
---

# Fix "CPU time N times elapsed time"

R CMD check reports this NOTE when code uses more CPU time than elapsed time,
which can only happen when something runs concurrently. The reporting threshold
is a ratio chosen by the checking machine, not a fixed value in R. R-ints
documents the default as `NA`, meaning no check at all, so the value CRAN uses is
theirs and is not published; 2.5 is the commonly cited figure.

## Read this first

The NOTE is a true observation. Some code really did use more than one core.
Treat it as a bug to locate, not a number to argue about.

The failure mode of this task is spending your effort trying to reproduce the
ratio on the developer's machine, then concluding it is spurious when you
cannot. Two facts make local reproduction nearly useless:

* The CRAN macOS and Windows builds link the single-threaded reference BLAS, and
  macOS binaries often ship without OpenMP. A suite measuring 3.1 on CRAN can
  measure 1.0 on a Mac that has more cores.
* The ratio scales with what the check machine has, not with what you have.
* Windows does not report the CPU component at all, so a Windows check shows a
  single number and can never surface this.

So do not try to reproduce it locally. Go straight to measuring on Linux, and
localize per file before changing any code.

## Step 1: make the ratio visible

The timing report is off unless you turn it on, and the ratio check is off
unless you set a threshold. Defaults are `NA`, meaning no report at all.

```sh
env _R_CHECK_TIMINGS_=0 _R_CHECK_TEST_TIMING_CPU_TO_ELAPSED_THRESHOLD_=1.05 \
  R CMD check --as-cran --timings <pkg>.tar.gz
```

`--as-cran` alone prints `[cpu/elapsed]` per test file and vignette, so an
existing CI log may already have the number. Check that before running anything:
CI that runs `--as-cran`, which is the common default, has been recording this
ratio all along. Grep old logs for `Running .testthat` and read the bracketed
pair. On Linux and macOS jobs it is a `cpu/elapsed` pair; on Windows a single
elapsed number.

Thresholds, all defaulting to `NA` (documented in R-ints):

| variable | covers |
|---|---|
| `_R_CHECK_TEST_TIMING_CPU_TO_ELAPSED_THRESHOLD_` | individual test files |
| `_R_CHECK_EXAMPLE_TIMING_CPU_TO_ELAPSED_THRESHOLD_` | examples |
| `_R_CHECK_VIGNETTE_TIMING_CPU_TO_ELAPSED_THRESHOLD_` | vignettes |
| `_R_CHECK_INSTALL_TIMING_CPU_TO_ELAPSED_THRESHOLD_` | installation |

Setting a threshold near 1.05, well below whatever the check machine uses, turns
this into a regression gate. Note it only fires where
`cpu >= max(theta * elapsed, 1)`, so fast suites never report regardless.

## Step 2: get a Linux runner with a threaded BLAS

Use R-hub v2. If the maintainer already has a token, `rc_submit()` needs no
workflow file, no push, and no repo changes at all:

```r
rhub::rc_list_local_tokens()   # check for an existing token first
rhub::rc_submit(platforms = "ubuntu-release", confirmation = TRUE)
```

Without a token, `rhub::rc_new_token()` emails one. The alternative,
`rhub_setup()` plus `rhub_check()`, writes a workflow that **must be committed to
the default branch**, which is often not acceptable on a shared repo.

`rc_submit()` uploads the package source to R Consortium infrastructure and
creates a **public** repository under the `r-hub2` organisation. Confirm with the
maintainer before using it on anything unpublished or private. It also builds
from the working directory, not from git, which is what makes the `.gitignore`
trap below possible.

Useful platforms (`rhub::rhub_platforms()` for the full list):

| platform | why |
|---|---|
| `ubuntu-release` | Ubuntu default is the pthread build of OpenBLAS. Best default. |
| `mkl` | Intel MKL, a different threading implementation |
| `atlas` | ATLAS. earth has been seen to fail to `dyn.load` on this container, unrelated to the package under test. |

Runs take 3 to 5 minutes. They are GitHub Actions runners with about 4 cores, so
a mechanism that saturates all cores shows roughly 3 to 4, not the higher ratios
a large CRAN machine reports. That is enough to localize and to verify a fix.

Results:

```sh
gh run list  --repo r-hub2/<generated-repo-name> --limit 1
gh run view <id> --repo r-hub2/<repo> --log | grep -E "Running .testthat|re-building of vignette"
gh run download <id> --repo r-hub2/<repo> --dir art   # full .Rcheck directory
```

## Step 3: localize before fixing

Do not cap threads across the suite and hope. Find the file. Temporarily replace
`tests/testthat.R` with a loop that times each file, submit once, and read the
per-file ratios. `proc.time()` covers every thread of the process, so any file
above about 1 is running something concurrently.

```r
library(testthat)
library(<pkg>)
old <- setwd("testthat")
for (f in sort(list.files(".", pattern = "^test.*[.][Rr]$"))) {
  a <- proc.time()
  try(test_file(f, reporter = "silent"), silent = TRUE)
  d <- proc.time() - a
  cat(sprintf(
    "TIMING %-32s cpu=%7.2f elapsed=%7.2f ratio=%6.2f\n",
    f, sum(d[-3L]), d[3L], sum(d[-3L]) / max(d[3L], 0.001)
  ))
}
setwd(old)
```

`proc.time()` also counts child processes, so this catches a test that farms work
out to a subprocess, which a thread count taken from one PID would miss.

Test output only reaches the check log on failure, so read it from the
downloaded artifact at `<pkg>.Rcheck/tests/testthat.Rout`. Restore the real
`testthat.R` immediately after submitting, so instrumentation cannot be
committed by accident.

For vignettes, each one knits in its own process, so a `document` hook gives a
per-vignette whole-process ratio. Write the log somewhere the artifact keeps,
such as the `.Rcheck` root:

```r
knitr::knit_hooks$set(document = function(x) {
  t <- proc.time()
  cat(
    sprintf("VIGTIMING %s cpu=%.2f elapsed=%.2f\n", knitr::current_input(),
            sum(t[-3L]), t[3L]),
    file = file.path(getwd(), "..", "..", "..", "vigtimings.txt"), append = TRUE
  )
  x
})
```

That path assumes vignettes are rebuilt in `<pkg>.Rcheck/vign_test/<pkg>/vignettes`
and writes to the `.Rcheck` root, which the artifact keeps. If the file does not
appear in the artifact, log `getwd()` and adjust the depth.

### Reading the numbers

Compare `cpu - elapsed`, not the ratio. The ratio misleads badly on short files.

* Excess growing with the work: real parallel compute. Fix it.
* Excess constant across files that do completely different amounts of work:
  fixed per-process startup, and not yours to fix. A threaded BLAS spawning its
  thread pool as R loads it is the likely source, since that happens before any
  package code runs, but the diagnosis does not depend on pinning the mechanism:
  an excess that does not vary with the work cannot be coming from the work. It
  has run on the order of 0.3s per process. A suite in one process hides this; a
  dozen vignettes in a dozen processes multiply it. No in-process call can
  reclaim it, because the threads have already spun. Only an environment variable
  such as `OPENBLAS_NUM_THREADS`, set before R starts, would, and that belongs to
  the check machine.

## Step 4: cap the threads

Prefer a call-site argument. Fall back to an in-process API call. Environment
variables are the weakest option, because OpenMP and BLAS latch their thread
counts when loaded, which for BLAS is before any code you control.

The table below is **not a checklist and not a list of everything that
threads**. It records how to cap the sources that have actually been measured,
so you do not have to rediscover them. Anything absent from it is untested, not
cleared. Step 3 is what finds offenders; this is the lookup you reach afterwards.
Thread defaults and argument names also change between releases, so confirm
against the installed version rather than trusting the row.

### Finding the knob for a package not listed here

```r
grep("thread|threads|cores|ncpus|parallel|nthread", names(formals(f)),
     value = TRUE, ignore.case = TRUE)
```

Work through, in order:

1. An argument on the function doing the work, **and separately** on whatever
   constructs its input and whatever consumes its output. A single call often
   spans three functions with three independent thread settings, and the ones
   either side of the obvious call are the ones usually missed.
2. An in-process setter (`setDTthreads()`, `blas_set_num_threads()`,
   `torch::torch_set_num_threads()`, `arrow::set_cpu_count()`,
   `RcppParallel::setThreadOptions()`).
3. A package-specific environment variable, which may be read at call time and
   so still work, or latched at load and so not.
4. Nothing available: check whether the package is even installed on CRAN's
   machines, then whether the offending test can be skipped there.

Anything wrapping a native thread pool or a BLAS can thread: `arrow`, `duckdb`,
`polars`, `fst`, `torch`, Stan-based packages, and anything using `RcppParallel`
or OpenMP directly.

| source | how to cap | notes |
|---|---|---|
| BLAS/LAPACK | `RhpcBLASctl::blas_set_num_threads(1)` | Debian and Ubuntu default to `openblas-pthread`, which **ignores `OMP_NUM_THREADS` by design**, so every `OMP_*` variable looks inert. Check this first, and confirm with `La_library()`. |
| data.table | `data.table::setDTthreads(1L)` | Latches at load. Reached indirectly through `xgb.model.dt.tree()` and `lgb.model.dt.tree()`, neither of which takes a thread argument. |
| xgboost | `nthread` in `xgb.train(params=)` **and** in `xgb.DMatrix()` | The `DMatrix` constructor defaults to every core and is easy to miss. |
| lightgbm | `num_threads` in `lgb.train(params=)`, `lgb.Dataset(params=)` **and** `predict(params=)` | lightgbm calls `omp_set_num_threads()` itself at predict time, overriding the environment. |
| ranger | `num.threads` on **both** `ranger()` and `predict()` | `predict.ranger()` defaults to every core no matter what the fit used. Uses `std::thread`, so no `OMP_*` variable reaches it. |
| earth | none; cap the BLAS | Thousands of tiny least-squares fits, enough to cross OpenBLAS's threading threshold. Often the single largest contributor while looking innocent. |
| catboost | none available | Spawns a thread per core. Not on CRAN, so usually skipped there. |
| dbarts | `nthread` | Already defaults to `1L`. |

Verified against xgboost 3.x, lightgbm 4.x and ranger 0.16 (2026).

Put process-wide caps at the very top of `tests/testthat.R`, above the
`library()` calls. Add whatever you use to `Suggests`, guarded by
`requireNamespace()`.

## Step 5: verify against the baseline

Resubmit to the same platform and compare with the number you recorded before
the fix. Do not accept "the NOTE is gone" as evidence: the NOTE only fires if a
threshold variable is set, and rhub does not set one. Read the printed
`[cpu/elapsed]` pair.

## Traps

* **A `vignettes/.gitignore` containing `*.R` will silently drop a shared setup
  file.** `rc_submit()` builds from the working directory, so the run passes
  while a fresh checkout would fail. Add `!_threads.R`, then confirm with
  `git archive HEAD | tar -t | grep _threads`.
* **A peak-thread-count probe reads a single PID.** It misses child processes,
  and on macOS it clears packages whose OpenMP is compiled out there but active
  on Linux. Do not use it to exonerate anything.
* **A ratio near 1.2 on 4 cores is not automatically benign.** Decide with the
  `cpu - elapsed` test above, rather than by comparing against a threshold.
