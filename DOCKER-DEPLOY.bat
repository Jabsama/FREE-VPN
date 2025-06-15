@echo off
REM =============================================================================
REM VPN Server - Docker Deployment Script (Windows)
REM One-click deployment with Docker Compose
REM =============================================================================

title VPN Server - Docker Deployment

echo.
echo ========================================
echo    🐳 VPN Server Docker Deployment
echo ========================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not installed or not in PATH
    echo Please install Docker Desktop from: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

REM Check if Docker Compose is available
docker compose version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose is not available
    echo Please update Docker Desktop to the latest version
    pause
    exit /b 1
)

echo ✅ Docker is installed and ready
echo.

REM Create necessary directories
echo 📁 Creating directories...
if not exist "docker\custom-configs" mkdir "docker\custom-configs"
if not exist "docker\nginx\ssl" mkdir "docker\nginx\ssl"
if not exist "logs" mkdir "logs"

REM Generate SSL certificates for nginx
echo 🔐 Generating SSL certificates...
openssl req -x509 -nodes -days 365 -newkey rsa:2048 ^
    -keyout docker\nginx\ssl\nginx.key ^
    -out docker\nginx\ssl\nginx.crt ^
    -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost" >nul 2>&1

if %errorlevel% neq 0 (
    echo ⚠️  OpenSSL not found, using HTTP only
) else (
    echo ✅ SSL certificates generated
)

echo.
echo 🚀 Starting VPN Server deployment...
echo.
echo This will:
echo   • Build and start all containers
echo   • Generate VPN certificates automatically
echo   • Set up monitoring dashboard
echo   • Configure database and Redis
echo   • Start web interfaces
echo.

set /p confirm="Continue? (Y/N): "
if /i not "%confirm%"=="Y" (
    echo Deployment cancelled.
    pause
    exit /b 0
)

echo.
echo 🔨 Building and starting containers...
docker compose up -d --build

if %errorlevel% neq 0 (
    echo ❌ Deployment failed!
    echo Check the logs with: docker compose logs
    pause
    exit /b 1
)

echo.
echo ✅ VPN Server deployed successfully!
echo.
echo 📊 Access Points:
echo   • VPN Server:        Port 1194 (UDP)
echo   • Web Interface:     http://localhost:8080
echo   • HTTPS Interface:   https://localhost:8443
echo   • Monitoring:        http://localhost:3000
echo   • Nginx Proxy:       http://localhost:80
echo.
echo 🔧 Management Commands:
echo   • View logs:         docker compose logs -f
echo   • Stop services:     docker compose down
echo   • Restart:           docker compose restart
echo   • Update:            docker compose pull && docker compose up -d
echo.
echo 📋 Default Credentials:
echo   • Admin User:        admin
echo   • Admin Password:    SecureVPN2025!
echo.

REM Wait for services to be ready
echo ⏳ Waiting for services to start...
timeout /t 10 /nobreak >nul

REM Check service health
echo 🔍 Checking service health...
docker compose ps

echo.
echo 🎉 Deployment complete! 
echo.
echo 💡 Next steps:
echo   1. Configure your VPN clients with generated certificates
echo   2. Access the monitoring dashboard to view statistics
echo   3. Customize settings in the web interface
echo.

set /p open="Open monitoring dashboard? (Y/N): "
if /i "%open%"=="Y" (
    start http://localhost:3000
)

pause
