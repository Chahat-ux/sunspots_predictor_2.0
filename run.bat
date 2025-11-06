@echo off
chcp 65001 >nul
echo ========================================
echo   Sunspot Prediction Web Application
echo ========================================
echo.
echo Starting server...
echo.
echo Once started, open your browser and go to:
echo   http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.
cd /d "%~dp0"
.venv\Scripts\python start_app.py
pause

