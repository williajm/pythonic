# pythonic

[![CI](https://github.com/williajm/pythonic/actions/workflows/ci.yml/badge.svg)](https://github.com/williajm/pythonic/actions/workflows/ci.yml)
[![Site](https://img.shields.io/badge/site-williajm.github.io%2Fpythonic-blue)](https://williajm.github.io/pythonic/)
[![Python 3.14](https://img.shields.io/badge/python-3.14-blue)](https://www.python.org/downloads/)

**What makes Python great — honest, tested examples of pythonic code.**

📖 **Read the site: [williajm.github.io/pythonic](https://williajm.github.io/pythonic/)**

Ten short chapters, each contrasting a common habit with the pythonic
alternative, on the latest stable Python (3.14) — comprehensions,
iteration, generators, context managers, EAFP, records, protocols,
pattern matching, paths, and strings.

## The honesty rules

1. **Every code block on the site is real** — embedded straight from
   [`src/pythonic/`](src/pythonic/), which CI holds to 100% line *and*
   branch coverage. The site cannot show code the tests don't run.
2. **The counter-examples work too.** Tests prove the "unpythonic"
   versions produce the same results — except where they genuinely
   don't, and then the bug is tested and documented. (Property-based
   testing has already caught
   [one real bug](https://williajm.github.io/pythonic/strings/) in a
   counter-example we believed was merely ugly.)
3. **Every chapter has a "when not to" clause.** Idioms oversold become
   cargo cults.
4. **When the stdlib already ships the answer, we say so.**

## Try it

```bash
git clone https://github.com/williajm/pythonic.git
cd pythonic
uv sync --all-groups
uv run pytest            # 73 tests, 100% coverage floor
uv run mkdocs serve      # the site, locally
```

The example package has **zero runtime dependencies** — everything it
teaches is standard library. The dev tooling is the modern Python stack:
[uv](https://docs.astral.sh/uv/), [ruff](https://docs.astral.sh/ruff/)
with `select = ["ALL"]`, `mypy --strict`,
[pytest](https://docs.pytest.org/) +
[hypothesis](https://hypothesis.readthedocs.io/), and
[mkdocs-material](https://squidfunk.github.io/mkdocs-material/).

## Security

Supply-chain hygiene is part of the curriculum: locked and hash-verified
dependencies with a 7-day cooldown, SHA-pinned actions, least-privilege
workflows, `pip-audit` in CI, and a protected `main`. Details in
[SECURITY.md](SECURITY.md) and on
[the toolchain page](https://williajm.github.io/pythonic/toolchain/).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). PRs only — `main` is protected.

## License

[MIT](LICENSE).
