# Paths

`os.path` works on strings: every operation is a free function, every join
is a separator bug waiting for a Windows machine. `pathlib.Path` puts the
operations on the object.

## The habit

```python
--8<-- "src/pythonic/paths.py:unpythonic"
```

Strings in, strings out, and a nested loop to express what one glob says.
The `noqa: PTH118` is ruff's flake8-use-pathlib plugin objecting to the
manual join — again, when the linter can name the habit, the language has
the idiom.

## The idiom

```python
--8<-- "src/pythonic/paths.py:pythonic"
```

`rglob` does the walking, the filtering, and the joining. A test proves
both versions find the same files — the objection is the plumbing, not
the result.

## Joining, reading, and one deliberate keyword

```python
--8<-- "src/pythonic/paths.py:operations"
```

Two details worth their weight:

- `base / str(year) / f"{name}.csv"` — the `/` operator makes path
  assembly read like a path, with the OS-specific separator handled by
  the object.
- `encoding="utf-8"` is explicit because relying on the platform default
  is how "works on my machine" bug reports are born. (Python 3.15 will
  finally make UTF-8 the default; being explicit is correct on every
  version.)

!!! warning "When not to"
    APIs that traffic in strings (subprocess argv lists, some C
    extensions) are happier with `str(path)` at the boundary — convert at
    the edge, keep `Path` objects inside. And for millions of files on a
    hot path, `os.scandir` is measurably faster than `pathlib`; when
    profiling says so, say so in a comment and use it.
