"""DCC-style spinbox widgets.

Provides enhanced spinbox widgets with features from Houdini and 3ds Max:
- Middle-click stepper dialog for precise value control (Houdini-style)
- Click-drag on spinbox to adjust value (3ds Max-style)
- Keyboard modifiers for step multipliers (Ctrl=fine, Shift=coarse)
- ESC to restore original value during drag
- Right-click on buttons to reset to default value
"""

from typing import Optional, Union

from ._qt import QtWidgets, QtCore, QtGui, Qt
from .stepper import StepperDialog
from .utils import get_event_pos

__all__ = ["SpinBox", "DoubleSpinBox"]


class _SpinBoxMixin:
    """Shared functionality for SpinBox and DoubleSpinBox.

    Provides:
    - Vertical drag to adjust value
    - Middle-click stepper dialog
    - Modifier keys for step multipliers
    - ESC to restore original value
    - Default value with right-click reset
    """

    def _init_dcc_features(self) -> None:
        """Initialize DCC-specific features. Call from subclass __init__."""
        # Default value (reset on right-click)
        self._default_value: float = 0

        # Drag settings
        self._drag_step_multiplier: float = 0.5
        self._fine_multiplier: float = 0.1  # Ctrl modifier
        self._coarse_multiplier: float = 10.0  # Shift modifier

        # Internal drag state
        self._mouse_start_pos_y: int = 0
        self._drag_start_value: float = 0
        self._is_dragging: bool = False
        self._original_value: float = 0  # For ESC restore

        # Stepper dialog
        self._stepper: Optional[StepperDialog] = None

        # Enable mouse tracking
        self.setMouseTracking(True)
        self.lineEdit().installEventFilter(self)

    def _create_stepper(self) -> StepperDialog:
        """Create and configure the stepper dialog."""
        stepper = StepperDialog(parent=self)
        self._update_stepper_steps(stepper)
        return stepper

    def _update_stepper_steps(self, stepper: StepperDialog) -> None:
        """Update stepper steps based on spinbox range. Override in subclass."""
        stepper.auto_generate_steps(int(abs(self.maximum())), 0)

    def _get_stepper(self) -> StepperDialog:
        """Get or create the stepper dialog."""
        if self._stepper is None:
            self._stepper = self._create_stepper()
        return self._stepper

    # --- Properties ---

    @property
    def default_value(self) -> float:
        """The default value to reset to on right-click."""
        return self._default_value

    @default_value.setter
    def default_value(self, value: float) -> None:
        self._default_value = value

    def setDefaultValue(self, value: float) -> None:
        """Set the default value.

        Args:
            value: The value to reset to on right-click.
        """
        self.default_value = value

    def defaultValue(self) -> float:
        """Get the default value.

        Returns:
            The default value.
        """
        return self.default_value

    @property
    def drag_step_multiplier(self) -> float:
        """Base multiplier for drag sensitivity."""
        return self._drag_step_multiplier

    @drag_step_multiplier.setter
    def drag_step_multiplier(self, value: float) -> None:
        self._drag_step_multiplier = value

    def setDragStepMultiplier(self, value: float) -> None:
        """Set the drag step multiplier.

        Args:
            value: Multiplier for drag sensitivity.
        """
        self.drag_step_multiplier = value

    def dragStepMultiplier(self) -> float:
        """Get the drag step multiplier.

        Returns:
            The drag step multiplier.
        """
        return self.drag_step_multiplier

    @property
    def stepper(self) -> StepperDialog:
        """The stepper dialog instance."""
        return self._get_stepper()

    # --- Event Handling ---

    def eventFilter(
        self, obj: QtCore.QObject, event: QtCore.QEvent
    ) -> bool:
        """Filter events on the line edit for middle-click stepper."""
        if obj == self.lineEdit():
            if event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == Qt.MiddleButton:
                    self._show_stepper()
        return super().eventFilter(obj, event)

    def _show_stepper(self) -> None:
        """Show the stepper dialog."""
        self._get_stepper().show()

    def stepBy(self, steps: int) -> None:
        """Override stepBy to prevent stepping during drag."""
        if not self._is_dragging:
            super().stepBy(steps)

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        """Handle mouse press - start potential drag operation."""
        pos = get_event_pos(event)
        self._mouse_start_pos_y = pos.y()
        self._drag_start_value = self.value()
        self._original_value = self.value()
        self._is_dragging = False
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        """Handle mouse move - drag to adjust value."""
        pos = get_event_pos(event)

        # Start dragging if cursor leaves bounds or already dragging
        if (
            pos.y() < self.rect().top()
            or pos.y() > self.rect().bottom()
            or self._is_dragging
        ):
            self.setCursor(Qt.SizeVerCursor)
            self._is_dragging = True

            # Calculate multiplier with modifiers
            mult = self._drag_step_multiplier
            modifiers = event.modifiers()

            if modifiers & Qt.ControlModifier:
                mult *= self._fine_multiplier
            elif modifiers & Qt.ShiftModifier:
                mult *= self._coarse_multiplier

            # Calculate and apply new value
            drag_delta = (self._mouse_start_pos_y - pos.y()) * mult
            self.setValue(self._drag_start_value + drag_delta)
        else:
            # Update start value if not dragging yet
            self._drag_start_value = self.value()

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        """Handle mouse release - end drag operation."""
        super().mouseReleaseEvent(event)
        self.unsetCursor()
        self._is_dragging = False

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        """Handle key press - ESC restores original value."""
        if event.key() == Qt.Key_Escape and self._is_dragging:
            self.setValue(self._original_value)
            self.unsetCursor()
            self._is_dragging = False
        else:
            super().keyPressEvent(event)

    def contextMenuEvent(self, event: QtGui.QContextMenuEvent) -> None:
        """Handle context menu - right-click on buttons resets to default."""
        style = self.style()
        opt = QtWidgets.QStyleOptionSpinBox()
        self.initStyleOption(opt)

        up_rect = style.subControlRect(
            QtWidgets.QStyle.CC_SpinBox,
            opt,
            QtWidgets.QStyle.SC_SpinBoxUp,
            self,
        )
        down_rect = style.subControlRect(
            QtWidgets.QStyle.CC_SpinBox,
            opt,
            QtWidgets.QStyle.SC_SpinBoxDown,
            self,
        )
        buttons_rect = up_rect.united(down_rect)

        pos = get_event_pos(event)
        if buttons_rect.contains(pos):
            self.setValue(self._default_value)
            self.selectAll()
        else:
            super().contextMenuEvent(event)


class SpinBox(_SpinBoxMixin, QtWidgets.QSpinBox):
    """Enhanced integer spinbox with DCC-style features.

    Features:
    - Middle-click to open stepper dialog (Houdini-style value ladder)
    - Drag vertically on spinbox to adjust value (3ds Max-style)
    - Hold Ctrl while dragging for fine adjustment (0.1x)
    - Hold Shift while dragging for coarse adjustment (10x)
    - Press ESC during drag to restore original value
    - Right-click on up/down buttons to reset to default value

    Example:
        spinbox = SpinBox()
        spinbox.setRange(-1000, 1000)
        spinbox.setDefaultValue(0)
        spinbox.setValue(50)
    """

    def __init__(self, parent: Optional[QtWidgets.QWidget] = None) -> None:
        """Initialize the spinbox.

        Args:
            parent: Optional parent widget.
        """
        super().__init__(parent)
        self._init_dcc_features()

    def _update_stepper_steps(self, stepper: StepperDialog) -> None:
        """Update stepper steps for integer spinbox."""
        stepper.auto_generate_steps(int(abs(self.maximum())), 0)

    def setRange(self, minimum: int, maximum: int) -> None:
        """Set the spinbox range.

        Args:
            minimum: Minimum value.
            maximum: Maximum value.
        """
        super().setRange(minimum, maximum)
        if self._stepper is not None:
            self._update_stepper_steps(self._stepper)

    def setMinimum(self, minimum: int) -> None:
        """Set the minimum value.

        Args:
            minimum: Minimum value.
        """
        super().setMinimum(minimum)
        if self._stepper is not None:
            self._update_stepper_steps(self._stepper)

    def setMaximum(self, maximum: int) -> None:
        """Set the maximum value.

        Args:
            maximum: Maximum value.
        """
        super().setMaximum(maximum)
        if self._stepper is not None:
            self._update_stepper_steps(self._stepper)


class DoubleSpinBox(_SpinBoxMixin, QtWidgets.QDoubleSpinBox):
    """Enhanced double spinbox with DCC-style features.

    Features:
    - Middle-click to open stepper dialog (Houdini-style value ladder)
    - Drag vertically on spinbox to adjust value (3ds Max-style)
    - Hold Ctrl while dragging for fine adjustment (0.1x)
    - Hold Shift while dragging for coarse adjustment (10x)
    - Press ESC during drag to restore original value
    - Right-click on up/down buttons to reset to default value

    Example:
        spinbox = DoubleSpinBox()
        spinbox.setRange(-100.0, 100.0)
        spinbox.setDecimals(3)
        spinbox.setDefaultValue(0.0)
        spinbox.setValue(1.5)
    """

    def __init__(self, parent: Optional[QtWidgets.QWidget] = None) -> None:
        """Initialize the spinbox.

        Args:
            parent: Optional parent widget.
        """
        super().__init__(parent)
        self._init_dcc_features()

    def _update_stepper_steps(self, stepper: StepperDialog) -> None:
        """Update stepper steps for double spinbox."""
        stepper.auto_generate_steps(int(abs(self.maximum())), self.decimals())

    def setRange(self, minimum: float, maximum: float) -> None:
        """Set the spinbox range.

        Args:
            minimum: Minimum value.
            maximum: Maximum value.
        """
        super().setRange(minimum, maximum)
        if self._stepper is not None:
            self._update_stepper_steps(self._stepper)

    def setMinimum(self, minimum: float) -> None:
        """Set the minimum value.

        Args:
            minimum: Minimum value.
        """
        super().setMinimum(minimum)
        if self._stepper is not None:
            self._update_stepper_steps(self._stepper)

    def setMaximum(self, maximum: float) -> None:
        """Set the maximum value.

        Args:
            maximum: Maximum value.
        """
        super().setMaximum(maximum)
        if self._stepper is not None:
            self._update_stepper_steps(self._stepper)

    def setDecimals(self, decimals: int) -> None:
        """Set the number of decimal places.

        Args:
            decimals: Number of decimal places to display.
        """
        super().setDecimals(decimals)
        if self._stepper is not None:
            self._update_stepper_steps(self._stepper)
