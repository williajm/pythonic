"""Tests for pythonic.comprehensions — including proof the two styles agree."""

from hypothesis import given
from hypothesis import strategies as st

from pythonic.comprehensions import (
    invert,
    squares_of_evens,
    squares_of_evens_unpythonic,
    total_letters,
    unique_lengths,
)


def test_squares_of_evens() -> None:
    """Evens are squared, odds are dropped, order is kept."""
    assert squares_of_evens([1, 2, 3, 4, 5, 6]) == [4, 16, 36]


def test_squares_of_evens_empty() -> None:
    """An empty input yields an empty list."""
    assert squares_of_evens([]) == []


@given(st.lists(st.integers()))
def test_both_styles_agree(numbers: list[int]) -> None:
    """The counter-example is equivalent — the objection is style, not output."""
    assert squares_of_evens_unpythonic(numbers) == squares_of_evens(numbers)


def test_invert_round_trips_unique_values() -> None:
    """With unique values, inverting twice restores the original."""
    original = {"a": 1, "b": 2, "c": 3}
    assert invert(invert(original)) == original


def test_invert_last_key_wins_on_duplicate_values() -> None:
    """Duplicate values collapse: the later key survives, as documented."""
    assert invert({"a": 1, "b": 1}) == {1: "b"}


def test_unique_lengths() -> None:
    """Duplicate lengths appear once."""
    assert unique_lengths(["spam", "eggs", "ni"]) == {4, 2}


def test_total_letters() -> None:
    """Lengths are summed without materialising a list."""
    assert total_letters(["spam", "eggs", "ni"]) == 10
