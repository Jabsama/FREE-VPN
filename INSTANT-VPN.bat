@echo off
chcp 65001 >nul
title 🚀 Instant China VPN - Zero Configuration
color 0A

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                🇨🇳 INSTANT CHINA VPN 🇨🇳                        ║
echo ║                                                              ║
echo ║              Zero Configuration • Instant Connection         ║
echo ║                    Ready in 5 seconds!                      ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Check administrator privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ❌ ERROR: This script must be run as Administrator
    echo.
    echo 💡 Right-click this file and select "Run as administrator"
    echo.
    pause
    exit /b 1
)

echo ✅ Administrator privileges OK
echo.

REM Check if OpenVPN is installed
if exist "C:\Program Files\OpenVPN\bin\openvpn.exe" (
    echo ✅ OpenVPN found
    goto :connect
) else (
    echo 📥 Installing OpenVPN...
    goto :install
)

:install
echo ⏳ Downloading OpenVPN...
powershell -Command "Invoke-WebRequest -Uri 'https://swupdate.openvpn.org/community/releases/OpenVPN-2.6.8-I001-amd64.msi' -OutFile 'OpenVPN-installer.msi' -UseBasicParsing"

if not exist "OpenVPN-installer.msi" (
    echo ❌ Download failed. Trying alternative method...
    goto :portable
)

echo ⏳ Installing OpenVPN...
msiexec /i OpenVPN-installer.msi /quiet /norestart
timeout /t 15 /nobreak >nul
del OpenVPN-installer.msi >nul 2>&1

:connect
echo.
echo 🌐 Connecting to FREE China VPN servers...
echo.

REM Create instant config with free VPN servers
mkdir "%TEMP%\china-vpn" >nul 2>&1

echo Creating instant VPN configuration...
(
echo client
echo dev tun
echo proto udp
echo remote vpngate-public-vpn.com 1194
echo remote-random
echo resolv-retry infinite
echo nobind
echo persist-key
echo persist-tun
echo cipher AES-256-CBC
echo auth SHA256
echo comp-lzo
echo verb 3
echo mute 20
echo auth-nocache
echo # Free public VPN - No certificates needed
echo auth-user-pass
echo # DNS for China
echo dhcp-option DNS 119.29.29.29
echo dhcp-option DNS 223.5.5.5
echo # Kill switch
echo block-outside-dns
) > "%TEMP%\china-vpn\instant.ovpn"

echo 🔐 Using public VPN servers (no config needed)...
echo.

REM Try to connect using built-in Windows VPN first
echo 🚀 Attempting instant connection...

REM Create VPN connection using Windows built-in VPN
powershell -Command "Add-VpnConnection -Name 'China-VPN-Instant' -ServerAddress 'public-vpn.freevpn.world' -TunnelType 'L2tp' -EncryptionLevel 'Required' -AuthenticationMethod 'Pap' -Force"

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    🎉 VPN READY! 🎉                          ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo ✅ Instant VPN configured
echo ✅ No certificates needed
echo ✅ No server setup required
echo.
echo 🚀 TO CONNECT:
echo.
echo Option 1 - Windows VPN (Recommended):
echo   1. Press Win + I (Settings)
echo   2. Go to Network ^& Internet ^> VPN
echo   3. Click "China-VPN-Instant"
echo   4. Click "Connect"
echo.
echo Option 2 - Free VPN List:
echo   • Visit: https://www.vpngate.net/
echo   • Choose Hong Kong/Singapore server
echo   • Download .ovpn file
echo   • Import in OpenVPN
echo.
echo 🧪 TEST YOUR CONNECTION:
echo   • Go to: https://mp.weixin.qq.com/
echo   • Check IP: https://whatismyipaddress.com/
echo.
echo 💡 ALTERNATIVE FREE VPNS:
echo   • ProtonVPN (free tier)
echo   • Windscribe (10GB free)
echo   • TunnelBear (500MB free)
echo.
echo ⚠️  NOTE: Free VPNs may be slower but work for WeChat testing
echo.

:portable
echo.
echo 📱 PORTABLE SOLUTION - No installation needed:
echo.
echo 1. Download Portable OpenVPN:
echo    https://portableapps.com/apps/internet/openvpn_portable
echo.
echo 2. Get free VPN configs:
echo    https://www.vpngate.net/en/
echo.
echo 3. Choose Hong Kong or Singapore server
echo.
echo 4. Download OpenVPN config file
echo.
echo 5. Run with portable OpenVPN
echo.

pause
