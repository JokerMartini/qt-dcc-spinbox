# Project Guidelines

## Overview
DCC-style spinbox widgets (Houdini/3ds Max style) for PySide2 and PySide6. Features middle-click stepper dialog for precise value control with dynamic step increments.

## Environment
- Python interpreter: `C:\Program Files\Python310\python.exe`
- PySide2: 5.15.2.1
- PySide6: 6.9.1

## Project Structure
```
qt-dcc-spinbox/
├── qt_dcc_spinbox/
│   ├── __init__.py          # public API exports
│   ├── _qt.py               # PySide2/PySide6 compatibility shim
│   ├── spinbox.py           # SpinBox, DoubleSpinBox (unified)
│   ├── stepper.py           # StepButton, StepperDialog
│   └── utils.py             # helpers (mouse position, step generation)
├── examples/
│   └── demo.py              # usage examples
├── tests/
│   └── test_spinbox.py      # widget tests
└── pyproject.toml           # package config
```

## Code Style
- Follow PEP 8 strictly
- Use type hints for all function signatures
- Maximum line length: 88 characters

## Documentation
- Use Google-style docstrings for all public functions and classes
- Include Args, Returns, and Raises sections where applicable
- Module-level docstrings describing purpose

## Testing
- Tests located in `tests/` directory
- Use `pytest-qt` for widget testing
- Run demo: `python examples/demo.py`
- Run tests (Windows):
  ```
  set QT_BINDING=pyside2 && python -m pytest tests/
  set QT_BINDING=pyside6 && python -m pytest tests/
  ```
- Run tests (Linux/Mac):
  ```
  QT_BINDING=pyside2 pytest tests/
  QT_BINDING=pyside6 pytest tests/
  ```

## PySide2/PySide6 Compatibility
Key API differences to handle:
| Area | PySide2 | PySide6 |
|------|---------|---------|
| exec | `app.exec_()` | `app.exec()` |
| Mouse position | `event.pos()` | `event.position().toPoint()` |
| Global position | `event.globalPos()` | `event.globalPosition().toPoint()` |
| QAction | `QtWidgets.QAction` | `QtGui.QAction` |

Use `_qt.py` shim for imports, `utils.py` helpers for mouse position.

## Implemented Features
- Vertical click-drag on spinbox to adjust value
- Middle-click stepper dialog (Houdini-style value ladder)
- Keyboard modifiers: Ctrl=fine (0.1x), Shift=coarse (10x)
- ESC key to restore original value during drag
- Right-click on buttons to reset to default value
- Auto-generated step values based on range and decimals

## Backlog
- Cursor wrapping at screen edges during drag
- Enhanced visual feedback (drag state indicator)
- Configurable stepper position (above/below vs centered)
