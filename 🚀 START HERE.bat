@echo off
chcp 65001 >nul
title 🌍 FREE VPN - Choose Your Experience
color 0A

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    🌍 FREE VPN LAUNCHER 🌍                   ║
echo ║                                                              ║
echo ║              Welcome! Choose your VPN experience            ║
echo ║                     Made with ❤️ for you                     ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🎯 What do you want to do?
echo.
echo 🇨🇳 1. CHINA VPN (Quick)      - Instant China connection for WeChat
echo 🌍 2. FLEXIBLE VPN (Pro)      - Choose from 15 countries like NordVPN
echo 🌐 3. WEB INTERFACE           - Professional web control panel
echo 🤖 4. BOT INTEGRATION         - Setup for WeChat bots
echo 📖 5. DOCUMENTATION           - Read the guides
echo 🔧 6. CUSTOM SERVER           - Use your own VPN server
echo.
echo ❓ 7. HELP                    - Get support
echo 🚪 8. EXIT                    - Close this launcher
echo.

set /p choice="Choose option (1-8): "

if "%choice%"=="1" goto :china_quick
if "%choice%"=="2" goto :flexible
if "%choice%"=="3" goto :web_interface
if "%choice%"=="4" goto :bot_setup
if "%choice%"=="5" goto :documentation
if "%choice%"=="6" goto :custom_server
if "%choice%"=="7" goto :help
if "%choice%"=="8" goto :exit

echo ❌ Invalid choice. Please try again.
pause
goto :start

:china_quick
echo.
echo 🇨🇳 Launching China VPN (Quick Mode)...
echo ⚡ Perfect for WeChat, Bilibili, Chinese services
echo.
call "ONE-CLICK-VPN.bat"
goto :start

:flexible
echo.
echo 🌍 Launching Flexible VPN (Professional Mode)...
echo 🌐 Choose from 15 countries worldwide
echo.
call "FLEXIBLE-VPN.bat"
goto :start

:web_interface
echo.
echo 🌐 Starting Web Interface...
echo 📱 Access at: http://localhost:8080
echo.
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Starting web server...
python web_interface.py
pause
goto :start

:bot_setup
echo.
echo 🤖 Bot Integration Setup
echo.
echo This will help you integrate the VPN with your bots.
echo.
echo 📖 Opening bot integration guide...
start docs\bot-sha-256-integration.md
echo.
echo 🇨🇳 For WeChat bots, use China VPN option (1)
echo 🌍 For multi-platform bots, use Flexible VPN option (2)
echo.
pause
goto :start

:documentation
echo.
echo 📖 Opening Documentation...
echo.
start README.md
start docs\flexible-vpn-guide.md
echo.
echo 📚 Documentation opened in your default editor
pause
goto :start

:custom_server
echo.
echo 🔧 Custom Server Setup
echo.
echo This option is for advanced users who want to use their own VPN server.
echo.
call "LAUNCH-VPN.bat"
goto :start

:help
echo.
echo ❓ HELP & SUPPORT
echo.
echo 🌐 GitHub Repository: https://github.com/Jabsama/FREE-VPN
echo 📧 Issues: https://github.com/Jabsama/FREE-VPN/issues
echo 📖 Documentation: README.md
echo.
echo 🚀 Quick Start:
echo   • For WeChat: Choose option 1 (China VPN)
echo   • For multiple countries: Choose option 2 (Flexible VPN)
echo   • For website integration: Choose option 3 (Web Interface)
echo.
echo 🤖 Bot Integration:
echo   • WeChat bots need China IP (option 1)
echo   • Multi-platform bots use Flexible VPN (option 2)
echo.
echo ⚠️  Troubleshooting:
echo   • Run as Administrator
echo   • Check internet connection
echo   • Disable antivirus temporarily if needed
echo.
pause
goto :start

:exit
echo.
echo 👋 Thank you for using FREE VPN!
echo 🌟 Don't forget to star us on GitHub: https://github.com/Jabsama/FREE-VPN
echo.
pause
exit

:start
cls
goto :eof
