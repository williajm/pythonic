# Comprehensions

A comprehension states *what* the result contains; a loop describes *how* to
assemble it. When the transformation is one map/filter step, the declarative
form is shorter, faster, and has no moving parts to get wrong.

## The habit

```python title="src/pythonic/comprehensions.py"
--8<-- "src/pythonic/comprehensions.py:unpythonic"
```

Three lines of ceremony — create, append, return — wrapped around one line
of intent. Note the `noqa`: ruff's PERF401 flags this pattern out of the box.
When the linter can name your habit, the language has a better idiom for it.

## The idiom

```python title="src/pythonic/comprehensions.py"
--8<-- "src/pythonic/comprehensions.py:pythonic"
```

The test suite [checks that both versions agree across a battery of generated inputs](https://github.com/williajm/pythonic/blob/main/tests/test_comprehensions.py)
(hypothesis invents the lists — sampled evidence, not a proof over an
infinite domain). The objection to the first version was
never correctness — it is that every extra line is a place for the next
edit to introduce a bug.

## Dicts and sets too

```python title="src/pythonic/comprehensions.py"
--8<-- "src/pythonic/comprehensions.py:dict-set"
```

`invert` is honest about its edge case: duplicate values collapse, later key
wins. The tests pin that behaviour down instead of pretending it away.

## No collection at all

```python title="src/pythonic/comprehensions.py"
--8<-- "src/pythonic/comprehensions.py:genexp"
```

Drop the square brackets and you have a *generator expression*: values are
produced and consumed one at a time, so memory stays flat.

!!! warning "When not to"
    Comprehensions stop being pythonic the moment they nest deeply or grow
    side effects. Two `for` clauses is usually the limit; a comprehension
    you have to read twice should have been a loop — or a generator
    function with a name.
