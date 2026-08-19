"""Strings: f-strings for formatting, join for assembly, t-strings for later.

Python has retired three generations of formatting (``%``, ``format``,
manual concatenation) in favour of f-strings: the expression sits where
its value will appear. Python 3.14 adds template strings (PEP 750),
which capture the *pieces* instead of eagerly producing text.
"""

from collections.abc import Iterable
from string.templatelib import Interpolation, Template


# --8<-- [start:unpythonic]
def join_names_unpythonic(names: Iterable[str]) -> str:
    """Assemble a comma-separated list with += in a loop.

    We first published this claiming the ``if result:`` bookkeeping was
    merely noisy. Then property-based testing (hypothesis) proved it is
    also *wrong*: an empty name early in the list makes ``result`` falsy,
    so the next separator is silently dropped — ``["", ""]`` yields
    ``""`` where join yields ``", "``. The hand-rolled version stays
    here, bug and all, because that is the actual argument for ``join``:
    bookkeeping you write is bookkeeping you get wrong.

    Args:
        names: The names to join.

    Returns:
        The names separated by ", " — except around empty names, where
        the separator bug documented above kicks in.
    """
    result = ""
    for name in names:
        if result:
            result += ", "
        result += name
    return result


# --8<-- [end:unpythonic]


# --8<-- [start:pythonic]
def join_names(names: Iterable[str]) -> str:
    """Assemble a comma-separated list the way the language intends.

    The separator calls the shot: one method, no bookkeeping, linear
    time guaranteed.

    Args:
        names: The names to join.

    Returns:
        The names separated by ", ".
    """
    return ", ".join(names)


def receipt_line(item: str, price: float, width: int = 30) -> str:
    """Format one receipt line with f-string alignment specs.

    The spec after the colon handles padding, alignment, and decimal
    places — no manual space arithmetic.

    Args:
        item: The item name, left-aligned.
        price: The price, right-aligned to two decimal places.
        width: Total line width in characters.

    Returns:
        A fixed-width line like ``"tea                       2.50"``.
    """
    return f"{item:<{width - 8}}{price:>8.2f}"


# --8<-- [end:pythonic]


# --8<-- [start:tstrings]
def redact(template: Template) -> str:
    """Render a t-string with every interpolated value masked.

    An f-string hands you finished text; a t-string (Python 3.14,
    PEP 750) hands you the parts — static text and interpolations,
    separately. That lets library code decide how values are rendered:
    escaped for HTML, parameterised for SQL, or, here, redacted for a
    log line. ``redact(t"user {name} logged in")`` never sees the raw
    name in its output.

    Args:
        template: A t-string literal.

    Returns:
        The template's static text with every interpolation replaced
        by ``[REDACTED]``.
    """
    parts: list[str] = []
    for part in template:
        if isinstance(part, Interpolation):
            parts.append("[REDACTED]")
        else:
            parts.append(part)
    return "".join(parts)


# --8<-- [end:tstrings]
