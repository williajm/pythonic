# Context managers

`with` is Python's answer to resource leaks: the cleanup runs whether the
block finishes, returns, or raises. Anything that must be undone — closing
a file, releasing a lock, restoring state — belongs in one.

## The habit

```python title="src/pythonic/context_managers.py"
--8<-- "src/pythonic/context_managers.py:unpythonic"
```

The leak hides between the lines: if `readline` raises, `close` never runs.
Code like this passes every happy-path test ever written for it.

## The idiom

```python title="src/pythonic/context_managers.py"
--8<-- "src/pythonic/context_managers.py:pythonic"
```

Returning from inside the block is fine — the file still closes on the way
out. That is the whole contract: *any* exit runs the cleanup.

## The protocol is two methods

```python title="src/pythonic/context_managers.py"
--8<-- "src/pythonic/context_managers.py:class"
```

The tests exercise the path that matters: an exception inside the block
still records the elapsed time, and the exception still escapes.

## Or one decorated generator

```python title="src/pythonic/context_managers.py"
--8<-- "src/pythonic/context_managers.py:contextlib"
```

`@contextmanager` is the lightweight form — setup before `yield`, cleanup
in the `finally`. Note what makes this example's cleanup trustworthy: it
owns *a key*, not a position, so nothing the block does elsewhere in the
mapping can make it restore the wrong thing (there is a test where the
block rewrites the managed key and grows the mapping — the cleanup still
restores exactly its own entry). Honesty note: `unittest.mock.patch.dict`
and pytest's `monkeypatch.setitem` are the battle-hardened versions of
this idea; this one shows the mechanics.

And `contextlib.suppress` names an intent that try/except/pass only
mumbles.

!!! warning "When not to"
    Not every pair of actions is a resource. If there is nothing that
    *must* run on the error path, a context manager is ceremony. And for
    cleanup spanning many resources with dynamic lifetimes, reach for
    `contextlib.ExitStack` rather than nesting `with` five deep.
