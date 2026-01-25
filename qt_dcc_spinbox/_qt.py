"""PySide2/PySide6 compatibility shim.

This module provides a unified import layer for Qt bindings. It supports
explicit binding selection via the QT_BINDING environment variable, or
auto-detection with PySide6 preferred over PySide2.

Usage:
    from qt_dcc_spinbox._qt import QtWidgets, QtCore, QtGui, Qt, Signal
"""

import os
from typing import TYPE_CHECKING

__all__ = ["QtWidgets", "QtCore", "QtGui", "Qt", "Signal", "QT_BINDING"]

QT_BINDING = os.environ.get("QT_BINDING", "").lower()

if QT_BINDING == "pyside2":
    from PySide2 import QtWidgets, QtCore, QtGui
    from PySide2.QtCore import Qt, Signal
elif QT_BINDING == "pyside6":
    from PySide6 import QtWidgets, QtCore, QtGui
    from PySide6.QtCore import Qt, Signal
else:
    # Auto-detect: try PySide6 first, fall back to PySide2
    try:
        from PySide6 import QtWidgets, QtCore, QtGui
        from PySide6.QtCore import Qt, Signal
        QT_BINDING = "pyside6"
    except ImportError:
        from PySide2 import QtWidgets, QtCore, QtGui
        from PySide2.QtCore import Qt, Signal
        QT_BINDING = "pyside2"

if TYPE_CHECKING:
    from PySide6 import QtWidgets, QtCore, QtGui
    from PySide6.QtCore import Qt, Signal
