# Toolchains and CI (Windows/macOS/Linux)

Most compiled-code pain is toolchain friction. Treat CI failures as signal, not noise.

## Toolchain expectations (high level)

- Windows: Rtools toolchain must be installed and discoverable.
- macOS: Xcode command line tools are commonly required.
- Linux: build-essential toolchain is commonly required.

## CI strategy

- Use `r-lib/actions` `check-standard` as a baseline.
- If you depend on a system library, add explicit OS-specific install steps before installing R deps.

## Debugging tactics

- Always capture the full compiler and linker output.
- Reduce to one translation unit when chasing an include/link issue.
- Confirm you’re not accidentally compiling with different standards/flags across OSs.

## Common failure patterns

- “C++ compiler cannot create executables” → toolchain missing/misconfigured.
- “header.h: No such file or directory” → include paths or missing dev headers.
- “ld: library not found” / “cannot find -lxxx” → linker flags or missing libs.

## References

- r-lib/actions: https://github.com/r-lib/actions
- CRAN policy (external libraries, portability): https://cran.r-project.org/web/packages/policies.html
