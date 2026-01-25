"""Tests for DCC spinbox widgets."""

import pytest

from qt_dcc_spinbox import SpinBox, DoubleSpinBox, QT_BINDING
from qt_dcc_spinbox.utils import (
    generate_whole_incrementers,
    generate_decimal_incrementers,
    generate_steps,
)


class TestUtils:
    """Tests for utility functions."""

    def test_generate_whole_incrementers_1000(self) -> None:
        """Test whole incrementers for max value 1000."""
        result = generate_whole_incrementers(1000)
        assert result == [100, 10, 1]

    def test_generate_whole_incrementers_100(self) -> None:
        """Test whole incrementers for max value 100."""
        result = generate_whole_incrementers(100)
        assert result == [10, 1]

    def test_generate_whole_incrementers_10(self) -> None:
        """Test whole incrementers for max value 10."""
        result = generate_whole_incrementers(10)
        assert result == [1]

    def test_generate_whole_incrementers_zero(self) -> None:
        """Test whole incrementers for zero returns [1]."""
        result = generate_whole_incrementers(0)
        assert result == [1]

    def test_generate_decimal_incrementers_3(self) -> None:
        """Test decimal incrementers for 3 decimal places."""
        result = generate_decimal_incrementers(3)
        assert result == [0.1, 0.01, 0.001]

    def test_generate_decimal_incrementers_zero(self) -> None:
        """Test decimal incrementers for 0 decimal places."""
        result = generate_decimal_incrementers(0)
        assert result == []

    def test_generate_steps_combined(self) -> None:
        """Test combined step generation."""
        result = generate_steps(100, 2)
        assert result == [10, 1, 0.1, 0.01]


class TestSpinBox:
    """Tests for SpinBox widget."""

    def test_create_spinbox(self, qtbot) -> None:
        """Test basic spinbox creation."""
        spinbox = SpinBox()
        qtbot.addWidget(spinbox)
        assert spinbox.value() == 0

    def test_set_range(self, qtbot) -> None:
        """Test setting range."""
        spinbox = SpinBox()
        qtbot.addWidget(spinbox)
        spinbox.setRange(-100, 100)
        assert spinbox.minimum() == -100
        assert spinbox.maximum() == 100

    def test_set_default_value(self, qtbot) -> None:
        """Test setting default value."""
        spinbox = SpinBox()
        qtbot.addWidget(spinbox)
        spinbox.setDefaultValue(50)
        assert spinbox.defaultValue() == 50

    def test_set_value(self, qtbot) -> None:
        """Test setting value."""
        spinbox = SpinBox()
        qtbot.addWidget(spinbox)
        spinbox.setRange(-1000, 1000)
        spinbox.setValue(500)
        assert spinbox.value() == 500

    def test_stepper_exists(self, qtbot) -> None:
        """Test that stepper dialog is created on access."""
        spinbox = SpinBox()
        qtbot.addWidget(spinbox)
        assert spinbox.stepper is not None

    def test_drag_multiplier(self, qtbot) -> None:
        """Test drag step multiplier."""
        spinbox = SpinBox()
        qtbot.addWidget(spinbox)
        spinbox.setDragStepMultiplier(1.0)
        assert spinbox.dragStepMultiplier() == 1.0


class TestDoubleSpinBox:
    """Tests for DoubleSpinBox widget."""

    def test_create_double_spinbox(self, qtbot) -> None:
        """Test basic double spinbox creation."""
        spinbox = DoubleSpinBox()
        qtbot.addWidget(spinbox)
        assert spinbox.value() == 0.0

    def test_set_decimals(self, qtbot) -> None:
        """Test setting decimal places."""
        spinbox = DoubleSpinBox()
        qtbot.addWidget(spinbox)
        spinbox.setDecimals(4)
        assert spinbox.decimals() == 4

    def test_set_range_float(self, qtbot) -> None:
        """Test setting float range."""
        spinbox = DoubleSpinBox()
        qtbot.addWidget(spinbox)
        spinbox.setRange(-1.5, 1.5)
        assert spinbox.minimum() == -1.5
        assert spinbox.maximum() == 1.5

    def test_stepper_steps_update_on_decimals(self, qtbot) -> None:
        """Test that stepper steps update when decimals change."""
        spinbox = DoubleSpinBox()
        qtbot.addWidget(spinbox)
        spinbox.setRange(-100, 100)
        spinbox.setDecimals(3)
        # Access stepper to trigger creation
        steps = spinbox.stepper.steps
        assert 0.001 in steps
