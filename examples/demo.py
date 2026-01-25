"""Demo application for DCC-style spinbox widgets.

Run with:
    python examples/demo.py

Or specify Qt binding:
    QT_BINDING=pyside2 python examples/demo.py
    QT_BINDING=pyside6 python examples/demo.py
"""

import sys
from pathlib import Path

# Add parent directory to path for development
sys.path.insert(0, str(Path(__file__).parent.parent))

from qt_dcc_spinbox import SpinBox, DoubleSpinBox, QT_BINDING
from qt_dcc_spinbox._qt import QtWidgets, Qt


class DemoWindow(QtWidgets.QWidget):
    """Demo window showcasing DCC spinbox features."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(f"DCC Spinbox Demo ({QT_BINDING})")
        self.resize(400, 300)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QtWidgets.QVBoxLayout(self)

        # Header
        header = QtWidgets.QLabel(
            "<b>DCC Spinbox Demo</b><br>"
            "<small>Drag vertically to adjust • MMB for stepper • "
            "Ctrl=fine • Shift=coarse • ESC=cancel</small>"
        )
        header.setWordWrap(True)
        layout.addWidget(header)

        layout.addSpacing(10)

        # Integer spinbox
        layout.addWidget(QtWidgets.QLabel("Integer SpinBox (range: -1000 to 1000):"))
        self.int_spinbox = SpinBox()
        self.int_spinbox.setRange(-1000, 1000)
        self.int_spinbox.setDefaultValue(0)
        self.int_spinbox.setValue(100)
        layout.addWidget(self.int_spinbox)

        layout.addSpacing(10)

        # Double spinbox - 2 decimals
        layout.addWidget(
            QtWidgets.QLabel("Double SpinBox (range: -100 to 100, 2 decimals):")
        )
        self.double_spinbox = DoubleSpinBox()
        self.double_spinbox.setRange(-100, 100)
        self.double_spinbox.setDecimals(2)
        self.double_spinbox.setDefaultValue(0.0)
        self.double_spinbox.setValue(25.5)
        layout.addWidget(self.double_spinbox)

        layout.addSpacing(10)

        # Double spinbox - high precision
        layout.addWidget(
            QtWidgets.QLabel("High Precision SpinBox (range: -10 to 10, 6 decimals):")
        )
        self.precision_spinbox = DoubleSpinBox()
        self.precision_spinbox.setRange(-10, 10)
        self.precision_spinbox.setDecimals(6)
        self.precision_spinbox.setDefaultValue(0.0)
        self.precision_spinbox.setValue(1.234567)
        self.precision_spinbox.stepper.set_threshold(30)  # Slower stepping
        layout.addWidget(self.precision_spinbox)

        layout.addSpacing(10)

        # Spinbox with suffix
        layout.addWidget(QtWidgets.QLabel("SpinBox with suffix (pixels):"))
        self.suffix_spinbox = SpinBox()
        self.suffix_spinbox.setRange(0, 1920)
        self.suffix_spinbox.setDefaultValue(1920)
        self.suffix_spinbox.setValue(1080)
        self.suffix_spinbox.setSuffix(" px")
        layout.addWidget(self.suffix_spinbox)

        layout.addStretch()

        # Info label
        info = QtWidgets.QLabel(
            f"<small>Using: {QT_BINDING} • "
            "Right-click buttons to reset to default</small>"
        )
        info.setAlignment(Qt.AlignCenter)
        layout.addWidget(info)


def main() -> None:
    """Run the demo application."""
    app = QtWidgets.QApplication(sys.argv)
    window = DemoWindow()
    window.show()

    # Use exec() for PySide6 compatibility (exec_() also works)
    if hasattr(app, "exec"):
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())


if __name__ == "__main__":
    main()
