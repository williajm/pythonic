# Protocols

Python has always cared about what an object *can do*, not what it *is* —
"if it quacks like a duck". `typing.Protocol` writes the quacking down, so
a type checker can verify it without anyone inheriting anything.

## The idiom

```python title="src/pythonic/protocols.py"
--8<-- "src/pythonic/protocols.py:protocol"
```

`total_area` names only the capability it needs. mypy checks every caller
*structurally*: pass an object without an `area()` method and the build
fails — this repository runs `mypy --strict` in CI, so that claim is
enforced, not aspirational.

## Implementations that never heard of the protocol

```python title="src/pythonic/protocols.py"
--8<-- "src/pythonic/protocols.py:shapes"
```

Neither shape imports `HasArea`, inherits from it, or registers with it.
One test drives the point home by defining a `Triangle` class *inside the
test function* — it satisfies the protocol by shape alone.

This is the pythonic middle path: the flexibility of duck typing with the
verification of static types. The alternative — an abstract base class
that every implementation must import and subclass — couples modules that
had no other reason to meet, and is closed to types you don't own.

!!! warning "When not to"
    - Protocols check *shape*, not *meaning*: any `area() -> float` method
      satisfies `HasArea`, even one returning a temperature. Names and
      docs still carry the semantics.
    - `isinstance` checks need `@runtime_checkable`, and even then only
      method *presence* is checked at runtime, not signatures.
    - When you own all the implementations and want shared behaviour, an
      abstract base class with concrete helper methods is the better tool
      — inheritance is not the enemy; *mandatory* inheritance is.
