@echo off
chcp 65001 >nul
echo ========================================
echo   Push to GitHub Repository
echo ========================================
echo.
echo Repository: https://github.com/awaleayush777/sunspots_predictor_2.0
echo Branch: main
echo.
echo This will push your code to GitHub.
echo You will be prompted for authentication.
echo.
echo Options:
echo   1. Username: awaleayush777
echo   2. Password: Use Personal Access Token (not GitHub password)
echo.
echo To create a token:
echo   https://github.com/settings/tokens
echo.
pause
echo.
echo Pushing to GitHub...
git push -u origin main
echo.
if %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] Code pushed to GitHub successfully!
    echo.
    echo View your repository at:
    echo https://github.com/awaleayush777/sunspots_predictor_2.0
) else (
    echo [ERROR] Push failed. Check the error message above.
    echo.
    echo Common issues:
    echo - Authentication failed: Use Personal Access Token
    echo - Network error: Check internet connection
    echo - Permission denied: Check repository access
    echo.
    echo See GITHUB_SETUP.md for detailed instructions.
)
echo.
pause

