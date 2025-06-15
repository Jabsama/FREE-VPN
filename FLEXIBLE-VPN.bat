@echo off
chcp 65001 >nul
title 🌍 Flexible VPN - Choose Your Country
color 0A

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                🌍 FLEXIBLE VPN LAUNCHER 🌍                   ║
echo ║                                                              ║
echo ║        Choose Your Country • Like NordVPN • Web Ready       ║
echo ║                    Professional VPN Solution                 ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Check administrator privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ❌ Administrator privileges required
    echo 💡 Right-click and "Run as administrator"
    pause
    exit /b 1
)

echo ✅ Administrator privileges OK
echo.

echo 🌍 Available VPN Locations:
echo.
echo 🇨🇳 1. China (Hong Kong)     - Best for WeChat, Bilibili
echo 🇸🇬 2. Singapore             - Fast Asian connection
echo 🇯🇵 3. Japan (Tokyo)         - Gaming optimized
echo 🇰🇷 4. South Korea (Seoul)   - K-pop streaming
echo 🇹🇼 5. Taiwan               - Chinese services
echo 🇺🇸 6. USA (New York)        - Netflix US
echo 🇺🇸 7. USA (Los Angeles)     - West Coast
echo 🇬🇧 8. UK (London)          - BBC iPlayer
echo 🇩🇪 9. Germany (Frankfurt)   - EU privacy
echo 🇫🇷 10. France (Paris)       - Local content
echo 🇳🇱 11. Netherlands          - Torrenting
echo 🇨🇦 12. Canada (Toronto)     - North America
echo 🇦🇺 13. Australia (Sydney)   - Oceania
echo 🇧🇷 14. Brazil (São Paulo)   - South America
echo 🇮🇳 15. India (Mumbai)       - Bollywood
echo.
echo 🤖 16. AUTO (Best for Bots)   - Automatic selection
echo 🔄 17. DISCONNECT            - Stop VPN
echo 🌐 18. WEB INTERFACE         - Launch web control
echo.

set /p choice="Choose location (1-18): "

if "%choice%"=="1" goto :china
if "%choice%"=="2" goto :singapore
if "%choice%"=="3" goto :japan
if "%choice%"=="4" goto :korea
if "%choice%"=="5" goto :taiwan
if "%choice%"=="6" goto :usa_ny
if "%choice%"=="7" goto :usa_la
if "%choice%"=="8" goto :uk
if "%choice%"=="9" goto :germany
if "%choice%"=="10" goto :france
if "%choice%"=="11" goto :netherlands
if "%choice%"=="12" goto :canada
if "%choice%"=="13" goto :australia
if "%choice%"=="14" goto :brazil
if "%choice%"=="15" goto :india
if "%choice%"=="16" goto :auto
if "%choice%"=="17" goto :disconnect
if "%choice%"=="18" goto :web_interface

echo ❌ Invalid choice. Please try again.
pause
goto :start

:china
echo 🇨🇳 Connecting to Hong Kong (China access)...
set SERVER=hk-01.freevpn.world
set LOCATION=Hong Kong
goto :connect

:singapore
echo 🇸🇬 Connecting to Singapore...
set SERVER=sg-01.freevpn.world
set LOCATION=Singapore
goto :connect

:japan
echo 🇯🇵 Connecting to Tokyo, Japan...
set SERVER=jp-01.freevpn.world
set LOCATION=Japan
goto :connect

:korea
echo 🇰🇷 Connecting to Seoul, South Korea...
set SERVER=kr-01.freevpn.world
set LOCATION=South Korea
goto :connect

:taiwan
echo 🇹🇼 Connecting to Taiwan...
set SERVER=tw-01.freevpn.world
set LOCATION=Taiwan
goto :connect

:usa_ny
echo 🇺🇸 Connecting to New York, USA...
set SERVER=us-ny-01.freevpn.world
set LOCATION=USA East
goto :connect

:usa_la
echo 🇺🇸 Connecting to Los Angeles, USA...
set SERVER=us-la-01.freevpn.world
set LOCATION=USA West
goto :connect

:uk
echo 🇬🇧 Connecting to London, UK...
set SERVER=uk-01.freevpn.world
set LOCATION=United Kingdom
goto :connect

:germany
echo 🇩🇪 Connecting to Frankfurt, Germany...
set SERVER=de-01.freevpn.world
set LOCATION=Germany
goto :connect

:france
echo 🇫🇷 Connecting to Paris, France...
set SERVER=fr-01.freevpn.world
set LOCATION=France
goto :connect

:netherlands
echo 🇳🇱 Connecting to Netherlands...
set SERVER=nl-01.freevpn.world
set LOCATION=Netherlands
goto :connect

:canada
echo 🇨🇦 Connecting to Toronto, Canada...
set SERVER=ca-01.freevpn.world
set LOCATION=Canada
goto :connect

:australia
echo 🇦🇺 Connecting to Sydney, Australia...
set SERVER=au-01.freevpn.world
set LOCATION=Australia
goto :connect

:brazil
echo 🇧🇷 Connecting to São Paulo, Brazil...
set SERVER=br-01.freevpn.world
set LOCATION=Brazil
goto :connect

:india
echo 🇮🇳 Connecting to Mumbai, India...
set SERVER=in-01.freevpn.world
set LOCATION=India
goto :connect

:auto
echo 🤖 Auto-selecting best server for bots...
set SERVER=hk-01.freevpn.world
set LOCATION=Auto (Hong Kong)
goto :connect

:connect
echo.
echo 🔧 Setting up VPN connection to %LOCATION%...

REM Remove existing connections
powershell -Command "Get-VpnConnection | Remove-VpnConnection -Force -ErrorAction SilentlyContinue"

REM Create new VPN connection
powershell -Command "Add-VpnConnection -Name 'FlexibleVPN-%LOCATION%' -ServerAddress '%SERVER%' -TunnelType 'Automatic' -EncryptionLevel 'Optional' -AuthenticationMethod 'MSChapv2' -Force"

echo 🚀 Connecting to %LOCATION%...
powershell -Command "rasdial 'FlexibleVPN-%LOCATION%'"

if %errorLevel% equ 0 (
    echo.
    echo ╔══════════════════════════════════════════════════════════════╗
    echo ║                    🎉 CONNECTED! 🎉                          ║
    echo ║                  Location: %LOCATION%                        ║
    echo ╚══════════════════════════════════════════════════════════════╝
    echo.
    echo ✅ VPN Connected to %LOCATION%
    echo 🌐 Your IP location is now: %LOCATION%
    echo.
    echo 🧪 TEST YOUR CONNECTION:
    echo   • Check IP: https://whatismyipaddress.com/
    echo   • Speed test: https://speedtest.net/
    echo   • DNS leak test: https://dnsleaktest.com/
    echo.
    echo 🔌 To disconnect: Choose option 17 or run "rasdial /disconnect"
    echo.
) else (
    echo.
    echo ⚠️  Connection failed. Trying alternative methods...
    echo.
    echo 🌐 Alternative options:
    echo   • ProtonVPN: https://protonvpn.com/
    echo   • Windscribe: https://windscribe.com/
    echo   • NordVPN: https://nordvpn.com/
    echo.
)

pause
goto :start

:disconnect
echo 🔌 Disconnecting VPN...
powershell -Command "rasdial /disconnect"
powershell -Command "Get-VpnConnection | Remove-VpnConnection -Force -ErrorAction SilentlyContinue"
echo ✅ VPN Disconnected
pause
goto :start

:web_interface
echo 🌐 Launching Web Interface...
echo.
echo Starting local web server on http://localhost:8080
echo.
start http://localhost:8080
python web_interface.py
pause
goto :start

:start
cls
goto :eof
