@echo off
chcp 65001 >nul
title 🚀 China VPN - Quick Launch
color 0A

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    🇨🇳 CHINA VPN LAUNCHER 🇨🇳                    ║
echo ║                                                              ║
echo ║           Free VPN Solution for WeChat & Bots               ║
echo ║                     Ready in 2 seconds!                     ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Check administrator privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ❌ ERROR: This script must be run as Administrator
    echo.
    echo 💡 SOLUTION:
    echo    1. Right-click on this file
    echo    2. Select "Run as administrator"
    echo.
    pause
    exit /b 1
)

echo ✅ Administrator privileges detected
echo.

REM Check if OpenVPN is installed
if exist "C:\Program Files\OpenVPN\bin\openvpn.exe" (
    echo ✅ OpenVPN already installed
    goto :configure
) else (
    echo 📥 Installing OpenVPN...
    goto :install
)

:install
echo.
echo ⏳ Downloading OpenVPN...
powershell -Command "try { Invoke-WebRequest -Uri 'https://swupdate.openvpn.org/community/releases/OpenVPN-2.6.8-I001-amd64.msi' -OutFile 'OpenVPN-installer.msi' -UseBasicParsing } catch { Write-Host 'Download error' }"

if not exist "OpenVPN-installer.msi" (
    echo ❌ Download failed. Check your internet connection.
    pause
    exit /b 1
)

echo ⏳ Installing OpenVPN...
msiexec /i OpenVPN-installer.msi /quiet /norestart
timeout /t 10 /nobreak >nul

echo 🧹 Cleaning up...
del OpenVPN-installer.msi >nul 2>&1

:configure
echo.
echo ⚙️  Configuring VPN...

REM Create configuration directory
if not exist "C:\Program Files\OpenVPN\config" (
    mkdir "C:\Program Files\OpenVPN\config"
)

REM Copy configuration
copy "%~dp0configs\china-vpn.ovpn" "C:\Program Files\OpenVPN\config\" >nul

REM Create desktop shortcut
echo 🖥️  Creating shortcuts...
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\🇨🇳 China VPN.lnk'); $Shortcut.TargetPath = 'C:\Program Files\OpenVPN\bin\openvpn-gui.exe'; $Shortcut.Arguments = '--config china-vpn.ovpn'; $Shortcut.WorkingDirectory = 'C:\Program Files\OpenVPN\config'; $Shortcut.IconLocation = 'C:\Program Files\OpenVPN\bin\openvpn-gui.exe,0'; $Shortcut.Save()"

REM Create quick connection script
echo @echo off > "%USERPROFILE%\Desktop\🚀 Connect China VPN.bat"
echo title China VPN Connection >> "%USERPROFILE%\Desktop\🚀 Connect China VPN.bat"
echo echo Connecting to China VPN... >> "%USERPROFILE%\Desktop\🚀 Connect China VPN.bat"
echo "C:\Program Files\OpenVPN\bin\openvpn.exe" --config "C:\Program Files\OpenVPN\config\china-vpn.ovpn" >> "%USERPROFILE%\Desktop\🚀 Connect China VPN.bat"

REM Configure Windows Firewall
echo 🔥 Configuring firewall...
netsh advfirewall firewall add rule name="China VPN OpenVPN" dir=in action=allow program="C:\Program Files\OpenVPN\bin\openvpn.exe" enable=yes >nul 2>&1
netsh advfirewall firewall add rule name="China VPN GUI" dir=in action=allow program="C:\Program Files\OpenVPN\bin\openvpn-gui.exe" enable=yes >nul 2>&1

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    🎉 INSTALLATION COMPLETE! 🎉                ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo ✅ OpenVPN installed and configured
echo ✅ Desktop shortcuts created
echo ✅ Firewall configured
echo.
echo 📋 NEXT STEPS:
echo.
echo 1️⃣  CONFIGURE YOUR SERVER:
echo    • Open: configs\china-vpn.ovpn
echo    • Replace: china-vpn-server.example.com
echo    • With your server IP or domain name
echo.
echo 2️⃣  ADD YOUR CERTIFICATES:
echo    • Replace test certificates
echo    • With your real VPN certificates
echo.
echo 3️⃣  LAUNCH VPN:
echo    • Double-click "🇨🇳 China VPN" (desktop)
echo    • Or "🚀 Connect China VPN" (desktop)
echo.
echo 4️⃣  TEST WECHAT:
echo    • Go to: https://mp.weixin.qq.com/
echo    • Verify unrestricted access
echo.
echo 💡 HELP: Check README.md for more info
echo.
echo ⚠️  IMPORTANT: 
echo    This VPN is for legitimate use only.
echo    Respect local laws and service terms.
echo.
pause
