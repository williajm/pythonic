# Security policy

## Reporting a vulnerability

Report suspected vulnerabilities privately via GitHub's
[private vulnerability reporting](https://github.com/williajm/pythonic/security/advisories/new)
— please do not open a public issue. Expect an initial response within a
week.

## Scope

pythonic is an educational repository: a stdlib-only example package, its
test suite, and a static documentation site. It ships no service, parses
no untrusted input, and is not published to PyPI (the
`Private :: Do Not Upload` classifier blocks accidental uploads). The
security-relevant surface is the supply chain and the CI/deploy pipeline.

## Supply-chain measures

- Dependencies are locked with hash verification against PyPI only, and
  no dependency may be locked to a version published within the last
  7 days (`tool.uv.exclude-newer` in `pyproject.toml`).
- GitHub Actions are pinned to commit SHAs; Dependabot alerts on security
  advisories only (routine pin refreshes are manual, under the same
  7-day cooldown).
- Workflows run with least privilege (`contents: read`) and checkouts do
  not persist credentials; the Pages deploy uses OIDC, not stored
  credentials.
- The lockfile is audited for known CVEs (`pip-audit`) on every CI run.
- `main` is protected: changes arrive by pull request with required
  status checks, enforced for administrators, with force pushes and
  deletions refused.
