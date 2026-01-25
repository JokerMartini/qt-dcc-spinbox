"""DCC-style spinbox widgets for PySide2 and PySide6.

This package provides enhanced spinbox widgets with features inspired by
professional DCC (Digital Content Creation) applications like Houdini
and 3ds Max.

Features:
    - Middle-click stepper dialog for precise value control (Houdini-style)
    - Vertical drag on spinbox to adjust value (3ds Max-style)
    - Keyboard modifiers for step multipliers (Ctrl=fine, Shift=coarse)
    - ESC to restore original value during drag
    - Right-click on buttons to reset to default value
    - Automatic PySide2/PySide6 compatibility

Example:
    from qt_dcc_spinbox import SpinBox, DoubleSpinBox

    # Integer spinbox
    spinbox = SpinBox()
    spinbox.setRange(-1000, 1000)
    spinbox.setDefaultValue(0)

    # Double spinbox with 3 decimal places
    double_spinbox = DoubleSpinBox()
    double_spinbox.setRange(-100.0, 100.0)
    double_spinbox.setDecimals(3)
"""

__version__ = "0.1.0"

from .spinbox import SpinBox, DoubleSpinBox
from .stepper import StepperDialog, StepButton
from ._qt import QT_BINDING

__all__ = [
    "SpinBox",
    "DoubleSpinBox",
    "StepperDialog",
    "StepButton",
    "QT_BINDING",
    "__version__",
]
