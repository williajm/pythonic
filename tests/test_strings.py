"""Tests for pythonic.strings — including the t-string newcomer."""

from hypothesis import given
from hypothesis import strategies as st

from pythonic.strings import join_names, join_names_unpythonic, receipt_line, redact


def test_join_names() -> None:
    """Names join with a comma-space separator."""
    assert join_names(["ada", "grace", "guido"]) == "ada, grace, guido"


def test_join_names_empty() -> None:
    """No names, empty string — no stray separator."""
    assert join_names([]) == ""


@given(st.lists(st.text(min_size=1)))
def test_both_join_styles_agree_on_non_empty_names(names: list[str]) -> None:
    """For non-empty names the two versions agree; for empty ones they don't."""
    assert join_names_unpythonic(names) == join_names(names)


def test_hand_rolled_join_drops_separators_around_empty_names() -> None:
    """Regression test for the bug hypothesis found in the counter-example.

    The ``if result:`` guard misfires when an early name is empty: the
    separator vanishes. This is documented, not fixed — the broken
    bookkeeping *is* the argument for str.join.
    """
    assert join_names(["", ""]) == ", "
    assert join_names_unpythonic(["", ""]) == ""


def test_receipt_line() -> None:
    """Item left-aligned, price right-aligned to two decimals."""
    line = receipt_line("tea", 2.5)
    assert line == "tea                       2.50"
    assert len(line) == 30


def test_receipt_line_custom_width() -> None:
    """The width knob stretches the padding."""
    assert len(receipt_line("tea", 2.5, width=40)) == 40


def test_redact_masks_interpolations() -> None:
    """The static text survives; the interpolated value does not."""
    name = "ada"
    assert redact(t"user {name} logged in") == "user [REDACTED] logged in"


def test_redact_handles_multiple_interpolations() -> None:
    """Every interpolation is masked independently."""
    user, host = "ada", "lovelace.example"
    assert redact(t"{user}@{host}") == "[REDACTED]@[REDACTED]"


def test_redact_plain_template() -> None:
    """A template with no interpolations is returned as-is."""
    assert redact(t"nothing to hide") == "nothing to hide"
