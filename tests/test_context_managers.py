"""Tests for pythonic.context_managers — cleanup must survive exceptions."""

from pathlib import Path

import pytest

from pythonic.context_managers import (
    Timer,
    read_first_line,
    read_first_line_unpythonic,
    remove_if_present,
    temporarily_replaced,
)


def test_read_first_line(tmp_path: Path) -> None:
    """The first line comes back, newline included."""
    target = tmp_path / "poem.txt"
    target.write_text("first\nsecond\n", encoding="utf-8")
    assert read_first_line(target) == "first\n"


def test_both_readers_agree(tmp_path: Path) -> None:
    """The leaky version reads the same bytes — the objection is the leak."""
    target = tmp_path / "poem.txt"
    target.write_text("first\nsecond\n", encoding="utf-8")
    assert read_first_line_unpythonic(target) == read_first_line(target)


def test_timer_measures_something() -> None:
    """Elapsed time is positive after the block."""
    with Timer() as timer:
        sum(range(1000))
    assert timer.elapsed > 0.0


def test_timer_records_even_when_block_raises() -> None:
    """__exit__ runs on the exception path too, and the exception escapes."""
    timer = Timer()
    boom = "boom"
    with pytest.raises(RuntimeError, match=boom), timer:
        raise RuntimeError(boom)
    assert timer.elapsed > 0.0


def test_temporarily_replaced_swaps_and_restores() -> None:
    """The entry is replaced inside the block and restored after."""
    config = {"mode": "live"}
    with temporarily_replaced(config, "mode", "test"):
        assert config["mode"] == "test"
    assert config["mode"] == "live"


def test_temporarily_replaced_restores_on_exception() -> None:
    """The finally clause restores even when the block raises."""
    config = {"mode": "live"}
    boom = "boom"
    with (
        pytest.raises(RuntimeError, match=boom),
        temporarily_replaced(config, "mode", "test"),
    ):
        raise RuntimeError(boom)
    assert config["mode"] == "live"


def test_temporarily_replaced_owns_its_key_whatever_the_block_does() -> None:
    """Regression test for the cleanup-ownership review finding.

    The block may rewrite the managed key or grow the mapping; cleanup
    still restores exactly that key and touches nothing else.
    """
    config = {"mode": "live", "retries": "3"}
    with temporarily_replaced(config, "mode", "test"):
        config["mode"] = "chaos"
        config["added"] = "by the block"
    assert config == {"mode": "live", "retries": "3", "added": "by the block"}


def test_temporarily_replaced_requires_existing_key() -> None:
    """Absent keys are rejected before the block runs, as documented."""
    config: dict[str, str] = {}
    with (
        pytest.raises(KeyError, match="mode"),
        temporarily_replaced(config, "mode", "test"),
    ):
        pytest.fail("the block must never run")


def test_remove_if_present_removes() -> None:
    """A present value is removed."""
    items = [1, 2, 3]
    remove_if_present(items, 2)
    assert items == [1, 3]


def test_remove_if_present_ignores_absence() -> None:
    """An absent value raises nothing and changes nothing."""
    items = [1, 3]
    remove_if_present(items, 2)
    assert items == [1, 3]
