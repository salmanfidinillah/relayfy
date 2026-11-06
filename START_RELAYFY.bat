@echo off
cd /d "%~dp0"
where py >nul 2>&1
if %errorlevel% equ 0 (
  py -3 run_demo.py
) else (
  python run_demo.py
)
pause
