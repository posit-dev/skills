---
name: deploy-to-connect
description: >-
  Deploy or publish Python and R content to a Posit Connect server using
  rsconnect-python or the R rsconnect package. Handles interactive apps and
  dashboards, web APIs, rendered documents, and prepared bundles/manifests. Use
  whenever the user asks to deploy, publish, or redeploy content to Posit
  Connect, or mentions rsconnect. Consult this skill instead of guessing flags
  or commands.
metadata:
  author: posit-pbc
  version: "2.0"
---

# Deploying to Posit Connect

This skill deploys **both Python and R content** to **Posit Connect**. Work
through the stages in order.

Two toolchains are involved:

- **Python** —
  [rsconnect-python](https://github.com/posit-dev/rsconnect-python), which
  provides the `rsconnect` CLI and is published on PyPI.
- **R** — the R [`rsconnect`](https://rstudio.github.io/rsconnect/) package,
  targeting the Connect **server** (not Connect Cloud).

**As you go, record every decision, install, fallback, and assumption** so you
can report them at the end — this is what makes the run auditable and
self-healing rather than silent.

---

## Stage 1 — Detect the content

Infer the **language** and **framework** from the files in the project
directory. Common signals:

| Signal in project dir | Likely content |
| --- | --- |
| `app.py` | Python web app — Shiny for Python, Streamlit, Dash, Gradio, Panel, or Bokeh (disambiguate by imports, below) |
| `app.R`, or `ui.R` + `server.R` | Shiny for R |
| `plumber.R` / `entrypoint.R` containing `plumb()` | Plumber API (R) |
| `*.qmd` | Quarto document |
| `*.Rmd` | R Markdown |
| `*.ipynb` | Jupyter notebook / Voila |
| `manifest.json` | Prebuilt bundle (deploy directly, no framework guess needed) |

**Disambiguate `app.py` by its imports:**

```console
grep -Eo 'import (shiny|streamlit|dash|gradio|panel|bokeh)|from (shiny|streamlit|dash|gradio|panel|bokeh)' app.py
```

- `shiny` → shiny (Python)  · `streamlit` → streamlit  · `dash` → dash
- `gradio` → gradio  · `panel` → panel  · `bokeh` → bokeh
- A bare ASGI/WSGI object (`fastapi` / `flask`) → `fastapi` / `flask`

**Dependency-file signals** confirm the language:

- Python: `requirements.txt`, `pyproject.toml`
- R: `DESCRIPTION`, `renv.lock`, or a spread of `.R` files

**If the content is ambiguous** (e.g. both Python and R files, or an `app.py`
with no recognizable import): if you have an ask-user / prompt tool available,
ask the user which framework to deploy. Otherwise, **pick the strongest signal**
(a framework-specific import beats a generic dep file) and **record the
assumption** for your report.

---

## Stage 2 — Inventory your tools

Probe the environment and build a capability set — don't assume anything is
installed.

```console
command -v rsconnect                                 # rsconnect-python on PATH
command -v uv                                        # uv (installs and runs Python tools)
uv tool list 2>/dev/null | grep rsconnect            # rsconnect-python installed via uv
command -v Rscript                                   # R present
Rscript -e 'cat(requireNamespace("rsconnect", quietly=TRUE))' 2>/dev/null   # R rsconnect package
command -v quarto                                     # quarto CLI
command -v git                                        # git
```

Note which of these are present: `rsconnect` (or `uv`, which can run it without
installing), `Rscript` + R `rsconnect`, `quarto`, `git`.

With `uv` available you never need an install step for Python content —
`uv tool run --from rsconnect-python rsconnect ...` fetches and runs it on
demand.

---

## Stage 3 — Pick a route

Cross the detected content (Stage 1) with your capabilities (Stage 2):

### Python content

Use rsconnect-python.

1. **`rsconnect` already on `PATH`:**
   ```console
   rsconnect deploy <framework> ./my-app
   ```
2. **Not on `PATH` but `uv` is** — run it without installing anything:
   ```console
   uv tool run --from rsconnect-python rsconnect deploy <framework> ./my-app
   ```

Both forms take identical arguments; the rest of this skill writes the bare
`rsconnect ...` form, so prefix it with `uv tool run --from rsconnect-python`
if you're on route 2.

`<framework>` is one of `api`, `bokeh`, `bundle`, `dash`, `fastapi`, `flask`,
`git`, `gradio`, `html`, `manifest`, `nodejs`, `notebook`, `panel`, `pyproject`,
`quarto`, `shiny`, `streamlit`, `tensorflow`, `voila`
(`rsconnect deploy other-content` prints guidance for anything not in that
list).

**The available frameworks and flags depend on the installed version**. 
Always confirm against `rsconnect deploy --help` rather than trusting this list.
If `uv tool run` resolves a stale cached version, pin it:
`uv tool run --from 'rsconnect-python==1.30.0' rsconnect ...`.

### R content

Prefer the R `rsconnect` package targeting the Connect **server**, run through
`Rscript -e '...'` or an R session.

Which deploy function to use:

- **Shiny for R / Plumber API / any app directory** → `deployApp()`
- **A single R Markdown or Quarto document** → `deployDoc()`
- **A full R Markdown / Quarto site** → `deploySite()`

**If R is absent** (no `Rscript`): deploy the R content through rsconnect-python
using a `manifest.json`.

- If a `manifest.json` already exists, deploy it directly:
  ```console
  rsconnect deploy manifest ./manifest.json
  ```
- If there's no manifest and R *is* available elsewhere, generate one first with
  `rsconnect::writeManifest()` (see Stage 5).
- If there's **neither R nor a manifest**, you cannot produce a valid R bundle.
  Surface this as a blocker: ask the user (if you have an ask-user tool) or
  report it clearly. Don't fake a deploy.

### Quarto content

Use the rsconnect quarto route:

```console
rsconnect deploy quarto ./report
```

Note: **R-flavored Quarto** (documents with R code chunks) needs R available to
render. If the `.qmd` has R chunks and R is absent, treat it like R content
(manifest route) or surface the gap.

---

## Stage 4 — Check credentials for that tool

Now that you know which tool you're using, check whether it can already reach the
server. **This is a check, not a login** — being authenticated already is the
common case (env vars set by CI, an account linked in an earlier session). If a
path is live, do nothing here: don't run a login, don't run `rsconnect add`.

Both tools read `CONNECT_SERVER` / `CONNECT_API_KEY` from the environment, so
start there either way:

```console
env | grep -E '^CONNECT_(SERVER|API_KEY)=' | sed 's/=.*/=<set>/'   # don't print the key
```

**Python (rsconnect-python)** — saved servers and stored tokens:

```console
rsconnect list
```

**R (`rsconnect`)** — linked servers and accounts:

```console
Rscript -e 'print(rsconnect::accounts())'
```

If the tool itself isn't installed yet, the env-var check still tells you what
you need; close the install gap in Stage 5, then run the tool-specific check.

Record the verdict: either a credential path is live (continue to Stage 6 once
any other gaps are closed) or there is none, which is a discrepancy for Stage 5.
Beware of having *two* paths live at once for Python — see the mixing warning in
the [credentials reference](#credentials-reference).

---

## Stage 5 — Resolve discrepancies (self-heal)

When Stages 3 and 4 find a gap, close it and **record the action**:

- **`rsconnect` not on `PATH`** → don't install anything if `uv` is present;
  just run it on demand:
  ```console
  uv tool run --from rsconnect-python rsconnect deploy <framework> ./my-app
  ```
  If the user wants it installed persistently (or `uv tool run` isn't viable):
  ```console
  uv tool install rsconnect-python     # or: pip install rsconnect-python
  ```
  **Note the package/command mismatch:** the PyPI package is
  `rsconnect-python`, the command it provides is `rsconnect`. That's why
  `uv tool run` needs `--from rsconnect-python`. To update later:
  `uv tool upgrade rsconnect-python`.
- **R `rsconnect` package missing** (but `Rscript` present) → install it from
  Posit Package Manager (P3M), which serves **precompiled Linux binaries** — far
  faster than a source build and with no `-dev` system libraries to apt-get. Two
  things are required to actually get binaries: the `__linux__/<codename>` repo
  URL **and** a platform-identifying `HTTPUserAgent` (without it P3M serves
  source):
  ```console
  export P3M="https://packagemanager.posit.co/cran/__linux__/$(. /etc/os-release && echo "$VERSION_CODENAME")/latest"
  Rscript -e '
    options(HTTPUserAgent = sprintf("R/%s R (%s)", getRversion(),
      paste(getRversion(), R.version["platform"], R.version["arch"], R.version["os"])))
    install.packages("rsconnect", repos = Sys.getenv("P3M"))
  '
  ```
  P3M binaries exist for **x86_64** on common distros; on **arm64** or an
  unsupported distro P3M transparently falls back to source (still correct, just
  slower — make sure the usual `-dev` libraries and a compiler are present). Only
  reach for `https://cloud.r-project.org` (CRAN source) if P3M is unreachable.
- **`manifest.json` missing for R content** (R present) → generate it:
  ```console
  Rscript -e 'rsconnect::writeManifest()'
  ```
  Alternatively, rsconnect-python can write one for Python content:
  ```console
  rsconnect write-manifest <framework> ./my-app
  ```
  Then deploy the manifest via rsconnect-python if R can't deploy directly.
- **No credentials** (Stage 4 found no env vars, no saved server, no linked
  account) → authenticate now, following
  [Credentials reference](#credentials-reference) for the ordering, the
  pitfalls, and what to do when nothing can supply them. Prefer a browser login
  (`rsconnect login`, `rsconnect::connectUser()`) when one is available.
- **Dependencies** → you generally do **not** hand-list them. rsconnect and
  rsconnect-python scan the code and snapshot required package versions
  automatically (Python from `requirements.txt`/imports, R from your `.R`
  code). Make sure a Python `requirements.txt` exists when deploying Python
  content. For R, the content's own packages must be **installed locally** for
  rsconnect to detect and snapshot them (e.g. `plumber` for a Plumber API,
  `shiny` for a Shiny app) — install any that are missing from the same P3M repo
  shown above, not from CRAN source.

---

## Stage 6 — Deploy and handle failure

### Discover the live command surface (Python)

rsconnect-python's frameworks and flags change between releases, so **read the
help text — it's the source of truth**:

```console
rsconnect version                  # which version you're actually running
rsconnect deploy --help            # every framework you can deploy
rsconnect deploy <framework> --help  # flags for one framework
```

### Deploy

For Python, `rsconnect deploy <framework> <dir>` with the framework Stage 3
picked (`manifest` takes the manifest file rather than a directory).

Non-obvious flags: `-t/--title`, `-N/--new` (force a new deployment instead of
updating the recorded one), `-a/--app-id <id>` (target an existing item
explicitly — mutually exclusive with `--new`), `-E NAME=VALUE` (set an
environment variable, repeatable), `--draft` (keep serving the previous bundle
until published).

For R, call the function Stage 3 selected, passing `appTitle` so the content
isn't named after the directory.

### If `rsconnect` isn't found at deploy time

It may be installed but off `PATH` in this shell (common in IDE-spawned
terminals or with a virtualenv active). Fall back to `uv tool run` as described
in Stage 5 — remembering `--from rsconnect-python`, since the package and
command names differ.

### Pre-flight check (optional)

To confirm the target is reachable and the credentials work before deploying:

```console
rsconnect details -n myserver                   # reachability + auth for one server
```

### When a deploy fails

**Python:**

- Auth errors: confirm the target with `rsconnect list`, re-run
  `rsconnect login` (1.30.0+), or pass `-s`/`-k` (or set
  `CONNECT_SERVER`/`CONNECT_API_KEY`).
- `-n/--name ... cannot be specified in conjunction with ... ENVIRONMENT`: you
  mixed a saved nickname with env-var credentials — see the mixing warning in
  the credentials reference. Drop `-n` or
  `unset CONNECT_SERVER CONNECT_API_KEY`.
- `The requirements file 'requirements.txt' does not exist`: Python content
  needs one. Create it, point at another file with `--requirements-file`, or
  generate it with `--force-generate` (a `pip freeze`, so it may over-pin).
- Self-signed TLS: use `-i/--insecure` (or `-c/--cacert <file>`); set
  `CONNECT_INSECURE` / `CONNECT_CA_CERTIFICATE` to apply it everywhere.
- Rejected flag or unknown framework: re-check `rsconnect version` and re-read
  `rsconnect deploy <framework> --help` — this usually means the installed
  version is older than the flag you used.

**R:**

- "No account" / auth errors: run `rsconnect::accounts()`; if empty, re-run
  `rsconnect::addServer()` + `connectUser()`/`connectApiUser()`. Double-check you
  used a server function, not `connectCloudUser()` (Cloud).
- Deploy hangs at an account prompt: more than one account is linked. Pass
  `account =` (and `server =`) explicitly to the deploy call.
- Wrong deploy function: use `deployApp()` for directories/apps, `deployDoc()`
  for a single document, `deploySite()` for a site.
- Self-signed TLS: pass the CA bundle via the `RETICULATE`/`curl` options or
  add the server with the appropriate certificate; for quick tests set
  `options(rsconnect.check.certificate = FALSE)` (use sparingly).
- Absolute-path warnings: files with hard-coded absolute paths won't block the
  deploy but should be made relative to the project directory.

---

## Credentials reference

How to authenticate when Stage 4 found no credentials and Stage 5 sent you here.
If a credential path is already live, you don't need any of this.

### Python (rsconnect-python)

In order of preference:

1. **OAuth login (interactive).** Requires **rsconnect-python 1.30.0+** — check
   with `rsconnect version` first. One browser flow per server; tokens land in
   the OS keyring (falling back to a local credential store) and refresh
   automatically:
   ```console
   rsconnect login https://connect.example.com
   rsconnect login https://connect.example.com --use-device-code   # headless
   ```
2. **Saved API-key nickname.** Save once, select later with `-n/--name`:
   ```console
   rsconnect add -n myserver -s https://connect.example.com -k <api-key>
   rsconnect list                    # confirm what's saved
   ```
3. **Env vars.** Best for headless/automated runs — no state to manage, and
   works on any version:
   ```console
   export CONNECT_SERVER=https://connect.example.com
   export CONNECT_API_KEY=...        # honored across the whole `rsconnect` surface
   ```
4. **Ad hoc flags** on the deploy command itself: `-s <url> -k <api-key>`.

**Shared credential flags:** `-n/--name` (saved server), `-s/--server` (env
`CONNECT_SERVER`), `-k/--api-key` (env `CONNECT_API_KEY`), `-i/--insecure` (env
`CONNECT_INSECURE`, for self-signed TLS), `-c/--cacert <file>` (env
`CONNECT_CA_CERTIFICATE`).

> **Pick ONE auth path — never mix `-n` with env-var credentials.** rsconnect
> rejects a command that combines a saved-server name (`-n/--name`) with
> `CONNECT_SERVER`/`CONNECT_API_KEY` set in the environment, with an error like
> `-n/--name (from COMMANDLINE) cannot be specified in conjunction with options
> -s/--server (from ENVIRONMENT)`. Choose by what you have:
>
> - **`CONNECT_SERVER` and `CONNECT_API_KEY` are set** (typical headless/automated
>   run) → do **not** pass `-n`; let the env vars supply the target and key.
>   Deploy with just `rsconnect deploy <framework> <dir>`.
> - **The request names a specific saved server** (e.g. "deploy to dogfood") →
>   use `-n dogfood`, and make sure `CONNECT_SERVER`/`CONNECT_API_KEY` are **not**
>   also exported for that command (`unset` them, or don't run `rsconnect add`
>   from a shell that has them set).
>
> If you have env-var creds but the request also names a server, prefer the env
> vars (drop `-n`) — mixing is what triggers the rejection.

### R (`rsconnect`)

Register the server under a local nickname, then register your user against it:

```r
library(rsconnect)

# 1. The server (once per server; the name is a local nickname)
rsconnect::addServer(url = "https://connect.example.com", name = "myserver")

# 2a. Interactive — approve in a browser, no key to handle
rsconnect::connectUser(server = "myserver")

# 2b. Or non-interactively (CI) — connectApiUser() requires an apiKey
rsconnect::connectApiUser(
  server  = "myserver",
  account = "your-username",
  apiKey  = Sys.getenv("CONNECT_API_KEY")
)
```

> **Critical — this is Connect *server*, not Connect Cloud.** Use
> `rsconnect::connectUser()` or `rsconnect::connectApiUser()`, **never**
> `connectCloudUser()`. The Cloud functions authenticate against a different
> service and will not work here.

### If no credentials can be found

- Rely on the `CONNECT_SERVER` / `CONNECT_API_KEY` env vars and, if
  they're absent, **report the missing credentials** rather than guessing 
  or asking the user to paste an API key into the context.
