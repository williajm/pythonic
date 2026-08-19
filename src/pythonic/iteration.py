"""Iteration: Python's for loop already knows how to count and pair.

Most index arithmetic in Python is a C habit wearing a snake costume.
``enumerate`` counts for you, ``zip`` pairs parallel sequences, and
star-unpacking splits a sequence without a single subscript.
"""

from collections.abc import Iterable, Sequence


# --8<-- [start:unpythonic]
def label_positions_unpythonic(items: Sequence[str]) -> list[str]:
    """Number the items by juggling indexes manually.

    ``range(len(items))`` forces every read through a subscript and
    quietly demands a ``Sequence`` — the natural version works on any
    iterable. Ruff flags the append loop as PERF401.

    Args:
        items: The items to label.

    Returns:
        Each item prefixed with its position, e.g. ``"0: spam"``.
    """
    result: list[str] = []
    for i in range(len(items)):
        result.append(f"{i}: {items[i]}")  # noqa: PERF401  # Deliberate counter-example.
    return result


# --8<-- [end:unpythonic]


# --8<-- [start:enumerate]
def label_positions(items: Iterable[str]) -> list[str]:
    """Number the items with enumerate.

    Args:
        items: The items to label — any iterable, no indexing required.

    Returns:
        Each item prefixed with its position, e.g. ``"0: spam"``.
    """
    return [f"{i}: {item}" for i, item in enumerate(items)]


# --8<-- [end:enumerate]


# --8<-- [start:zip]
def pair_scores(names: Sequence[str], scores: Sequence[int]) -> dict[str, int]:
    """Pair parallel sequences with zip.

    ``strict=True`` (Python 3.10+) turns a silent truncation bug into an
    immediate ``ValueError`` when the sequences drift out of step. Ruff
    (B905) insists on it, with good reason.

    Args:
        names: The keys, in order.
        scores: The values, in the same order.

    Returns:
        A dict pairing each name with its score.

    Raises:
        ValueError: If the two sequences have different lengths.
    """
    return dict(zip(names, scores, strict=True))


# --8<-- [end:zip]


# --8<-- [start:unpacking]
def head_and_rest(items: Sequence[int]) -> tuple[int, list[int]]:
    """Split off the first element with star-unpacking.

    No slices, no off-by-one opportunities: the assignment target
    mirrors the shape of the data.

    Args:
        items: A non-empty sequence.

    Returns:
        The first element, and the remaining elements as a list.

    Raises:
        ValueError: If ``items`` is empty (there is no head to take).
    """
    head, *rest = items
    return head, rest


def swapped[A, B](pair: tuple[A, B]) -> tuple[B, A]:
    """Swap a pair — tuple assignment needs no temporary variable.

    Args:
        pair: Any two-element tuple.

    Returns:
        The same two elements, reversed.
    """
    first, second = pair
    return second, first


# --8<-- [end:unpacking]
