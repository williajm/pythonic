"""Tests for pythonic.iteration."""

import pytest

from pythonic.iteration import (
    head_and_rest,
    label_positions,
    label_positions_unpythonic,
    pair_scores,
    swapped,
)


def test_label_positions() -> None:
    """Positions count from zero."""
    assert label_positions(["spam", "eggs"]) == ["0: spam", "1: eggs"]


def test_both_labelling_styles_agree() -> None:
    """The index-juggling version produces the same labels."""
    items = ["a", "b", "c"]
    assert label_positions_unpythonic(items) == label_positions(items)


def test_pair_scores() -> None:
    """Names pair with scores in order."""
    assert pair_scores(["ada", "grace"], [1, 2]) == {"ada": 1, "grace": 2}


def test_pair_scores_rejects_mismatched_lengths() -> None:
    """strict=True raises instead of silently truncating."""
    with pytest.raises(ValueError, match="zip"):
        pair_scores(["ada", "grace"], [1])


def test_head_and_rest() -> None:
    """The head splits off; the rest stays a list."""
    assert head_and_rest([1, 2, 3]) == (1, [2, 3])


def test_head_and_rest_single_element() -> None:
    """A one-element sequence leaves an empty rest."""
    assert head_and_rest([7]) == (7, [])


def test_head_and_rest_rejects_empty() -> None:
    """An empty sequence has no head to take."""
    with pytest.raises(ValueError, match="not enough"):
        head_and_rest([])


def test_swapped() -> None:
    """The pair comes back reversed, types and all."""
    assert swapped((1, "one")) == ("one", 1)
