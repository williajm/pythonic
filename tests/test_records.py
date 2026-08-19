"""Tests for pythonic.records — generated and hand-rolled behave alike."""

import dataclasses

import pytest

from pythonic.records import Point, PointByHand, Reading


def test_point_by_hand_equality_and_repr() -> None:
    """The hand-written dunders do work — that was never the objection."""
    point = PointByHand(1.0, 2.0)
    assert point == PointByHand(1.0, 2.0)
    assert point != PointByHand(9.0, 2.0)
    assert repr(point) == "PointByHand(x=1.0, y=2.0)"
    assert hash(point) == hash(PointByHand(1.0, 2.0))


def test_point_by_hand_compares_unequal_to_other_types() -> None:
    """NotImplemented lets Python fall back to plain inequality."""
    assert PointByHand(1.0, 2.0) != (1.0, 2.0)


def test_dataclass_matches_hand_rolled_behaviour() -> None:
    """The generated dunders give the same equality and repr semantics."""
    point = Point(1.0, 2.0)
    assert point == Point(1.0, 2.0)
    assert point != Point(9.0, 2.0)
    assert repr(point) == "Point(x=1.0, y=2.0)"
    assert hash(point) == hash(Point(1.0, 2.0))


def test_point_distance() -> None:
    """A 3-4-5 triangle, as tradition demands."""
    assert Point(0.0, 0.0).distance_to(Point(3.0, 4.0)) == 5.0


def test_point_is_frozen() -> None:
    """frozen=True turns mutation into an immediate error."""
    point = Point(1.0, 2.0)
    with pytest.raises(dataclasses.FrozenInstanceError):
        point.x = 9.0  # type: ignore[misc]  # The error is the point (mypy agrees).


def test_point_has_slots() -> None:
    """slots=True means no per-instance __dict__ at all."""
    assert not hasattr(Point(1.0, 2.0), "__dict__")


def test_reading_unpacks_like_a_tuple() -> None:
    """NamedTuple keeps tuple behaviour and adds names."""
    reading = Reading(timestamp=60.0, value=21.5)
    timestamp, value = reading
    assert (timestamp, value) == (60.0, 21.5)
    assert reading.value == 21.5
