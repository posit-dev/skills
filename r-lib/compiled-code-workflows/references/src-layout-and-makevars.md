# `src/` layout and Makevars

This reference focuses on the practical contract between your package and the R build system.

## The shape of `src/`

Typical files:

- `src/*.c`, `src/*.cpp`, `src/*.f`, `src/*.f90` — your sources
- `src/Makevars` — compiler/linker flags for Unix-like platforms
- `src/Makevars.win` — compiler/linker flags for Windows

R will compile sources under `src/` and link them into a shared object that is loaded by `.Call()` / `.C()` / `.Fortran()`.

## When you actually need `Makevars`

You usually add `Makevars` when you need to:

- add include paths (headers)
- link to a library
- define compile-time macros

## Common variables

You’ll most often see:

- `PKG_CPPFLAGS` — include paths and preprocessor flags
- `PKG_CFLAGS` / `PKG_CXXFLAGS` — compiler flags
- `PKG_LIBS` — libraries to link against

Keep flags minimal; prefer portable flags.

## Windows vs Unix differences

- Prefer `src/Makevars.win` for Windows-specific flags.
- Don’t assume `pkg-config` is present.
- Linking behavior differs across platforms; if you depend on a system library, expect platform-specific installation instructions.

## Common mistakes

- Putting `-I` / `-L` flags in the wrong variable.
- Hard-coding absolute paths.
- Assuming a library is present on all machines.

## Related

- [linkingto-and-systemrequirements.md](linkingto-and-systemrequirements.md)
- [toolchains-and-ci.md](toolchains-and-ci.md)
