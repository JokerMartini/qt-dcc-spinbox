"""Utility functions for DCC spinbox widgets.

Provides cross-compatible helpers for PySide2/PySide6 differences,
particularly around mouse event handling.
"""

from typing import Union

from ._qt import QtCore, QtGui, QT_BINDING

__all__ = [
    "get_event_pos",
    "get_event_global_pos",
    "get_cursor_pos",
    "generate_whole_incrementers",
    "generate_decimal_incrementers",
    "generate_steps",
]


def get_event_pos(event: Union[QtGui.QMouseEvent, QtCore.QEvent]) -> QtCore.QPoint:
    """Get local position from a mouse event.

    Args:
        event: A Qt mouse event.

    Returns:
        The local position as QPoint.
    """
    if hasattr(event, "position"):  # PySide6
        return event.position().toPoint()
    return event.pos()  # PySide2


def get_event_global_pos(
    event: Union[QtGui.QMouseEvent, QtCore.QEvent]
) -> QtCore.QPoint:
    """Get global position from a mouse event.

    Args:
        event: A Qt mouse event.

    Returns:
        The global position as QPoint.
    """
    if hasattr(event, "globalPosition"):  # PySide6
        return event.globalPosition().toPoint()
    return event.globalPos()  # PySide2


def get_cursor_pos() -> QtCore.QPoint:
    """Get the current global cursor position.

    Returns:
        The global cursor position as QPoint.
    """
    return QtGui.QCursor.pos()


def generate_whole_incrementers(num: int) -> list[float]:
    """Generate whole number step increments based on a maximum value.

    For a number like 1000, generates [100, 10, 1].

    Args:
        num: The maximum value to generate steps for.

    Returns:
        List of whole number steps in descending order.
    """
    if num <= 0:
        return [1]
    str_num = str(int(abs(num))).split(".")[0]
    length = len(str_num) - 1
    if length <= 0:
        return [1]
    return [10 ** (length - i - 1) for i in range(length)]


def generate_decimal_incrementers(decimals: int) -> list[float]:
    """Generate decimal step increments.

    For decimals=3, generates [0.1, 0.01, 0.001].

    Args:
        decimals: Number of decimal places to generate steps for.

    Returns:
        List of decimal steps in descending order.
    """
    if decimals <= 0:
        return []
    return [10**-i for i in range(1, decimals + 1)]


def generate_steps(maximum: int = 100, decimals: int = 0) -> list[float]:
    """Generate a complete list of step increments.

    Combines whole number and decimal increments, sorted descending.

    Args:
        maximum: The maximum value of the spinbox.
        decimals: Number of decimal places supported.

    Returns:
        List of all step values in descending order.
    """
    whole = generate_whole_incrementers(maximum)
    decimal = generate_decimal_incrementers(decimals)
    return sorted(whole + decimal, reverse=True)
