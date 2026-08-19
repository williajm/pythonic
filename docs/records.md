# Records

A class that exists to hold named fields should not hand-roll `__init__`,
`__repr__`, and `__eq__`. The language writes them for you, correctly,
from the field declarations.

## The habit

```python title="src/pythonic/records.py"
--8<-- "src/pythonic/records.py:unpythonic"
```

The hand-written dunders *work* — the tests prove it. The objection is the
maintenance contract: add a field and you must remember `__init__`,
`__repr__`, `__eq__`, **and** `__hash__`, or equality silently lies.

And one trap in this class has already sprung: it is hashable **and**
mutable. Store a point in a set, mutate it, and it becomes unfindable —
the set filed it under the old hash. A test pins that failure down. The
generated version refuses to make this mistake: a plain `@dataclass` sets
`__hash__` to `None`, and only `frozen=True` buys hashability back — by
removing the mutability that made it dangerous.

## The idiom

```python title="src/pythonic/records.py"
--8<-- "src/pythonic/records.py:pythonic"
```

Two field declarations replace sixteen lines, and the extras are free:

- `frozen=True` makes instances immutable — and therefore safely hashable.
- `slots=True` drops the per-instance `__dict__`, cutting memory and
  turning attribute typos into immediate `AttributeError`s.
- The unquoted `Point` annotation inside its own class is Python 3.14's
  lazy annotations (PEP 649) at work: no quotes, no `__future__` import.

## When you really do want a tuple

```python title="src/pythonic/records.py"
--8<-- "src/pythonic/records.py:namedtuple"
```

`NamedTuple` keeps tuple behaviour — unpacking, ordering, compatibility
with tuple-expecting APIs — while call sites read `reading.value`, not
`r[1]`.

!!! warning "When not to"
    Dataclasses do **containment, not validation**: `Point("a", "b")` is a
    type error mypy will catch, but nothing stops it at runtime. When data
    crosses a trust boundary — user input, APIs, files — use an
    established validation library (pydantic, or attrs with validators)
    rather than reinventing one. And a class with real invariants and
    behaviour deserves a hand-written `__init__` that enforces them; not
    everything is a record.
