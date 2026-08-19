# Context managers

`with` is Python's answer to resource leaks: the cleanup runs whether the
block finishes, returns, or raises. Anything that must be undone — closing
a file, releasing a lock, restoring state — belongs in one.

## The habit

```python
--8<-- "src/pythonic/context_managers.py:unpythonic"
```

The leak hides between the lines: if `readline` raises, `close` never runs.
Code like this passes every happy-path test ever written for it.

## The idiom

```python
--8<-- "src/pythonic/context_managers.py:pythonic"
```

Returning from inside the block is fine — the file still closes on the way
out. That is the whole contract: *any* exit runs the cleanup.

## The protocol is two methods

```python
--8<-- "src/pythonic/context_managers.py:class"
```

The tests exercise the path that matters: an exception inside the block
still records the elapsed time, and the exception still escapes.

## Or one decorated generator

```python
--8<-- "src/pythonic/context_managers.py:contextlib"
```

`@contextmanager` is the lightweight form — setup before `yield`, cleanup
in the `finally`. And `contextlib.suppress` names an intent that
try/except/pass only mumbles.

!!! warning "When not to"
    Not every pair of actions is a resource. If there is nothing that
    *must* run on the error path, a context manager is ceremony. And for
    cleanup spanning many resources with dynamic lifetimes, reach for
    `contextlib.ExitStack` rather than nesting `with` five deep.
