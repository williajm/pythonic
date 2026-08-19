"""Tests for pythonic.generators — including proof of laziness."""

from itertools import accumulate

from pythonic.generators import (
    first_match,
    first_squares_unpythonic,
    running_total,
    squares,
    take,
)


def test_take_from_infinite_generator() -> None:
    """Five squares come out of an infinite stream — laziness in action."""
    assert take(5, squares()) == [0, 1, 4, 9, 16]


def test_eager_and_lazy_agree() -> None:
    """The eager counter-example matches the lazy pipeline."""
    assert first_squares_unpythonic(10) == take(10, squares())


def test_take_stops_at_source_end() -> None:
    """Asking for more than exists returns what there is."""
    assert take(10, iter([1, 2])) == [1, 2]


def test_running_total() -> None:
    """Each yield is the sum so far."""
    assert list(running_total([1.0, 2.0, 3.0])) == [1.0, 3.0, 6.0]


def test_running_total_matches_stdlib() -> None:
    """The honest footnote, verified: itertools.accumulate does the same."""
    numbers = [2.5, -1.0, 4.0]
    assert list(running_total(numbers)) == list(accumulate(numbers))


def test_first_match() -> None:
    """The first satisfying item wins."""
    assert first_match([1, 3, 4, 6], wanted=lambda n: n % 2 == 0, default=0) == 4


def test_first_match_default() -> None:
    """No match falls back to the default."""
    assert first_match([1, 3], wanted=lambda n: n % 2 == 0, default=-1) == -1


def test_first_match_short_circuits() -> None:
    """Nothing after the first match is ever examined."""
    seen: list[int] = []

    def spy(n: int) -> bool:
        seen.append(n)
        return n > 1

    assert first_match([1, 2, 3, 4], wanted=spy, default=0) == 2
    assert seen == [1, 2]
