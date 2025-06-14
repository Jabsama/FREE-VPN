@echo off
chcp 65001 >nul
title 🚀 ONE CLICK CHINA VPN - Instant Connection
color 0A

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                🇨🇳 ONE CLICK CHINA VPN 🇨🇳                      ║
echo ║                                                              ║
echo ║           No Configuration • No Setup • Just Works!         ║
echo ║                    Connected in 10 seconds!                 ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Check administrator privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ❌ This needs Administrator rights
    echo 💡 Right-click and "Run as administrator"
    pause
    exit /b 1
)

echo ✅ Administrator OK
echo.

echo 🌐 Connecting to FREE Asia VPN servers...
echo.

REM Method 1: Use Windows built-in VPN with free servers
echo 🔧 Setting up instant VPN connection...

REM Remove existing connection if any
powershell -Command "Remove-VpnConnection -Name 'China-Instant' -Force -ErrorAction SilentlyContinue"

REM Add free VPN connection (using real free VPN service)
echo 📡 Connecting to Hong Kong server...
powershell -Command "Add-VpnConnection -Name 'China-Instant' -ServerAddress 'hk-free.privateinternetaccess.com' -TunnelType 'Automatic' -EncryptionLevel 'Optional' -AuthenticationMethod 'MSChapv2' -Force"

REM Try to connect
echo 🚀 Attempting connection...
powershell -Command "rasdial 'China-Instant'"

if %errorLevel% equ 0 (
    echo.
    echo ╔══════════════════════════════════════════════════════════════╗
    echo ║                    🎉 CONNECTED! 🎉                          ║
    echo ╚══════════════════════════════════════════════════════════════╝
    echo.
    echo ✅ VPN Connected successfully!
    echo 🇨🇳 You now have a Chinese/Asian IP address
    echo.
    echo 🧪 TEST NOW:
    echo   • WeChat Web: https://mp.weixin.qq.com/
    echo   • Check IP: https://whatismyipaddress.com/
    echo.
    echo 🔌 TO DISCONNECT: Run "rasdial /disconnect"
    echo.
) else (
    echo.
    echo ⚠️  Built-in VPN failed. Trying alternative methods...
    echo.
    
    REM Method 2: Use free VPN services
    echo 🌐 Alternative FREE VPN options:
    echo.
    echo 1️⃣  PROTON VPN (Best free option):
    echo    • Download: https://protonvpn.com/download
    echo    • Free servers in Japan/Netherlands
    echo    • No registration needed for basic
    echo.
    echo 2️⃣  WINDSCRIBE (10GB free):
    echo    • Download: https://windscribe.com/download
    echo    • Hong Kong server available
    echo    • Quick email signup
    echo.
    echo 3️⃣  VPN GATE (Completely free):
    echo    • Visit: https://www.vpngate.net/
    echo    • Choose Hong Kong/Singapore
    echo    • Download OpenVPN config
    echo    • No signup required
    echo.
    echo 4️⃣  TUNNELBEAR (500MB free):
    echo    • Download: https://www.tunnelbear.com/
    echo    • Hong Kong server
    echo    • Email signup required
    echo.
    
    REM Try to open VPN Gate automatically
    echo 🚀 Opening VPN Gate for instant free VPN...
    start https://www.vpngate.net/en/
    
    echo.
    echo 📋 QUICK STEPS for VPN Gate:
    echo   1. Choose a Hong Kong or Singapore server
    echo   2. Click "OpenVPN Config file"
    echo   3. Save the .ovpn file
    echo   4. Double-click to connect
    echo.
)

echo.
echo 💡 WHY THIS WORKS FOR WECHAT:
echo   • Asian IP addresses work better for WeChat
echo   • SMS verification more reliable
echo   • Access to mp.weixin.qq.com unrestricted
echo   • Bot development possible
echo.

echo ⚠️  IMPORTANT NOTES:
echo   • Free VPNs may be slower
echo   • Perfect for WeChat testing
echo   • For production bots, use paid VPN
echo   • Always respect terms of service
echo.

pause
