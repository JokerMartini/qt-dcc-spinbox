# qt-dcc-spinbox

DCC-style spinbox widgets for PySide2 and PySide6, inspired by Houdini and 3ds Max.

https://github.com/user-attachments/assets/46681d75-7ede-4191-ab24-8baff8590fee

## Features

- **Vertical drag** - Click and drag vertically on the spinbox to adjust values (3ds Max style)
- **Value ladder** - Middle-click to open a stepper dialog with precise step control (Houdini style)
- **Modifier keys** - Hold Ctrl for fine (0.1x), Alt for precision (0.01x), Shift for coarse (10x)
- **ESC to cancel** - Press Escape during drag to restore the original value
- **Default value** - Right-click on up/down buttons to reset to a configurable default
- **Auto-generated steps** - Step values automatically adapt to your range and decimal settings
- **Cross-compatible** - Works with both PySide2 and PySide6

## Installation

```bash
# Install with PySide6 (recommended)
pip install qt-dcc-spinbox[pyside6]

# Or with PySide2
pip install qt-dcc-spinbox[pyside2]

# Or install without Qt dependency (if already installed)
pip install qt-dcc-spinbox
```

### From source

```bash
git clone https://github.com/JokerMartini/qt-dcc-spinbox.git
cd qt-dcc-spinbox
pip install -e .
```

## Quick Start

```python
from qt_dcc_spinbox import SpinBox, DoubleSpinBox

# Integer spinbox
spinbox = SpinBox()
spinbox.setRange(-1000, 1000)
spinbox.setDefaultValue(0)
spinbox.setValue(100)

# Double spinbox with 3 decimal places
double_spinbox = DoubleSpinBox()
double_spinbox.setRange(-100.0, 100.0)
double_spinbox.setDecimals(3)
double_spinbox.setDefaultValue(0.0)
double_spinbox.setValue(1.5)
```

## Usage

### Basic Usage

The spinboxes work as drop-in replacements for `QSpinBox` and `QDoubleSpinBox`:

```python
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget
from qt_dcc_spinbox import SpinBox, DoubleSpinBox

app = QApplication([])

window = QWidget()
layout = QVBoxLayout(window)

# Add spinboxes
int_spin = SpinBox()
int_spin.setRange(0, 100)
layout.addWidget(int_spin)

float_spin = DoubleSpinBox()
float_spin.setRange(0.0, 1.0)
float_spin.setDecimals(4)
layout.addWidget(float_spin)

window.show()
app.exec()
```

### Interaction Guide

| Action | Effect |
|--------|--------|
| Drag vertically | Adjust value up/down |
| Ctrl + drag | Fine adjustment (0.1x speed) |
| Alt + drag | Precision adjustment (0.01x speed) |
| Shift + drag | Coarse adjustment (10x speed) |
| Middle-click | Open value ladder (stepper dialog) |
| Middle-drag horizontally | Adjust by selected step amount |
| ESC (while dragging) | Cancel and restore original value |
| Right-click on buttons | Reset to default value |

### Customization

```python
from qt_dcc_spinbox import SpinBox

spinbox = SpinBox()

# Set the default value (for right-click reset)
spinbox.setDefaultValue(50)

# Drag sensitivity is auto-calculated from range by default.
# Override with a fixed value if needed:
spinbox.setDragStepMultiplier(1.0)

# Or adjust how many pixels of drag to traverse the full range:
spinbox.setPixelsForFullRange(300)  # Default is 500

# Customize the stepper dialog
spinbox.stepper.set_threshold(20)  # Pixels per step (default: 10)
spinbox.stepper.set_steps([100, 50, 10, 5, 1])  # Custom step values
```

### Forcing a Qt Binding

By default, the package auto-detects PySide6 first, then falls back to PySide2. To force a specific binding:

```python
import os
os.environ["QT_BINDING"] = "pyside2"  # or "pyside6"

# Must be set BEFORE importing qt_dcc_spinbox
from qt_dcc_spinbox import SpinBox
```

Or via environment variable:

```bash
# Windows
set QT_BINDING=pyside2 && python your_app.py

# Linux/Mac
QT_BINDING=pyside2 python your_app.py
```

## API Reference

### SpinBox

Enhanced `QSpinBox` with DCC-style features.

| Method | Description |
|--------|-------------|
| `setDefaultValue(value)` | Set the value to reset to on right-click |
| `defaultValue()` | Get the default value |
| `setDragStepMultiplier(value)` | Override auto drag sensitivity with a fixed value |
| `dragStepMultiplier()` | Get the drag sensitivity (None = auto) |
| `setPixelsForFullRange(pixels)` | Set pixels of drag for full range traversal (default: 500) |
| `stepper` | Access the `StepperDialog` instance |

### DoubleSpinBox

Enhanced `QDoubleSpinBox` with DCC-style features. Same API as `SpinBox`.

### StepperDialog

The value ladder popup dialog.

| Method | Description |
|--------|-------------|
| `set_steps(steps)` | Set custom step values (list of floats) |
| `set_threshold(pixels)` | Set horizontal drag threshold per step |
| `auto_generate_steps(max, decimals)` | Auto-generate steps from range |

## Development

This project uses [uv](https://docs.astral.sh/uv/) for fast dependency management and testing.

### Setup

```bash
# Clone and install in development mode
git clone https://github.com/JokerMartini/qt-dcc-spinbox.git
cd qt-dcc-spinbox
uv sync --extra pyside6 --extra dev
```

### Running the Demo

```bash
uv run --extra pyside6 -- python examples/demo.py
```

### Running Tests

```bash
# Run all tests against both bindings (Windows)
scripts\test.bat

# Or run individually
uv run --extra pyside2 --extra dev -- python -m pytest tests/ -v
uv run --extra pyside6 --extra dev -- python -m pytest tests/ -v
```

# Run all tests (both PySide2 & PySide6)
`scripts\test.bat`

# Run individually
`uv run --extra pyside2 --extra dev -- python -m pytest tests/ -v`
`uv run --extra pyside6 --extra dev -- python -m pytest tests/ -v`

# Run demo
`uv run --extra pyside6 -- python examples/demo.py`


## Requirements

- Python 3.10 (pinned via `.python-version` for PySide2 compatibility)
- PySide2 >= 5.15 or PySide6 >= 6.0

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Acknowledgments

Inspired by the excellent spinbox implementations in:
- [SideFX Houdini](https://www.sidefx.com/) - Value ladder concept
- [Autodesk 3ds Max](https://www.autodesk.com/products/3ds-max/) - Click-drag interaction
