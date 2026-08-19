"""Tests for pythonic.pattern_matching — every case, plus the honest wrinkle."""

import pytest

from pythonic.pattern_matching import Deposit, SetBalance, Withdraw, apply, describe


def test_apply_deposit() -> None:
    """Deposits add."""
    assert apply(100, Deposit(30)) == 130


def test_apply_withdraw() -> None:
    """Withdrawals subtract."""
    assert apply(100, Withdraw(30)) == 70


def test_apply_set_balance() -> None:
    """SetBalance overwrites."""
    assert apply(100, SetBalance(55)) == 55


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ([], "an empty list"),
        (["x"], "a list holding the text 'x'"),
        ([1, 2, 3], "a list starting with a non-negative integer, plus 2 more"),
        ({"name": "Ada"}, "a record for Ada"),
        ({"name": "Ada", "age": 36}, "a record for Ada"),
        ("spam", "the text 'spam'"),
        (-5, "a negative integer"),
        (7, "a non-negative integer"),
        (3.5, "something else"),
    ],
)
def test_describe(value: object, expected: str) -> None:
    """Each shape of data lands in its own case.

    Note the mapping with an extra key still matches — mapping patterns
    ignore keys they do not mention.
    """
    assert describe(value) == expected


def test_describe_bool_is_an_int() -> None:
    """The honest wrinkle: bool subclasses int, so True matches int()."""
    assert describe(value=True) == "a non-negative integer"
