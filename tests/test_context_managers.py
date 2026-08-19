"""Tests for pythonic.context_managers — cleanup must survive exceptions."""

from pathlib import Path

import pytest

from pythonic.context_managers import (
    Timer,
    extra_element,
    read_first_line,
    read_first_line_unpythonic,
    remove_if_present,
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


def test_extra_element_restores_list() -> None:
    """The element exists inside the block and is gone after."""
    items = [1, 2]
    with extra_element(items, 3) as extended:
        assert extended == [1, 2, 3]
    assert items == [1, 2]


def test_extra_element_restores_on_exception() -> None:
    """The finally clause pops even when the block raises."""
    items = [1, 2]
    boom = "boom"
    with pytest.raises(RuntimeError, match=boom), extra_element(items, 3):
        raise RuntimeError(boom)
    assert items == [1, 2]


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
