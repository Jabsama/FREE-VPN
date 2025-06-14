@echo off
echo ========================================
echo China VPN Setup for Windows
echo ========================================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Running as Administrator - OK
) else (
    echo ERROR: This script must be run as Administrator
    echo Right-click and select "Run as administrator"
    pause
    exit /b 1
)

echo.
echo Installing OpenVPN...

REM Check if OpenVPN is already installed
if exist "C:\Program Files\OpenVPN\bin\openvpn.exe" (
    echo OpenVPN is already installed
) else (
    echo Downloading OpenVPN installer...
    powershell -Command "Invoke-WebRequest -Uri 'https://swupdate.openvpn.org/community/releases/OpenVPN-2.6.8-I001-amd64.msi' -OutFile 'OpenVPN-installer.msi'"
    
    echo Installing OpenVPN...
    msiexec /i OpenVPN-installer.msi /quiet /norestart
    
    echo Cleaning up installer...
    del OpenVPN-installer.msi
)

echo.
echo Setting up VPN configuration...

REM Create OpenVPN config directory if it doesn't exist
if not exist "C:\Program Files\OpenVPN\config" (
    mkdir "C:\Program Files\OpenVPN\config"
)

REM Copy configuration file
copy "%~dp0..\configs\china-vpn.ovpn" "C:\Program Files\OpenVPN\config\"

echo.
echo Creating desktop shortcut...
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\China VPN.lnk'); $Shortcut.TargetPath = 'C:\Program Files\OpenVPN\bin\openvpn-gui.exe'; $Shortcut.Arguments = '--config china-vpn.ovpn'; $Shortcut.WorkingDirectory = 'C:\Program Files\OpenVPN\config'; $Shortcut.Save()"

echo.
echo Setting up Windows Firewall rules...
netsh advfirewall firewall add rule name="OpenVPN" dir=in action=allow program="C:\Program Files\OpenVPN\bin\openvpn.exe" enable=yes
netsh advfirewall firewall add rule name="OpenVPN GUI" dir=in action=allow program="C:\Program Files\OpenVPN\bin\openvpn-gui.exe" enable=yes

echo.
echo Creating connection script...
echo @echo off > "%USERPROFILE%\Desktop\Connect China VPN.bat"
echo echo Connecting to China VPN... >> "%USERPROFILE%\Desktop\Connect China VPN.bat"
echo "C:\Program Files\OpenVPN\bin\openvpn.exe" --config "C:\Program Files\OpenVPN\config\china-vpn.ovpn" >> "%USERPROFILE%\Desktop\Connect China VPN.bat"

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Update the server address in china-vpn.ovpn
echo 2. Add your certificates and keys to the config file
echo 3. Use "Connect China VPN.bat" on your desktop to connect
echo 4. Or use the OpenVPN GUI from the system tray
echo.
echo For WeChat access:
echo - Connect to VPN first
echo - Open https://mp.weixin.qq.com/
echo - Your IP will appear as Chinese location
echo.
pause
