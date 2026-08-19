# Generators

A generator function looks like a normal function but `yield`s a stream.
Nothing runs until someone asks for the next value — so pipelines stay flat
in memory, and infinite sequences become ordinary objects.

## The habit

```python title="src/pythonic/generators.py"
--8<-- "src/pythonic/generators.py:unpythonic"
```

The eager version works — the tests prove it — but it scales with the size
of the *source*, not the size of the answer. And it needs that arbitrary
100,000 cap, because "all the squares" is not a list you can build.

## The idiom

```python title="src/pythonic/generators.py"
--8<-- "src/pythonic/generators.py:pythonic"
```

`squares()` is an *infinite sequence* in seven lines: state lives in the
paused function frame. `take(n, ...)` consumes exactly n items and not
one more — and a test with a counting source verifies the *consumption*,
not just the returned values, so that claim is measured rather than
assumed.

## Lazy pipelines

```python title="src/pythonic/generators.py"
--8<-- "src/pythonic/generators.py:pipeline"
```

`first_match` short-circuits: a spy predicate in the tests confirms nothing
after the first hit is ever examined.

!!! note "Honesty clause"
    `running_total` exists to show the mechanics — the stdlib already ships
    it as `itertools.accumulate`, and a test verifies ours matches. Knowing
    how to write a generator matters; knowing `itertools` already wrote it
    matters more.

!!! warning "When not to"
    A generator can be consumed **once**, has no `len()`, and cannot be
    indexed. If the caller needs to look twice, hand over a list and say
    so. Laziness is a strategy, not a virtue.
