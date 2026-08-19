"""Context managers: pair setup with guaranteed cleanup.

``with`` is Python's answer to resource leaks: the cleanup runs whether
the block finishes, returns, or raises. Anything that must be undone —
closing a file, releasing a lock, restoring state — belongs in one.
"""

import time
from collections.abc import Iterator
from contextlib import contextmanager, suppress
from pathlib import Path
from types import TracebackType
from typing import Self


# --8<-- [start:unpythonic]
def read_first_line_unpythonic(path: Path) -> str:
    """Open, read, close — with a leak hiding between the lines.

    If ``readline`` raises, ``close`` never runs and the handle leaks
    until the garbage collector deigns to collect it.

    Args:
        path: The file to read.

    Returns:
        The file's first line, newline included.
    """
    handle = path.open(encoding="utf-8")  # Deliberate counter-example: no with block.
    line = handle.readline()
    handle.close()  # Never reached if readline() raises.
    return line


# --8<-- [end:unpythonic]


# --8<-- [start:pythonic]
def read_first_line(path: Path) -> str:
    """Read the first line; the with block closes the file on any exit.

    Args:
        path: The file to read.

    Returns:
        The file's first line, newline included.
    """
    with path.open(encoding="utf-8") as handle:
        return handle.readline()


# --8<-- [end:pythonic]


# --8<-- [start:class]
class Timer:
    """Measure the wall-clock duration of a block.

    The protocol is just two methods: ``__enter__`` runs at the top of
    the ``with`` block, ``__exit__`` runs on the way out — exception or
    not. After the block, ``elapsed`` holds the duration in seconds.
    """

    def __init__(self) -> None:
        """Start with nothing measured."""
        self.elapsed = 0.0
        self._start = 0.0

    def __enter__(self) -> Self:
        """Record the start time and hand the timer to ``as``."""
        self._start = time.perf_counter()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Record the duration; returning None lets exceptions propagate."""
        self.elapsed = time.perf_counter() - self._start


# --8<-- [end:class]


# --8<-- [start:contextlib]
@contextmanager
def extra_element[T](items: list[T], element: T) -> Iterator[list[T]]:
    """Append an element for the duration of the block, then remove it.

    ``@contextmanager`` turns a generator into a context manager: code
    before ``yield`` is setup, code in the ``finally`` is cleanup, and
    the ``finally`` guarantees the cleanup even when the block raises.

    Args:
        items: The list to temporarily extend.
        element: The element to append.

    Yields:
        The extended list, for use inside the block.
    """
    items.append(element)
    try:
        yield items
    finally:
        items.pop()


def remove_if_present[T](items: list[T], value: T) -> None:
    """Remove a value from a list, ignoring its absence.

    ``contextlib.suppress`` replaces a four-line try/except/pass and
    names the intent: this exception is expected and unremarkable.

    Args:
        items: The list to remove from (modified in place).
        value: The value to remove, if present.
    """
    with suppress(ValueError):
        items.remove(value)


# --8<-- [end:contextlib]
