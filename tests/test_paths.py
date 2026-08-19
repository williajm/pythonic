"""Tests for pythonic.paths."""

from pathlib import Path

from pythonic.paths import (
    find_python_files,
    find_python_files_unpythonic,
    read_utf8,
    report_path,
)


def _make_tree(root: Path) -> None:
    """Create a small tree with .py files at two depths and one decoy."""
    (root / "a.py").write_text("", encoding="utf-8")
    (root / "notes.txt").write_text("", encoding="utf-8")
    (root / "pkg").mkdir()
    (root / "pkg" / "b.py").write_text("", encoding="utf-8")


def test_find_python_files(tmp_path: Path) -> None:
    """Recursive globbing finds .py files at every depth and skips the decoy."""
    _make_tree(tmp_path)
    assert find_python_files(tmp_path) == [tmp_path / "a.py", tmp_path / "pkg" / "b.py"]


def test_both_finders_agree(tmp_path: Path) -> None:
    """The os.walk version finds the same files — the objection is the plumbing."""
    _make_tree(tmp_path)
    from_strings = {Path(p) for p in find_python_files_unpythonic(str(tmp_path))}
    assert from_strings == set(find_python_files(tmp_path))


def test_report_path() -> None:
    """Segments join with /, and the year becomes a directory."""
    result = report_path(Path("reports"), 2026, "august")
    assert result == Path("reports") / "2026" / "august.csv"


def test_read_utf8(tmp_path: Path) -> None:
    """The explicit encoding reads non-ASCII text faithfully everywhere."""
    target = tmp_path / "greeting.txt"
    target.write_text("naïve café\n", encoding="utf-8")
    assert read_utf8(target) == "naïve café\n"
