"""Tests for pythonic.eafp — the LBYL bugs are pinned down, not papered over."""

import pytest

from pythonic.eafp import count_words, count_words_by_hand, to_int, to_int_lbyl


def test_to_int_accepts_plain_numbers() -> None:
    """The straightforward case works in both styles."""
    assert to_int("12") == 12
    assert to_int_lbyl("12") == 12


def test_to_int_rejects_garbage() -> None:
    """Non-numbers come back as None."""
    assert to_int("spam") is None
    assert to_int_lbyl("spam") is None


def test_lbyl_wrongly_rejects_negatives() -> None:
    """Documented bug: isdigit() says no to "-3", though int() accepts it."""
    assert to_int("-3") == -3
    assert to_int_lbyl("-3") is None


def test_lbyl_wrongly_accepts_superscripts() -> None:
    """Documented bug: isdigit() says yes to "³", so int() blows up."""
    assert to_int("³") is None
    with pytest.raises(ValueError, match="invalid literal"):
        to_int_lbyl("³")


def test_count_words_by_hand() -> None:
    """The dict.get idiom tallies correctly."""
    assert count_words_by_hand(["spam", "eggs", "spam"]) == {"spam": 2, "eggs": 1}


def test_counter_agrees_with_hand_tally() -> None:
    """The stdlib Counter matches the hand-rolled version, as promised."""
    words = ["spam", "eggs", "spam", "spam"]
    assert count_words(words) == count_words_by_hand(words)
