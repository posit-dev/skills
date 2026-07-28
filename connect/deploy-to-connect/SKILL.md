---
name: deploy-to-connect
description: >-
  Deploy or publish Python and R content to a Posit Connect server using the
  posit CLI, rsconnect-python, or the R rsconnect package. Handles interactive
  apps and dashboards, web APIs, rendered documents, and prepared
  bundles/manifests. Use whenever the user asks to deploy, publish, or redeploy
  content to Posit Connect, or mentions the posit CLI or rsconnect. The posit
  CLI is newer than your training data, so consult this skill instead of
  guessing flags or commands.
metadata:
  author: posit-pbc
  version: "2.0"
---

# Deploying to Posit Connect

This skill deploys **both Python and R content** to **Posit Connect**. Work
through the stages in order.

Two toolchains are involved:

- **Python** — the `posit` CLI (its deploy commands are mounted from
  [rsconnect-python](https://github.com/posit-dev/rsconnect-python), so
  rsconnect-python is an equivalent fallback).
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
command -v posit                                    # posit CLI on PATH
uv tool list 2>/dev/null | grep -E 'posit-cli|rsconnect'   # posit-cli / rsconnect-python via uv
command -v uv                                        # uv (installs Python tools, runs rsconnect-python)
command -v Rscript                                   # R present
Rscript -e 'cat(requireNamespace("rsconnect", quietly=TRUE))' 2>/dev/null   # R rsconnect package
command -v quarto                                     # quarto CLI
command -v git                                        # git
```

Note which of these are present: `posit`, `uv`, rsconnect-python (runnable via
`uv tool run --from rsconnect-python`), `Rscript` + R `rsconnect`, `quarto`,
`git`.

---

## Stage 3 — Pick a route

Cross the detected content (Stage 1) with your capabilities (Stage 2):

### Python content

1. **Preferred:** the `posit` CLI.
   ```console
   posit connect deploy <framework> ./my-app
   ```
2. **Fallback** (posit not installed/on PATH but `uv` is): rsconnect-python
   directly — the deploy commands are identical, just mounted differently.
   ```console
   uv tool run --from rsconnect-python rsconnect deploy <framework> ./my-app
   ```

`<framework>` is one of `api`, `bokeh`, `bundle`, `dash`, `fastapi`, `flask`,
`gradio`, `html`, `manifest`, `nodejs`, `notebook`, `panel`, `pyproject`,
`quarto`, `shiny`, `streamlit`, `tensorflow`, `voila`.

### R content

Prefer the R `rsconnect` package targeting the Connect **server**. The flow is:
register the server, register your API user, then deploy.

```r
library(rsconnect)

# 1. Register the Connect server (once per server; name is a local nickname)
rsconnect::addServer(url = "https://connect.example.com", name = "myserver")

# 2. Register your API user against that server (Connect SERVER auth)
rsconnect::connectApiUser(
  server  = "myserver",
  account = "your-username",
  apiKey  = Sys.getenv("CONNECT_API_KEY")
)

# 3. Deploy, choosing the function that matches the content:
rsconnect::deployApp(appDir = ".", appTitle = "My App")   # Shiny R, Plumber, dirs
rsconnect::deployDoc("report.Rmd")                          # single Rmd / qmd
rsconnect::deploySite(siteDir = ".")                        # Rmd/Quarto website
```

> **Critical — this is Connect *server*, not Connect Cloud.** Use
> `rsconnect::connectApiUser()` (or `connectUser()`), **never**
> `connectCloudUser()`. The Cloud functions authenticate against a different
> service and will not work here.

Which deploy function to use:

- **Shiny for R / Plumber API / any app directory** → `deployApp()`
- **A single R Markdown or Quarto document** → `deployDoc()`
- **A full R Markdown / Quarto site** → `deploySite()`

**If R is absent** (no `Rscript`): deploy the R content through rsconnect-python
using a `manifest.json`.

- If a `manifest.json` already exists, deploy it directly:
  ```console
  uv tool run --from rsconnect-python rsconnect deploy manifest ./manifest.json
  ```
- If there's no manifest and R *is* available elsewhere, generate one first with
  `rsconnect::writeManifest()` (see Stage 4).
- If there's **neither R nor a manifest**, you cannot produce a valid R bundle.
  Surface this as a blocker: ask the user (if you have an ask-user tool) or
  report it clearly. Don't fake a deploy.

### Quarto content

Use the posit / rsconnect quarto route:

```console
posit connect deploy quarto ./report
# or: uv tool run --from rsconnect-python rsconnect deploy quarto ./report
```

Note: **R-flavored Quarto** (documents with R code chunks) needs R available to
render. If the `.qmd` has R chunks and R is absent, treat it like R content
(manifest route) or surface the gap.

---

## Stage 4 — Resolve discrepancies (self-heal)

When Stage 3 finds a gap, close it and **record the action**:

- **`posit` CLI missing** → install it with `uv` (it is **not on PyPI**):
  ```console
  uv tool install git+https://github.com/posit-dev/posit-cli.git
  ```
  **Warning:** There is an unrelated `posit` package on PyPI. Do not
  `uv tool install posit` or `uv tool run posit` — always use `--from posit-cli`
  or install from the GitHub URL above. If GitHub is set up for SSH auth, use
  the `git+ssh://git@github.com/posit-dev/posit-cli.git` form (uv requires the
  `git@` username); for tokens or other hosts, see uv's
  [Git authentication docs](https://docs.astral.sh/uv/concepts/authentication/git/).
  To update later: `uv tool upgrade posit-cli`.
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
  Then deploy the manifest via rsconnect-python if R can't deploy directly.
- **Dependencies** → you generally do **not** hand-list them. rsconnect and
  rsconnect-python scan the code and snapshot required package versions
  automatically (Python from `requirements.txt`/imports, R from your `.R`
  code). Make sure a Python `requirements.txt` exists when deploying Python
  content. For R, the content's own packages must be **installed locally** for
  rsconnect to detect and snapshot them (e.g. `plumber` for a Plumber API,
  `shiny` for a Shiny app) — install any that are missing from the same P3M repo
  shown above, not from CRAN source.

---

## Stage 5 — Authenticate

Deploying needs credentials for the Connect server.

### Python (`posit` / rsconnect-python)

In order of preference:

1. **OAuth login (interactive).** One browser flow per server; tokens land in
   the OS keyring and refresh automatically:
   ```console
   posit connect login https://connect.example.com
   posit connect login https://connect.example.com --use-device-code   # headless
   ```
2. **Env vars / ad hoc flags.** Best for headless/automated runs:
   ```console
   export CONNECT_SERVER=https://connect.example.com
   export CONNECT_API_KEY=...        # honored across the whole `posit connect` surface
   ```
3. **Saved API-key nickname.** Save once, select later with `-n/--name`:
   ```console
   posit connect add -n myserver -s https://connect.example.com -k <api-key>
   ```

**Shared credential flags:** `-n/--name` (saved server), `-s/--server` (env
`CONNECT_SERVER`), `-k/--api-key` (env `CONNECT_API_KEY`), `-i/--insecure` (env
`CONNECT_INSECURE`, for self-signed TLS), `-c/--cacert <file>`.

> **Pick ONE auth path — never mix `-n` with env-var credentials.** The CLI
> rejects a command that combines a saved-server name (`-n/--name`) with
> `CONNECT_SERVER`/`CONNECT_API_KEY` set in the environment. Choose by what you
> have:
>
> - **`CONNECT_SERVER` and `CONNECT_API_KEY` are set** (typical headless/automated
>   run) → do **not** pass `-n`; let the env vars supply the target and key.
>   Deploy with just `posit connect deploy <framework> <dir>`.
> - **The request names a specific saved server** (e.g. "deploy to dogfood") →
>   use `-n dogfood`, and make sure `CONNECT_SERVER`/`CONNECT_API_KEY` are **not**
>   also exported for that command (`unset` them, or don't run `posit connect add`
>   from a shell that has them set).
>
> If you have env-var creds but the request also names a server, prefer the env
> vars (drop `-n`) — mixing is what triggers the rejection.

### R (`rsconnect`)

Register the server and API user as shown in Stage 3
(`addServer()` + `connectApiUser()`), pulling the key from `CONNECT_API_KEY`.
Check for already-linked accounts first:

```r
rsconnect::accounts()   # lists linked servers/accounts; empty => authenticate
```

### If credentials are missing

- If you have an **ask-user / prompt tool**, ask the user for the server URL and
  API key.
- Otherwise, rely on the `CONNECT_SERVER` / `CONNECT_API_KEY` env vars and, if
  they're absent, **report the missing credentials** rather than guessing.

---

## Stage 6 — Deploy and handle failure

### Discover the live command surface (Python)

The `posit connect deploy` commands track upstream and their flags can change,
so **read the help text — it's the source of truth**:

```console
posit connect deploy --help              # every framework you can deploy
posit connect deploy <framework> --help  # flags for one framework
```

### Deploy

```console
posit connect deploy streamlit ./my-app
posit connect deploy shiny ./my-shiny-app
posit connect deploy fastapi ./my-api
posit connect deploy quarto ./report
posit connect deploy manifest ./manifest.json   # a prepared bundle
```

For R, run the `deployApp()` / `deployDoc()` / `deploySite()` call from Stage 3.

### Resolving `posit` not found

The `posit` CLI may be installed but not on `PATH` in the current shell (common
in IDE-spawned terminals or when a virtualenv is active). Check with
`uv tool list | grep posit-cli`; if it's installed, invoke it via `uv tool run`:

```console
uv tool run --from posit-cli posit connect deploy shiny ./my-app -n myserver
```

**Critical:** always pass `--from posit-cli` — a bare `uv tool run posit`
resolves an unrelated PyPI package and will fail.

If it's not installed, install it (Stage 4) or fall back to rsconnect-python
(Stage 3, route 2).

### Pre-flight check (optional)

Before deploying, verify CLI access:

```console
posit connect list 2>/dev/null || uv tool run --from rsconnect-python rsconnect list
```

### When a deploy fails

**Python:**

- Auth errors: confirm the target with `posit connect list`, re-run
  `posit connect login`, or pass `-s`/`-k` (or set
  `CONNECT_SERVER`/`CONNECT_API_KEY`).
- Self-signed TLS: use `-i/--insecure` (or `-c/--cacert <file>`); set
  `CONNECT_INSECURE` to apply it everywhere.
- Rejected flag: re-read `posit connect deploy <framework> --help` — a rejected
  flag usually means it moved or changed upstream.

**R:**

- "No account" / auth errors: run `rsconnect::accounts()`; if empty, re-run
  `rsconnect::addServer()` + `rsconnect::connectApiUser()`. Double-check you used
  `connectApiUser` (server), not `connectCloudUser` (Cloud).
- Wrong deploy function: use `deployApp()` for directories/apps, `deployDoc()`
  for a single document, `deploySite()` for a site.
- Self-signed TLS: pass the CA bundle via the `RETICULATE`/`curl` options or
  add the server with the appropriate certificate; for quick tests set
  `options(rsconnect.check.certificate = FALSE)` (use sparingly).
- Absolute-path warnings: files with hard-coded absolute paths won't block the
  deploy but should be made relative to the project directory.

---

## R `rsconnect` functions reference (Connect server)

| Function | Purpose |
| --- | --- |
| `addServer(url, name)` | Registers a Connect **server** under a local nickname |
| `connectApiUser(server, account, apiKey)` | Authenticates an API user against a Connect **server** (use this, **not** `connectCloudUser`) |
| `accounts()` | Lists linked servers/accounts |
| `deployApp(appDir, appTitle)` | Deploys a directory app — Shiny for R, Plumber, etc. |
| `deployDoc(doc)` | Deploys a single document (Rmd, qmd) |
| `deploySite(siteDir)` | Deploys a full R Markdown / Quarto site |
| `writeManifest()` | Generates `manifest.json` (for the rsconnect-python / no-R route) |
| `removeAccount(name)` | Removes a stored account from the local machine |
