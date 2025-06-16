@echo off
title VPN Browser API Server - Production Ready
color 0A

echo.
echo ========================================
echo   🚀 VPN BROWSER API SERVER v2.0.0
echo ========================================
echo   Production Ready - All Limitations Solved
echo ========================================
echo.

echo [INFO] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not found in PATH
    echo [INFO] Please install Python from https://python.org
    pause
    exit /b 1
)

echo [OK] Python detected
echo.

echo [INFO] Checking dependencies...
if not exist "requirements_api.txt" (
    echo [ERROR] requirements_api.txt file not found
    pause
    exit /b 1
)

echo [INFO] Installing dependencies...
pip install -r requirements_api.txt

if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    echo [INFO] Trying with --user flag...
    pip install --user -r requirements_api.txt
)

echo [OK] Dependencies installed
echo.

echo [INFO] Checking API server...
if not exist "vpn_browser_api.py" (
    echo [ERROR] vpn_browser_api.py file not found
    pause
    exit /b 1
)

echo [OK] API server found
echo.

echo ========================================
echo   🚀 STARTING PRODUCTION SERVER
echo ========================================
echo.
echo   📡 API: http://localhost:8080
echo   🎛️ Dashboard: http://localhost:8080
echo   📖 Examples: http://localhost:8080/examples
echo   🎯 Widget: http://localhost:8080/widget
echo   📦 SDK: http://localhost:8080/sdk.js
echo   ⚙️ Install: http://localhost:8080/install.js
echo.
echo   ✅ All limitations solved:
echo   • Direct browser control
echo   • Free servers included
echo   • Automatic certificates
echo   • Zero-touch configuration
echo   • Complete REST API
echo   • JavaScript SDK
echo   • Embeddable widget
echo.
echo ========================================
echo.

echo [INFO] Starting production server...
echo [INFO] Press Ctrl+C to stop
echo.

python vpn_browser_api.py

echo.
echo [INFO] Server stopped
pause
