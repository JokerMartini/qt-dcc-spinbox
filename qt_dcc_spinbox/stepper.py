"""Stepper dialog for Houdini-style value ladder.

Provides a popup dialog with step buttons for precise value control.
Middle-click and drag vertically to select a step size, then drag
horizontally to increment/decrement the value.
"""

from typing import Optional

from ._qt import QtWidgets, QtCore, QtGui, Qt
from .utils import get_cursor_pos

__all__ = ["StepButton", "StepperDialog"]


class StepButton(QtWidgets.QPushButton):
    """A button representing a single step value in the stepper dialog.

    Highlights on hover to indicate the active step size.
    """

    def __init__(self, text: str, parent: Optional[QtWidgets.QWidget] = None) -> None:
        """Initialize the step button.

        Args:
            text: The step value to display (e.g., "0.1").
            parent: Optional parent widget.
        """
        super().__init__(text, parent)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.NoFocus)

    def enterEvent(self, event: QtCore.QEvent) -> None:
        """Handle mouse enter by requesting focus."""
        self.setFocus()
        super().enterEvent(event)

    def focusInEvent(self, event: QtGui.QFocusEvent) -> None:
        """Handle focus in by making text bold."""
        font = self.font()
        font.setBold(True)
        self.setFont(font)
        super().focusInEvent(event)

    def focusOutEvent(self, event: QtGui.QFocusEvent) -> None:
        """Handle focus out by restoring normal text weight."""
        font = self.font()
        font.setBold(False)
        self.setFont(font)
        super().focusOutEvent(event)

    def sizeHint(self) -> QtCore.QSize:
        """Return the recommended size for the button.

        Returns:
            Minimum size of 40x40, expanded to fit text.
        """
        size = QtCore.QSize(40, 40)
        if self.text():
            fm = self.fontMetrics()
            text_size = fm.size(Qt.TextShowMnemonic, self.text())
            size.setWidth(max(size.width(), text_size.width() + 40))
        return size


class StepperDialog(QtWidgets.QDialog):
    """Popup dialog for Houdini-style value ladder stepping.

    Shows a vertical list of step buttons. Drag horizontally to adjust
    the parent spinbox value by the currently selected step amount.
    """

    def __init__(self, parent: Optional[QtWidgets.QWidget] = None) -> None:
        """Initialize the stepper dialog.

        Args:
            parent: The parent spinbox widget.
        """
        super().__init__(parent)
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)
        self.setMinimumWidth(2)
        self.setMinimumHeight(2)
        self.setWindowOpacity(0.90)
        self.setCursor(Qt.SizeHorCursor)

        # Internal state
        self._step: float = 0
        self._steps: list[float] = [100, 10, 1, 0.1, 0.01, 0.001, 0.0001]
        self._last_cursor_pos = QtCore.QPoint(0, 0)
        self._threshold: int = 10  # Pixels of horizontal movement per step
        self._original_value: float = 0  # For ESC restore

        # Layout
        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self.setLayout(self._layout)

        self._update_layout()

    # --- Properties ---

    @property
    def step(self) -> float:
        """The currently selected step value."""
        return self._step

    @step.setter
    def step(self, value: float) -> None:
        if self._step != value:
            self._step = value
            self._last_cursor_pos = get_cursor_pos()

    @property
    def steps(self) -> list[float]:
        """The list of available step values."""
        return self._steps

    @steps.setter
    def steps(self, value: list[float]) -> None:
        self._steps = value
        self._update_layout()

    @property
    def threshold(self) -> int:
        """Pixels of horizontal movement required per value step."""
        return self._threshold

    @threshold.setter
    def threshold(self, value: int) -> None:
        self._threshold = value

    # --- Public Methods ---

    def set_steps(self, steps: list[float]) -> None:
        """Set the available step values.

        Args:
            steps: List of step values to display.
        """
        self.steps = steps

    def set_threshold(self, value: int) -> None:
        """Set the horizontal drag threshold.

        Args:
            value: Pixels of movement per step.
        """
        self.threshold = value

    def auto_generate_steps(self, maximum: int = 100, decimals: int = 0) -> None:
        """Auto-generate step values based on range and precision.

        Args:
            maximum: Maximum value of the spinbox.
            decimals: Number of decimal places.
        """
        from .utils import generate_steps

        self.steps = generate_steps(maximum, decimals)

    # --- Private Methods ---

    def _determine_step(self) -> None:
        """Determine the current step from cursor position over buttons.

        Only updates the step if cursor is over a button. When cursor moves
        outside buttons (during drag), the last selected step is retained.
        """
        local_pos = self.mapFromGlobal(get_cursor_pos())
        widget = self.childAt(local_pos)
        if widget:
            try:
                self.step = float(widget.text())
            except (ValueError, AttributeError):
                pass  # Keep current step if widget has no parseable text

    def _update_layout(self) -> None:
        """Rebuild the button layout from current steps."""
        # Clear existing buttons
        while self._layout.count():
            item = self._layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Add new buttons
        for step in self._steps:
            btn = StepButton(str(step))
            self._layout.addWidget(btn)

    def _update_value(self) -> None:
        """Update the parent spinbox value based on horizontal drag."""
        delta_x = (get_cursor_pos() - self._last_cursor_pos).x()
        parent = self.parent()
        if parent is None:
            return

        if delta_x > self.threshold:
            self._last_cursor_pos = get_cursor_pos()
            parent.setValue(parent.value() + self.step)
        elif delta_x < -self.threshold:
            self._last_cursor_pos = get_cursor_pos()
            parent.setValue(parent.value() - self.step)

    def _restore_original_value(self) -> None:
        """Restore the spinbox to its value when the dialog opened."""
        parent = self.parent()
        if parent is not None:
            parent.setValue(self._original_value)

    # --- Event Handlers ---

    def showEvent(self, event: QtGui.QShowEvent) -> None:
        """Handle show event - position dialog and store original value."""
        # Store original value for ESC restore
        parent = self.parent()
        if parent is not None:
            self._original_value = parent.value()

        # Center on cursor
        self.move(get_cursor_pos() - self.rect().center())
        super().showEvent(event)
        self._determine_step()
        self._last_cursor_pos = get_cursor_pos()

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        """Handle mouse move - update step selection and value."""
        self._determine_step()
        if event.buttons() & Qt.MiddleButton:
            self._update_value()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        """Handle mouse release - close the dialog."""
        super().mouseReleaseEvent(event)
        self.close()

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        """Handle key press - ESC restores original value."""
        if event.key() == Qt.Key_Escape:
            self._restore_original_value()
            self.close()
        else:
            super().keyPressEvent(event)
