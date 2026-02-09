@echo off
cd /d %~dp0
if exist .venv\Scripts\activate.bat (
  call .venv\Scripts\activate.bat
)
echo Running main.py
python main.py data/input/invoice.pdf
if %ERRORLEVEL% NEQ 0 (
  echo main.py exited with error %ERRORLEVEL%. Aborting.
  exit /b %ERRORLEVEL%
)
echo Running OEM matcher
python -m phase2_excel_to_web.utils.run_oem_match --debug --run-tests
