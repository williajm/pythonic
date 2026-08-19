# Iteration

Most index arithmetic in Python is a C habit wearing a snake costume. The
`for` loop already iterates; `enumerate` already counts; `zip` already pairs.

## The habit

```python title="src/pythonic/iteration.py"
--8<-- "src/pythonic/iteration.py:unpythonic"
```

`range(len(items))` forces every read through a subscript — and quietly
narrows the function to `Sequence`, when the natural version accepts any
iterable.

## Counting: enumerate

```python title="src/pythonic/iteration.py"
--8<-- "src/pythonic/iteration.py:enumerate"
```

## Pairing: zip, strictly

```python title="src/pythonic/iteration.py"
--8<-- "src/pythonic/iteration.py:zip"
```

`strict=True` deserves its own sentence: without it, sequences of different
lengths are *silently truncated* — a bug class that vanishes the day you
make mismatch an error. Ruff (B905) insists on choosing one or the other
explicitly. There is a test that feeds `pair_scores` mismatched input and
asserts the `ValueError`.

## Unpacking: let the target mirror the data

```python title="src/pythonic/iteration.py"
--8<-- "src/pythonic/iteration.py:unpacking"
```

No slices, no temporaries, no off-by-one opportunities. The `head, *rest`
target and the `second, first` return read as the shapes they produce.

!!! warning "When not to"
    Sometimes you genuinely need the index for its own sake — binary search,
    in-place swaps, parallel writes into a preallocated buffer. Indexing is
    a tool, not a sin; the habit to retire is indexing as the *default* way
    to visit elements.
