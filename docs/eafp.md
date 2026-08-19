# EAFP

"Easier to Ask Forgiveness than Permission": attempt the operation and
handle the exception, rather than checking preconditions first ("look
before you leap"). The deeper reason is correctness, not style — a
pre-check is a *second implementation* of the operation's rules, and
second implementations drift.

## The habit — wrong in both directions

```python title="src/pythonic/eafp.py"
--8<-- "src/pythonic/eafp.py:lbyl"
```

This is the strongest example in the repository, because the check isn't
just redundant — it is **wrong twice**, and the test suite pins both bugs:

- `"-3".isdigit()` is `False`, so valid input is rejected.
- `"³".isdigit()` is `True`, so the "guarded" `int("³")` raises anyway.

The guard *looks* like safety. It is actually a second, worse parser.

## The idiom

```python title="src/pythonic/eafp.py"
--8<-- "src/pythonic/eafp.py:eafp"
```

There is exactly one authority on what `int` accepts: `int`.

## Missing keys, and the honest ending

```python title="src/pythonic/eafp.py"
--8<-- "src/pythonic/eafp.py:counter"
```

`dict.get(key, default)` folds "first time seen" into the normal path —
worth knowing. But honesty compels the second function:
`collections.Counter` already does this, plus `most_common` and
arithmetic. A test verifies the two agree.

!!! warning "When not to"
    EAFP is a default, not a dogma. Look before you leap when failure has
    side effects that an exception won't undo, when the check genuinely
    *is* the business rule (validating user input deserves real messages,
    not `ValueError` pass-through), or when exceptions would fire on every
    other call and the cost matters. What EAFP really retires is the
    *redundant* pre-check — the one duplicating rules the operation
    already enforces.
