# Contributing

Thanks for your interest! This repository is deliberately strict — the
tooling is part of what it teaches.

## Setup

Install [uv](https://docs.astral.sh/uv/), then:

```bash
uv sync --all-groups   # Python 3.14 venv + dev and docs dependencies
```

## The gate

Everything CI runs, runnable locally:

```bash
uv run ruff format .          # format (CI checks with --check)
uv run ruff check .           # lint, select = ALL
uv run mypy                   # strict, src and tests
uv run pytest                 # tests + 100% line/branch coverage floor
uv run mkdocs build --strict  # docs build, snippets verified
uv run mkdocs serve           # live-preview the site
```

## Ground rules

- **Honesty is the house style.** Counter-examples must be tested, edge
  cases documented rather than hidden, and "when not to" clauses kept.
  If the stdlib already ships the answer, the example must say so.
- **Every snippet the site shows comes from `src/` via snippet markers**
  (`--8<--`). Don't paste code into the docs directly.
- **Suppressions are granted per line, never per file**: an inline
  `noqa: <code>` with a comment saying why, at the exact line that
  earned it.
- **PRs only.** `main` is protected; branch, push, open a pull request,
  and let CI decide.

<!-- TODO: add a pre-commit config mirroring the CI gate (ruff format,
     ruff check, mkdocs build) so contributors catch failures before
     pushing. Deferred from the initial scaffold. -->
