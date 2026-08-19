"""Generators: compute values on demand instead of all up front.

A generator function looks like a normal function but ``yield``s a
stream. Nothing runs until someone asks for the next value, so pipelines
stay flat in memory and infinite sequences become ordinary objects.
"""

from collections.abc import Callable, Iterable, Iterator
from itertools import islice


# --8<-- [start:unpythonic]
def first_squares_unpythonic(n: int) -> list[int]:
    """Take the first n squares by materialising 100,000 of them.

    The list is built in full, held in memory, then thrown away after
    the slice. The eager habit works — the tests prove it — but it
    scales with the size of the *source*, not the size of the answer.

    Args:
        n: How many squares to keep (at most 100,000 here, which is
            exactly the arbitrary-cap problem laziness avoids).

    Returns:
        The first n square numbers, starting from 0.
    """
    all_squares = [i * i for i in range(100_000)]
    return all_squares[:n]


# --8<-- [end:unpythonic]


# --8<-- [start:pythonic]
def squares() -> Iterator[int]:
    """Yield square numbers forever.

    An infinite sequence is unrepresentable as a list but trivial as a
    generator: state lives in the paused function frame.

    Yields:
        0, 1, 4, 9, 16, ... without end.
    """
    i = 0
    while True:
        yield i * i
        i += 1


def take[T](n: int, iterable: Iterable[T]) -> list[T]:
    """Materialise the first n items of any iterable.

    ``itertools.islice`` stops pulling as soon as it has enough, so
    ``take(5, squares())`` computes exactly five squares.

    Args:
        n: How many items to take.
        iterable: The source — finite or infinite.

    Returns:
        Up to n items, as a list.
    """
    return list(islice(iterable, n))


# --8<-- [end:pythonic]


# --8<-- [start:pipeline]
def running_total(numbers: Iterable[float]) -> Iterator[float]:
    """Yield the cumulative sum after each number.

    Written out to show the mechanics; honesty compels the footnote
    that the stdlib already ships this as ``itertools.accumulate``.

    Args:
        numbers: Any iterable of numbers.

    Yields:
        The total so far, once per input number.
    """
    total = 0.0
    for number in numbers:
        total += number
        yield total


def first_match[T](items: Iterable[T], wanted: Callable[[T], bool], default: T) -> T:
    """Find the first item satisfying a predicate, lazily.

    ``next`` over a generator expression stops at the first hit —
    nothing after it is ever examined.

    Args:
        items: The candidates, examined in order.
        wanted: The predicate a match must satisfy.
        default: Returned when nothing matches.

    Returns:
        The first matching item, or ``default``.
    """
    return next((item for item in items if wanted(item)), default)


# --8<-- [end:pipeline]
