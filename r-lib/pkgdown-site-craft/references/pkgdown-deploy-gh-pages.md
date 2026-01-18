# Deploying pkgdown to GitHub Pages

## usethis setup

A common starting point:

```r
usethis::use_pkgdown_github_pages()
```

This typically scaffolds pkgdown config and a GitHub Actions workflow to build/deploy the site.

If you already have a pkgdown setup and just want the workflow, you can also use:

```r
usethis::use_github_action("pkgdown")
```

## Key deployment considerations

- Ensure `_pkgdown.yml` has a correct `url`.
- Ensure the site is built from a clean checkout in CI.
- If your site includes articles/vignettes that need suggested packages, CI must install them.

## GitHub Pages settings (common gotcha)

The r-lib/actions `pkgdown` workflow commonly deploys the built site (the `docs/` folder) to the `gh-pages` branch.

In your GitHub repository settings, set Pages to publish from:

- branch: `gh-pages`
- folder: `/` (root)

If Pages is not configured to use `gh-pages`, deployment can “work” but nothing will be published.

## Permissions

Deployment requires write permissions to push the built site branch:

- workflow `permissions: read-all` at the top level (safe default)
- job `permissions: contents: write` for the deploy job

If you see permission errors, start by confirming these.

## Debugging deployment failures

- Rebuild locally with `pkgdown::build_site()`.
- Confirm docs are current: `devtools::document()`.
- Check CI logs for missing system dependencies or packages.

When debugging CI-only failures, common causes include:

- missing system libraries needed by a suggested package
- vignettes that assume interactive state or local files
- undeclared dependencies used in examples
