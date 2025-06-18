@echo off
title VoltageVPN Mobile - Free VPN for Android & iOS
color 0A

echo.
echo ========================================
echo    VoltageVPN Mobile - Android & iOS
echo ========================================
echo.
echo Starting mobile-optimized VPN service...
echo.
echo Features:
echo   📱 Touch-friendly interface
echo   🌍 Works on ALL mobile apps
echo   🔋 Battery optimized
echo   📶 No app installation required
echo   🆓 Completely FREE
echo.
echo Mobile Dashboard will be available at:
echo   📱 http://localhost:8081/mobile
echo.
echo Instructions:
echo   1. Open Chrome/Firefox (Android) or Safari (iOS)
echo   2. Visit: http://your-ip:8081/mobile
echo   3. Tap any server to connect
echo   4. Your mobile IP changes instantly!
echo.
echo Starting VoltageVPN Mobile...
echo.

python mobile_vpn_solution.py

pause
