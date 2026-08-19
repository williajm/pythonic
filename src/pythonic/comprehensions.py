"""Comprehensions: build a collection in one declarative expression.

A comprehension states *what* the result contains; a loop describes *how*
to assemble it. When the transformation is a single map/filter step, the
declarative form is shorter, faster, and impossible to get subtly wrong
(no forgotten ``append``, no leaked loop variable state).

Honesty clause: comprehensions stop being pythonic the moment they nest
deeply or grow side effects. Two ``for`` clauses is usually the limit;
past that, an explicit loop or a generator function reads better.
"""

from collections.abc import Hashable, Iterable, Mapping


# --8<-- [start:unpythonic]
def squares_of_evens_unpythonic(numbers: Iterable[int]) -> list[int]:
    """Collect the squares of the even numbers, the long way round.

    Three lines of ceremony (create, append, return) for one line of
    intent. Ruff flags the pattern as PERF401 — the linter itself knows
    this wants to be a comprehension.

    Args:
        numbers: Any iterable of integers.

    Returns:
        The square of every even number, in input order.
    """
    result: list[int] = []
    for number in numbers:
        if number % 2 == 0:
            result.append(number * number)  # noqa: PERF401  # Deliberate counter-example.
    return result


# --8<-- [end:unpythonic]


# --8<-- [start:pythonic]
def squares_of_evens(numbers: Iterable[int]) -> list[int]:
    """Collect the squares of the even numbers.

    Args:
        numbers: Any iterable of integers.

    Returns:
        The square of every even number, in input order.
    """
    return [number * number for number in numbers if number % 2 == 0]


# --8<-- [end:pythonic]


# --8<-- [start:dict-set]
def invert[K, V: Hashable](mapping: Mapping[K, V]) -> dict[V, K]:
    """Swap a mapping's keys and values with a dict comprehension.

    If two keys share a value, the later key wins — inversion is only
    faithful when the values are unique. The test suite pins down both
    behaviours rather than pretending the edge case away.

    Args:
        mapping: Any mapping with hashable values.

    Returns:
        A new dict mapping each value back to its (last seen) key.
    """
    return {value: key for key, value in mapping.items()}


def unique_lengths(words: Iterable[str]) -> set[int]:
    """Collect the distinct word lengths with a set comprehension.

    Args:
        words: Any iterable of strings.

    Returns:
        The set of lengths that occur.
    """
    return {len(word) for word in words}


# --8<-- [end:dict-set]


# --8<-- [start:genexp]
def total_letters(words: Iterable[str]) -> int:
    """Sum the word lengths without building an intermediate list.

    The argument to ``sum`` is a generator expression: each length is
    produced, consumed, and discarded one at a time, so memory stays
    flat no matter how many words stream past.

    Args:
        words: Any iterable of strings.

    Returns:
        The combined length of all the words.
    """
    return sum(len(word) for word in words)


# --8<-- [end:genexp]
