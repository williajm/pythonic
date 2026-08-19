"""Tests for pythonic.protocols — structural typing needs no inheritance."""

import math

import pytest

from pythonic.protocols import Circle, Square, total_area


def test_total_area_mixes_shapes() -> None:
    """Circle and Square share no base class, only a shape of behaviour."""
    assert total_area([Circle(1.0), Square(2.0)]) == pytest.approx(math.pi + 4.0)


def test_total_area_empty() -> None:
    """No shapes, zero area."""
    assert total_area([]) == 0.0


def test_a_local_class_satisfies_the_protocol() -> None:
    """A class defined right here quacks well enough — that is the point."""

    class Triangle:
        """Knows its area; has never heard of HasArea."""

        def area(self) -> float:
            """Return a fixed area for the test.

            Returns:
                Six, always.
            """
            return 6.0

    assert total_area([Triangle(), Square(1.0)]) == 7.0
