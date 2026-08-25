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
  version: "4.0"
---

<!--
Maintainer note: edit this skill in posit-dev/connect only.
Downstream copies are overwritten by the sync workflow.
-->

# Deploying to Posit Connect

This guide covers Python and R content on a Posit Connect server. Work through the stages in order.

Two toolchains do the work:

- Python — [rsconnect-python](https://github.com/posit-dev/rsconnect-python), which provides the `rsconnect` CLI and is published on PyPI.
- R — the R [`rsconnect`](https://rstudio.github.io/rsconnect/) package, pointed at a Connect server.

If the user asks a question ("how do I…", "what is the command…") rather than asking for a deploy, answer from this guide and stop.

At the end, report which server you deployed to, which content type you picked, any tool you installed, and any assumption you made.

---

## Stage 1 — Detect the content

Infer the language and framework from the files in the project directory. Common signals:

| Signal in project dir | Likely content |
| --- | --- |
| `app.py` | Python web app — Shiny for Python, Streamlit, Dash, Gradio, Panel, or Bokeh |
| `app.R`, or `ui.R` + `server.R` | Shiny for R |
| `plumber.R` / `entrypoint.R` containing `plumb()` | Plumber API (R) |
| `*.qmd` | Quarto document |
| `*.Rmd` | R Markdown |
| `*.ipynb` | Jupyter notebook / Voila |
| `manifest.json` | Prebuilt bundle — deploy it directly, no framework guess needed |

The imports in `app.py` name the framework:

```console
grep -Eo 'import (shiny|streamlit|dash|gradio|panel|bokeh)|from (shiny|streamlit|dash|gradio|panel|bokeh)' app.py
```

A bare ASGI or WSGI object means `fastapi` or `flask`.

Dependency files confirm the language: `requirements.txt` and `pyproject.toml` for Python, `DESCRIPTION` and `renv.lock` for R.

If the content is ambiguous (both Python and R files, or an `app.py` with no recognizable import), use your discretion, and report the assumption you made.

---

## Stage 2 — Inventory your tools

Probe the environment and build a capability set:

```console
command -v rsconnect                                 # rsconnect-python on PATH
command -v uv                                        # uv (installs and runs Python tools)
uv tool list 2>/dev/null | grep rsconnect            # rsconnect-python installed via uv
command -v Rscript                                   # R present
Rscript -e 'cat(requireNamespace("rsconnect", quietly=TRUE))' 2>/dev/null   # R rsconnect package
command -v quarto                                     # quarto CLI
command -v git                                        # git
```

With `uv` present, Python content needs no install step. `uv tool run --from rsconnect-python rsconnect ...` fetches and runs the CLI on demand.

---

## Stage 3 — Pick a route

Cross the detected content (Stage 1) with your capabilities (Stage 2).

### Python content

Use rsconnect-python. With `rsconnect` on `PATH`:

```console
rsconnect deploy <framework> ./my-app
```

Off `PATH` but with `uv` present:

```console
uv tool run --from rsconnect-python rsconnect deploy <framework> ./my-app
```

Both forms take identical arguments. The rest of this guide writes the bare `rsconnect ...` form. Prefix it with `uv tool run --from rsconnect-python` when you use the second route.

`<framework>` is one of `api`, `bokeh`, `bundle`, `dash`, `fastapi`, `flask`, `git`, `gradio`, `html`, `manifest`, `nodejs`, `notebook`, `panel`, `pyproject`, `quarto`, `shiny`, `streamlit`, `tensorflow`, `voila`. For anything outside that list, `rsconnect deploy other-content` prints guidance.

The frameworks and flags depend on the installed version, so confirm against `rsconnect deploy --help` rather than this list. If `uv tool run` resolves a stale cached version, pin it: `uv tool run --from 'rsconnect-python==1.30.0' rsconnect ...`.

### R content

Use the R `rsconnect` package, through `Rscript -e '...'` or an R session:

- Shiny for R, Plumber API, or any app directory → `deployApp()`
- A single R Markdown or Quarto document → `deployDoc()`
- A full R Markdown or Quarto site → `deploySite()`

If `Rscript` is absent, deploy the R content through rsconnect-python with a `manifest.json`:

- A `manifest.json` already exists — deploy it directly:
  ```console
  rsconnect deploy manifest ./manifest.json
  ```
- No manifest, but R is available elsewhere — generate one first with `rsconnect::writeManifest()` (see Stage 5).
- Neither R nor a manifest — a valid R bundle is not possible. Surface this as a blocker: ask the user or report it clearly.

### Quarto content

```console
rsconnect deploy quarto ./report
```

R-flavored Quarto (a `.qmd` with R code chunks) needs R to render. If R is absent, treat the document as R content and use the manifest route, or surface the gap.

---

## Stage 4 — Find the target and check its credentials

Now that the tool is known, find out which server to deploy to and whether the tool can already reach it. This is a check, not a login.

**Do not search the environment for API keys.** Do not read `CONNECT_API_KEY`, `CONNECT_SERVER`, a `.env` file, a keychain entry, or any other stored secret to pick a target or to register a server. Do this only when the user explicitly asks for it. An environment variable is not a request to use it.

List the accounts the tool already has. This is the only credential check you need.

```console
rsconnect list                                   # Python: saved servers, stored tokens, and the default server on 1.30.0+
Rscript -e 'print(rsconnect::accounts())'        # R: registered accounts
```

If the tool is not installed yet, close that gap in Stage 5 first. Then run the check.

Compare the result with the target the user named. Three outcomes:

- **An account matches the named target.** The credential path is live. Run no login and no `rsconnect add`. Continue to Stage 6 once the other gaps are closed.
- **The user named no target.** Ask them. List the servers the check found, and ask which one to deploy to, or whether they want a new target instead. Do not pick one for them, and do not deploy to the only saved server because it is the only one.
- **The target is new, or no account matches it.** This is a gap for Stage 5. Register it with a browser login.

A browser login is the way to register a new target:

```console
rsconnect login https://connect.example.com      # Python
```

```r
rsconnect::addServer(url = "https://connect.example.com", name = "myserver")   # R
rsconnect::connectUser(server = "myserver")
```

Both forms open a browser flow, so the user approves the login and no key passes through the conversation. The [credentials reference](#credentials-reference) has the details and the pitfalls.

---

## Stage 5 — Resolve gaps

When Stages 3 and 4 find a gap, close it, then include the action in your report.

**`rsconnect` not on `PATH`.** With `uv` present, no install is needed:

```console
uv tool run --from rsconnect-python rsconnect deploy <framework> ./my-app
```

If the user wants it installed persistently, or `uv tool run` is not viable:

```console
uv tool install rsconnect-python     # or: pip install rsconnect-python
```

The package name and the command name differ: the PyPI package is `rsconnect-python`, and the command it provides is `rsconnect`. That is why `uv tool run` needs `--from rsconnect-python`. To update later, run `uv tool upgrade rsconnect-python`.

**R `rsconnect` package missing, `Rscript` present.** Install it from Posit Package Manager (P3M), which serves precompiled Linux binaries. A binary install is much faster than a source build and needs no `-dev` system libraries. Binaries need two things: the `__linux__/<codename>` repo URL and a platform-identifying `HTTPUserAgent`. Without the user agent, P3M serves source.

```console
export P3M="https://packagemanager.posit.co/cran/__linux__/$(. /etc/os-release && echo "$VERSION_CODENAME")/latest"
Rscript -e '
  options(HTTPUserAgent = sprintf("R/%s R (%s)", getRversion(),
    paste(getRversion(), R.version["platform"], R.version["arch"], R.version["os"])))
  install.packages("rsconnect", repos = Sys.getenv("P3M"))
'
```

P3M binaries exist for x86_64 on common distros. On arm64 or an unsupported distro, P3M falls back to source. That result is still correct, only slower, and it needs the usual `-dev` libraries and a compiler. Use `https://cloud.r-project.org` (CRAN source) only when P3M is unreachable.

**`manifest.json` missing for R content, R present.** Generate it:

```console
Rscript -e 'rsconnect::writeManifest()'
```

rsconnect-python writes one for Python content:

```console
rsconnect write-manifest <framework> ./my-app
```

Then deploy the manifest with rsconnect-python if R cannot deploy directly.

**No account for the target.** Register it now with a browser login: `rsconnect login` for Python, or `rsconnect::addServer()` and `rsconnect::connectUser()` for R. The [credentials reference](#credentials-reference) has the details and the pitfalls. Do not fall back to an API key from the environment. If the browser flow is not available, report that and stop.

**Dependencies.** rsconnect and rsconnect-python scan the code and snapshot the required package versions for you, so hand-listing them is rarely necessary. Python content needs a `requirements.txt`. For R, the content's own packages must be installed locally for rsconnect to detect them — `plumber` for a Plumber API, `shiny` for a Shiny app. Install any that are missing from the same P3M repo shown above.

---

## Stage 6 — Deploy and handle failure

### Discover the live command surface (Python)

The frameworks and flags in rsconnect-python change between releases, and the help text is the source of truth:

```console
rsconnect version                  # which version you are actually running
rsconnect deploy --help            # every framework you can deploy
rsconnect deploy <framework> --help  # flags for one framework
```

### Deploy

For Python, run `rsconnect deploy <framework> <dir>` with the framework Stage 3 picked. The `manifest` framework takes the manifest file rather than a directory.

Non-obvious flags: `-t/--title`, `-N/--new` (force a new deployment instead of updating the recorded one), `-a/--app-id <id>` (target an existing item explicitly, mutually exclusive with `--new`), `-E NAME=VALUE` (set an environment variable, repeatable), `--draft` (keep serving the previous bundle until published).

For R, call the function Stage 3 selected. Pass `appTitle` so the content is not named after the directory.

### If `rsconnect` is not found at deploy time

It can be installed but off `PATH` in this shell. IDE-spawned terminals and active virtualenvs both cause this. Fall back to `uv tool run` as described in Stage 5, with `--from rsconnect-python`.

### Pre-flight check (optional)

To confirm that the target is reachable and the credentials work before you deploy:

```console
rsconnect details -n myserver
```

### When a deploy fails

Python:

- Auth errors — confirm the target with `rsconnect list`, then re-run `rsconnect login` (1.30.0+). Pass `-s`/`-k` only when the user told you to use an existing key.
- `-n/--name ... cannot be specified in conjunction with ... -s/--server (from ENVIRONMENT)` — `CONNECT_SERVER` is set and you also passed `-n`. Run `unset CONNECT_SERVER` and keep `-n`. The credentials reference explains why that direction. `CONNECT_API_KEY` can stay.
- `The requirements file 'requirements.txt' does not exist` — Python content needs one. Create it, point at another file with `--requirements-file`, or generate it with `--force-generate`. The last option runs a `pip freeze`, so it can over-pin.
- Self-signed TLS — use `-i/--insecure` or `-c/--cacert <file>`. Set `CONNECT_INSECURE` or `CONNECT_CA_CERTIFICATE` to apply it everywhere.
- Rejected flag or unknown framework — re-check `rsconnect version` and re-read `rsconnect deploy <framework> --help`. The installed version is usually older than the flag you used.

R:

- "No account" or auth errors — run `rsconnect::accounts()`. If it is empty, re-run `rsconnect::addServer()`, then `connectUser()` or `connectApiUser()`. Make sure that you used a server function and not `connectCloudUser()`.
- `Found multiple accounts. Please disambiguate by setting server and/or account` — more than one account is linked. Pass `account =` and `server =` explicitly to the deploy call. An interactive R session shows a menu instead, which hangs a headless run.
- Wrong deploy function — `deployApp()` for directories and apps, `deployDoc()` for a single document, `deploySite()` for a site.
- Self-signed TLS — pass the CA bundle through the `curl` options, or add the server with the certificate. For a quick test, set `options(rsconnect.check.certificate = FALSE)`.
- Absolute-path warnings — files with hard-coded absolute paths do not block the deploy, but they are better made relative to the project directory.

---

## Credentials reference

How to register a target that Stage 4 found no account for. If an account already matches the target, none of this is needed.

A browser login is the route. The API-key routes below it are there for one case only: the user explicitly tells you to use a key that already exists, in an environment variable or a credential store. Do not go looking for a key on your own, and never ask the user to give you one. An API key does not belong in the conversation.

### Python (rsconnect-python)

1. **OAuth login (interactive).** The default route. Needs rsconnect-python 1.30.0+, so check `rsconnect version` first. One browser flow per server. Tokens land in the OS keyring, or a local credential store, and refresh automatically.
   ```console
   rsconnect login https://connect.example.com
   rsconnect login https://connect.example.com --use-device-code   # headless
   ```
2. **Saved API-key nickname.** Only when the user asked for a key route. Save once, select later with `-n/--name`.
   ```console
   rsconnect add -n myserver -s https://connect.example.com -k <api-key>
   rsconnect list                    # confirm what is saved
   ```
   On 1.30.0+ a server can be the default, used when a command passes neither `-n` nor `-s`. `add` sets the default only with `--set-default`. `login` sets it unless you pass `--no-set-default`. `rsconnect server set-default -n <name>` changes it later. `CONNECT_SERVER` still takes precedence over the default.
3. **Environment variables.** Only when the user asked you to use them. rsconnect-python reads them directly, which suits a headless or automated run with no state to manage.
   ```console
   export CONNECT_SERVER=https://connect.example.com
   export CONNECT_API_KEY=...        # honored across the whole `rsconnect` surface
   ```
4. **Ad hoc flags** on the deploy command: `-s <url> -k <api-key>`. Same condition, and read the key from the variable the user named rather than writing it out.

Shared credential flags: `-n/--name` (saved server), `-s/--server` (env `CONNECT_SERVER`), `-k/--api-key` (env `CONNECT_API_KEY`), `-i/--insecure` (env `CONNECT_INSECURE`, for self-signed TLS), `-c/--cacert <file>` (env `CONNECT_CA_CERTIFICATE`).

> `-n` and `CONNECT_SERVER` cannot both be in play. rsconnect rejects a command that combines a saved-server name (`-n/--name`) with a server URL, including a URL that came from the environment: `-n/--name (from COMMANDLINE) cannot be specified in conjunction with options -s/--server (from ENVIRONMENT)`.
>
> Only the server conflicts. `CONNECT_API_KEY`, `CONNECT_INSECURE`, and `CONNECT_CA_CERTIFICATE` sit alongside `-n` without complaint, because the key is not part of the exclusion. `-n dogfood` with `CONNECT_API_KEY` exported is a valid command. It is `CONNECT_SERVER` that has to go.
>
> Choose by what the request names, not by what happens to be exported:
>
> - The request names a saved server ("deploy to dogfood") — use `-n dogfood` and `unset CONNECT_SERVER` for that command. Resolving the conflict the other way is worse: `CONNECT_SERVER` can point somewhere else entirely, so dropping `-n` to keep it would deploy to a server the user did not ask for.
> - The request names no server, the typical headless run — let `CONNECT_SERVER` and `CONNECT_API_KEY` supply the target, and deploy with `rsconnect deploy <framework> <dir>`.
>
> `CONNECT_SERVER` is not secret. Print it if you are unsure which server it points at, and name the server you deployed to in your report.

### R (`rsconnect`)

Register the server under a local nickname, then register your user against it:

```r
library(rsconnect)

# 1. The server (once per server; the name is a local nickname)
rsconnect::addServer(url = "https://connect.example.com", name = "myserver")

# 2a. Interactive — approve in a browser, no key to handle
rsconnect::connectUser(server = "myserver")

# 2b. Or non-interactively (CI), only when the user asked for a key route
rsconnect::connectApiUser(
  server  = "myserver",
  account = "your-username",
  apiKey  = Sys.getenv("CONNECT_API_KEY")
)
```

`connectCloudUser()` authenticates against Connect Cloud, a different service, so it does not work for a Connect server. Use `connectUser()` or `connectApiUser()` here.

### If the login route is not available

Report it and stop. Name the server you tried to register and say which login command failed. Do not search the environment, a `.env` file, or a credential store for a key to fill the gap, and do not ask the user for a key. The next step is theirs to choose.
