"""EAFP: it is Easier to Ask Forgiveness than Permission.

The pythonic instinct is to attempt the operation and handle the
exception, rather than checking preconditions first (LBYL, "look before
you leap"). The deeper reason is correctness, not style: a pre-check is
a *second implementation* of the operation's rules, and second
implementations drift.

Honesty clause: LBYL is right when failure is expensive, when an
exception would not be raised cleanly (e.g. destructive side effects),
or when the check genuinely is the operation. EAFP is a default, not
a dogma.
"""

from collections import Counter
from collections.abc import Iterable


# --8<-- [start:lbyl]
def to_int_lbyl(text: str) -> int | None:
    """Convert text to int by checking first — wrongly, twice over.

    ``str.isdigit`` is a *guess* at what ``int`` accepts, and it errs in
    both directions: ``"-3".isdigit()`` is False though ``int("-3")``
    works, while ``"³".isdigit()`` is True though ``int("³")`` raises.
    The tests pin both failure modes down.

    Args:
        text: The text to convert.

    Returns:
        The integer, or None when the (flawed) check says no.
    """
    if text.isdigit():
        return int(text)
    return None


# --8<-- [end:lbyl]


# --8<-- [start:eafp]
def to_int(text: str) -> int | None:
    """Convert text to int by asking int itself.

    There is exactly one authority on what ``int`` accepts: ``int``.
    Attempt the conversion and translate the failure.

    Args:
        text: The text to convert.

    Returns:
        The integer, or None when the text is not a valid integer.
    """
    try:
        value = int(text)
    except ValueError:
        return None
    else:
        return value


# --8<-- [end:eafp]


# --8<-- [start:counter]
def count_words_by_hand(words: Iterable[str]) -> dict[str, int]:
    """Tally words with dict.get — the classic missing-key idiom.

    ``counts.get(word, 0)`` folds the "first time seen" case into the
    normal path: no membership test, no KeyError.

    Args:
        words: The words to tally.

    Returns:
        A dict mapping each word to how often it appeared.
    """
    counts: dict[str, int] = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    return counts


def count_words(words: Iterable[str]) -> Counter[str]:
    """Tally words the way the stdlib intended.

    The honest ending to the previous example: ``collections.Counter``
    already does this, plus ``most_common`` and arithmetic. Knowing the
    idiom matters; knowing the stdlib already shipped it matters more.

    Args:
        words: The words to tally.

    Returns:
        A Counter mapping each word to how often it appeared.
    """
    return Counter(words)


# --8<-- [end:counter]
