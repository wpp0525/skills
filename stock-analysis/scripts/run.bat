@echo off
REM Stock Analysis Runner - Windows
REM This script runs the stock analysis directly using local Python

setlocal

REM Get the script directory
set "SCRIPT_DIR=%~dp0"

REM Check if stock code is provided
if "%~1"=="" (
    echo Usage: run.bat ^<stock_code^>
    echo Example: run.bat 000001
    exit /b 1
)

REM Run the analysis (pass current directory as output directory)
python "%SCRIPT_DIR%analyze_stock.py" %1 --output-dir %CD%
