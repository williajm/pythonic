"""Structural pattern matching: destructure data by its shape.

``match`` (Python 3.10+) is not a switch statement: a case can pull a
value apart, bind its pieces, and guard on them, all in one clause.
Paired with a closed union of dataclasses it gives Python honest sum
types — and ``assert_never`` makes mypy prove every case is handled.
"""

from dataclasses import dataclass
from typing import assert_never


# --8<-- [start:commands]
@dataclass(frozen=True, slots=True)
class Deposit:
    """Add money to the balance."""

    amount: int


@dataclass(frozen=True, slots=True)
class Withdraw:
    """Remove money from the balance."""

    amount: int


@dataclass(frozen=True, slots=True)
class SetBalance:
    """Overwrite the balance outright."""

    value: int


type Command = Deposit | Withdraw | SetBalance


def apply(balance: int, command: Command) -> int:
    """Apply a command to a balance.

    Each case destructures one variant. If a new variant joins
    ``Command`` and no case handles it, ``assert_never`` turns the
    omission into a *type error* — the bug is caught before the code
    ever runs.

    Args:
        balance: The balance before the command.
        command: The command to apply.

    Returns:
        The balance after the command.
    """
    match command:
        case Deposit(amount=amount):
            return balance + amount
        case Withdraw(amount=amount):
            return balance - amount
        case SetBalance(value=value):
            return value
    assert_never(command)


# --8<-- [end:commands]


# --8<-- [start:shapes-of-data]
def describe(value: object) -> str:  # noqa: PLR0911  # Eight shapes, eight returns: splitting the match would obscure it.
    """Describe a value by matching on its shape.

    Sequence patterns, mapping patterns, class patterns, and guards in
    one place. Order matters: the first matching case wins. And one
    honest wrinkle: ``True`` matches ``int()`` because bool subclasses
    int — the tests document it rather than hide it.

    Args:
        value: Anything.

    Returns:
        A human-readable description.
    """
    match value:
        case []:
            return "an empty list"
        case [only]:
            return f"a list holding {describe(only)}"
        case [first, *rest]:
            return f"a list starting with {describe(first)}, plus {len(rest)} more"
        case {"name": str(name)}:
            return f"a record for {name}"
        case str(text):
            return f"the text {text!r}"
        case int(number) if number < 0:
            return "a negative integer"
        case int():
            return "a non-negative integer"
        case _:
            return "something else"


# --8<-- [end:shapes-of-data]
