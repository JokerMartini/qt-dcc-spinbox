@echo off
echo ============================================
echo   Testing qt-dcc-spinbox
echo ============================================
echo.

echo [1/2] Testing with PySide2...
echo --------------------------------------------
set QT_BINDING=pyside2
uv run --extra pyside2 --extra dev -- python -m pytest tests/ %*
if errorlevel 1 (
    echo PySide2 tests FAILED
) else (
    echo PySide2 tests PASSED
)
echo.

echo [2/2] Testing with PySide6...
echo --------------------------------------------
set QT_BINDING=pyside6
uv run --extra pyside6 --extra dev -- python -m pytest tests/ %*
if errorlevel 1 (
    echo PySide6 tests FAILED
) else (
    echo PySide6 tests PASSED
)
echo.
echo ============================================
echo   Done
echo ============================================
