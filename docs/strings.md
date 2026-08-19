# Strings

Python has retired three generations of formatting — `%`, `.format()`,
manual concatenation — in favour of f-strings: the expression sits where
its value will appear. And Python 3.14 adds a fourth generation for a
different job entirely.

## The habit — and the bug we didn't know we'd written

```python
--8<-- "src/pythonic/strings.py:unpythonic"
```

True story, preserved in the docstring: this counter-example was first
published claiming the `if result:` bookkeeping was merely *noisy*. Then
property-based testing ([hypothesis](https://hypothesis.readthedocs.io/))
ran the equivalence test over arbitrary inputs and found `["", ""]` —
an empty name early in the list makes `result` falsy, so the next
separator is silently dropped. The "noise" was a bug.

We kept the bug, documented it, and added a regression test, because no
argument for `str.join` is stronger than this one: **bookkeeping you
write is bookkeeping you get wrong** — and we're the ones writing the
lesson.

## The idiom

```python
--8<-- "src/pythonic/strings.py:pythonic"
```

The separator calls the shot: one method, no bookkeeping, linear time
guaranteed. And in `receipt_line`, the f-string format spec handles
alignment, padding, and precision — including a *nested* interpolation
for the width.

## New in 3.14: t-strings

```python
--8<-- "src/pythonic/strings.py:tstrings"
```

An f-string hands you finished text; a t-string
([PEP 750](https://peps.python.org/pep-0750/)) hands you the **parts** —
static text and interpolations, separately — so library code decides how
values are rendered: escaped for HTML, parameterised for SQL, or, here,
redacted for a log line. It is the language's answer to a real security
lesson: eagerly gluing untrusted values into strings is how injection
bugs are born.

!!! warning "When not to"
    - f-strings are for *humans reading output*. For logging, prefer
      lazy `%`-style arguments (`logger.info("user %s", name)`) so the
      formatting cost is only paid when the record is emitted.
    - t-strings are brand new: reach for them when a library defines the
      rendering contract, not as a reflex. Honesty note: the ecosystem is
      still catching up to them.
