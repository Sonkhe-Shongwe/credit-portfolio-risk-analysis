@echo off
setlocal
set "report=%~dp0power-bi\Credit Portfolio.pbip"
if not exist "%report%" (
    echo The Power BI project is missing. Pull the latest files in GitHub Desktop.
    pause
    exit /b 1
)
start "" "%report%"
if errorlevel 1 (
    echo Open this project from File ^> Open in Power BI Desktop:
    echo "%report%"
    pause
    exit /b 1
)
