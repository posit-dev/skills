# `data-raw/` workflow for internal datasets

Use `data-raw/` scripts to generate small, curated datasets that ship under `data/`.

## Recommended workflow

1. Create a script:

- `data-raw/mydata.R`

2. In that script:

- read raw inputs (often outside the package, or in `inst/extdata` for small inputs)
- clean and reduce
- save a compact dataset

3. Save the dataset using usethis:

```r
usethis::use_data(mydata, overwrite = TRUE)
```

4. Ensure that raw inputs and intermediate artifacts do not inflate your tarball

- keep large raw sources out of the package
- use `.Rbuildignore` for local-only artifacts

## Rules of thumb

- Keep shipped datasets small and well-documented.
- Prefer storing just what users need (not full raw dumps).

## Related

- [compression-and-rda.md](compression-and-rda.md)
- [deciding-what-ships.md](deciding-what-ships.md)
