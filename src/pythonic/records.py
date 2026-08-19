"""Records: let the language write the boilerplate.

A class that exists to hold named fields should not hand-roll
``__init__``, ``__repr__``, and ``__eq__`` — ``@dataclass`` generates
them correctly from the field declarations. On Python 3.14, annotations
are lazily evaluated (PEP 649), so a method can reference its own class
in a signature with no quotes and no ``__future__`` import.

Honesty clause: dataclasses do containment, not validation. When data
crosses a trust boundary, reach for an established library (pydantic,
attrs with validators) rather than reinventing one.
"""

import math
from dataclasses import dataclass
from typing import NamedTuple


# --8<-- [start:unpythonic]
class PointByHand:
    """What a two-field record costs when written by hand.

    Sixteen lines of ceremony that ``@dataclass`` generates from two —
    and every line is a place for the next edit to introduce a bug
    (add a field, forget to update ``__eq__``, and equality silently
    lies).

    There is also a trap already sprung: this class is hashable *and*
    mutable. Mutate a point after storing it in a set or dict and it
    becomes unfindable — its hash changed while the container filed it
    under the old one (tested). The generated version refuses to make
    that mistake: a plain ``@dataclass`` sets ``__hash__`` to None, and
    only ``frozen=True`` buys hashability back — by removing the
    mutability that made it dangerous.
    """

    def __init__(self, x: float, y: float) -> None:
        """Store the coordinates.

        Args:
            x: Horizontal coordinate.
            y: Vertical coordinate.
        """
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        """Rebuild the constructor call, by hand."""
        return f"PointByHand(x={self.x!r}, y={self.y!r})"

    def __eq__(self, other: object) -> bool:
        """Compare field by field, by hand."""
        if not isinstance(other, PointByHand):
            return NotImplemented
        return (self.x, self.y) == (other.x, other.y)

    def __hash__(self) -> int:
        """Hash the same fields ``__eq__`` compares — easy to forget.

        Also the wrong call entirely on a mutable class: see the class
        docstring for the set-membership trap it creates.
        """
        return hash((self.x, self.y))


# --8<-- [end:unpythonic]


# --8<-- [start:pythonic]
@dataclass(frozen=True, slots=True)
class Point:
    """A point on the plane.

    ``frozen=True`` makes instances immutable (and therefore hashable);
    ``slots=True`` drops the per-instance dict, cutting memory and
    catching attribute typos at assignment time.
    """

    x: float
    y: float

    def distance_to(self, other: Point) -> float:
        """Measure the straight-line distance to another point.

        The unquoted ``Point`` annotation is PEP 649 at work: on 3.14,
        annotations evaluate lazily, so the class can name itself.

        Args:
            other: The point to measure to.

        Returns:
            The Euclidean distance.
        """
        return math.hypot(self.x - other.x, self.y - other.y)


# --8<-- [end:pythonic]


# --8<-- [start:namedtuple]
class Reading(NamedTuple):
    """A timestamped sensor value.

    ``NamedTuple`` is the right record when you genuinely want a tuple:
    unpackable, comparable, and compatible with tuple-expecting APIs —
    while the call sites still read ``reading.value``, not ``r[1]``.
    """

    timestamp: float
    value: float


# --8<-- [end:namedtuple]
