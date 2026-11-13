@echo off
setlocal
where py.exe >nul 2>&1
if errorlevel 1 goto use_python
py -3 "%~dp0scripts\open_power_bi.py"
goto finish

:use_python
python "%~dp0scripts\open_power_bi.py"

:finish
if errorlevel 1 (
    pause
    exit /b 1
)
