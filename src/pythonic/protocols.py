"""Protocols: duck typing that a type checker can verify.

Python has always cared about what an object *can do*, not what it *is*
("if it quacks..."). ``typing.Protocol`` writes that down: any class
with the right methods satisfies the protocol, no inheritance, no
registration, no import of the protocol by the implementing class.
"""

import math
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Protocol


# --8<-- [start:protocol]
class HasArea(Protocol):
    """Anything with an ``area`` method qualifies — structurally."""

    def area(self) -> float:
        """Return the area."""
        ...


def total_area(shapes: Iterable[HasArea]) -> float:
    """Sum the areas of any mix of shapes.

    This function names only the capability it needs. mypy verifies
    every caller structurally — pass an object without ``area`` and the
    build fails, yet no shape class knows this protocol exists.

    Args:
        shapes: Anything with an ``area`` method.

    Returns:
        The combined area.
    """
    return sum(shape.area() for shape in shapes)


# --8<-- [end:protocol]


# --8<-- [start:shapes]
@dataclass(frozen=True, slots=True)
class Circle:
    """A circle — satisfies HasArea without ever importing it."""

    radius: float

    def area(self) -> float:
        """Return the enclosed area.

        Returns:
            πr², the way Archimedes intended.
        """
        return math.pi * self.radius**2


@dataclass(frozen=True, slots=True)
class Square:
    """A square — also satisfies HasArea, also never imports it."""

    side: float

    def area(self) -> float:
        """Return the enclosed area.

        Returns:
            The side length squared.
        """
        return self.side * self.side


# --8<-- [end:shapes]
