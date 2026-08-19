# Pattern matching

`match` (Python 3.10+) is not a switch statement. A case can pull a value
apart, bind its pieces, and guard on them in one clause — and paired with
a closed union of dataclasses, it gives Python honest sum types.

## Sum types, checked for exhaustiveness

```python
--8<-- "src/pythonic/pattern_matching.py:commands"
```

The `type Command = ...` alias (PEP 695 syntax) closes the union, and
`assert_never` is the payoff: if a new variant joins `Command` and no case
handles it, **mypy fails the build** — the missing case is caught before
the code ever runs. This repository's CI enforces exactly that.

## Matching on the shape of data

```python
--8<-- "src/pythonic/pattern_matching.py:shapes-of-data"
```

Sequence patterns, mapping patterns, class patterns, and guards in one
place — the kind of destructuring that would otherwise be a ladder of
`isinstance` calls and manual indexing. Order matters: the first matching
case wins.

!!! note "Honest wrinkles, tested"
    - `True` matches `case int()` because `bool` subclasses `int` — a
      test documents it rather than hiding it.
    - A mapping with *extra* keys still matches `case {"name": str(name)}`
      — mapping patterns ignore keys they don't mention. Also tested.

!!! warning "When not to"
    Dispatching on a plain value (`match status: case 404:`) buys nothing
    over `if/elif` except novelty. Reach for `match` when there is
    *structure to destructure* — variants, shapes, nested data. And note
    the venerable pythonic alternative for value→value mapping: a dict.
