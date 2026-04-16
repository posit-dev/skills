Read @../../SKILL.md

Create an R CLI tool called `dotenv` (save it as `dotenv.R`) for managing environment variables in `.env` files. It should have:

- A global `--file` option (defaults to `.env`) that controls which `.env` file to use
- Three subcommands:
  - `get` — looks up a key and prints its value. Takes a positional `key` argument.
  - `set` — sets a key-value pair. Takes positional `key` and `value` arguments.
  - `list` — prints all key-value pairs. Has a `--sort` boolean flag (default FALSE) to sort alphabetically.

Each subcommand should have a title and description for help text.
