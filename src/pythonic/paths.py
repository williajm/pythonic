"""Paths: pathlib treats paths as objects, not string puzzles.

``os.path`` works on strings, so every operation is a free function and
every join is an opportunity for a separator bug. ``pathlib.Path`` puts
the operations on the object: joining is ``/``, reading is a method,
and globbing needs no manual recursion.
"""

import os
from pathlib import Path


# --8<-- [start:unpythonic]
def find_python_files_unpythonic(root: str) -> list[str]:
    """Walk a tree with os.walk and assemble paths by hand.

    Strings in, strings out, and a nested loop to do what one glob
    expresses. Ruff's flake8-use-pathlib rules flag the string join
    (PTH118).

    Args:
        root: The directory to search, as a string.

    Returns:
        Paths of all ``.py`` files under root, sorted.
    """
    found: list[str] = []
    for dirpath, _dirnames, filenames in os.walk(root):
        for filename in filenames:
            if filename.endswith(".py"):
                found.append(os.path.join(dirpath, filename))  # noqa: PTH118, PERF401  # Deliberate counter-example.
    return sorted(found)


# --8<-- [end:unpythonic]


# --8<-- [start:pythonic]
def find_python_files(root: Path) -> list[Path]:
    """Walk a tree with one recursive glob.

    Args:
        root: The directory to search.

    Returns:
        Paths of all ``.py`` files under root, sorted.
    """
    return sorted(root.rglob("*.py"))


# --8<-- [end:pythonic]


# --8<-- [start:operations]
def report_path(base: Path, year: int, name: str) -> Path:
    """Build a nested path with the / operator.

    No separator characters appear anywhere: the OS-specific joining is
    the Path object's job.

    Args:
        base: The directory reports live under.
        year: The report year (becomes a directory).
        name: The report name (becomes ``name.csv``).

    Returns:
        ``base/year/name.csv`` for the current platform.
    """
    return base / str(year) / f"{name}.csv"


def read_utf8(path: Path) -> str:
    """Read a whole text file in one call.

    ``read_text`` opens, reads, and closes — the context manager from
    the previous chapter, already folded into the method. The explicit
    encoding is deliberate: relying on the platform default is how
    Windows bug reports are born.

    Args:
        path: The file to read.

    Returns:
        The file's entire contents.
    """
    return path.read_text(encoding="utf-8")


# --8<-- [end:operations]
