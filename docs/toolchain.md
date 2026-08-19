# The toolchain

Pythonic is not just syntax. Half of what makes Python great in 2026 is
the tooling around it — and this repository practises what it preaches.
Everything below is enforced by CI on every pull request; none of it is
aspirational.

## uv — environments you can reproduce

[uv](https://docs.astral.sh/uv/) manages the Python version
(`.python-version` pins 3.14), the virtual environment, and the lockfile.
`uv sync --locked` in CI guarantees the tested environment is byte-for-byte
the one the lockfile describes, hash-verified against PyPI.

The examples themselves have **zero runtime dependencies** — everything
taught here is standard library. That is part of the lesson: Python's
batteries really are included.

## ruff — every rule it has

The linter runs with `select = ["ALL"]`: every rule ruff ships, with three
narrowly-scoped exceptions documented in `pyproject.toml`. Where a
deliberate counter-example trips a rule, it carries an inline
`noqa: <code>` naming the rule at that exact line — which is itself
educational: PERF401 knows the append loop should be a comprehension,
PTH118 knows the string join should be a `Path`. The linter has read more
Python style arguments than any of us; when it can name your habit,
listen.

## mypy --strict — claims, checked

Every signature in `src/` and `tests/` is fully typed and checked with
`mypy --strict`. This is what turns documentation claims into build
failures: pass `total_area` an object without `.area()` and mypy objects;
add a variant to `Command` without a `case` and `assert_never` fails the
build.

## pytest, coverage, hypothesis — the honesty enforcement

- **100% line and branch coverage, enforced.** The docs embed source files
  directly, so an untested line would mean the site shows unverified code.
  The build fails below 100%.
- **Equivalence tests.** Each counter-example is tested to produce the
  same results as the idiom — the honest version of "this is worse".
- **Property-based testing.** [hypothesis](https://hypothesis.readthedocs.io/)
  generates adversarial inputs for the equivalence claims. It has already
  [caught one real bug](strings.md) in a counter-example we believed was
  merely ugly.

## Supply-chain security

Educational repositories get cloned and copied; shipping secure defaults
is part of being honest. The measures, all visible in the repo:

- **Locked, hash-verified dependencies** against PyPI only, with a 7-day
  cooldown: resolution ignores anything published in the last week
  (`tool.uv.exclude-newer`), so a freshly-poisoned package version can't
  reach the lockfile the day it lands.
- **GitHub Actions pinned to commit SHAs** — tags can be moved, SHAs
  cannot. Dependabot watches for security advisories.
- **Least-privilege workflows**: CI runs with `contents: read` and
  checkouts don't persist credentials.
- **`pip-audit` on every CI run** checks the lockfile against known CVEs.
- **Branch protection on `main`**: changes arrive by pull request, checks
  must pass, force pushes are refused — for administrators too.

None of this is exotic; all of it is copyable. Take it.
