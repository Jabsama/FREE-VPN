#!/bin/bash

# =============================================================================
# VPN Server - Docker Deployment Script (Linux/macOS)
# One-click deployment with Docker Compose
# =============================================================================

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Logging functions
log() {
    echo -e "${BLUE}[$(date '+%H:%M:%S')] $1${NC}"
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}" >&2
}

# Banner
echo -e "${BLUE}"
echo "========================================"
echo "   🐳 VPN Server Docker Deployment"
echo "========================================"
echo -e "${NC}"

# Check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        error "Docker is not installed"
        echo "Please install Docker from: https://docs.docker.com/get-docker/"
        exit 1
    fi
    
    # Check Docker Compose
    if ! docker compose version &> /dev/null; then
        error "Docker Compose is not available"
        echo "Please update Docker to the latest version"
        exit 1
    fi
    
    # Check if running as root for privileged operations
    if [[ $EUID -eq 0 ]]; then
        warning "Running as root - this is not recommended for production"
    fi
    
    success "Prerequisites check passed"
}

# Create directories
create_directories() {
    log "Creating necessary directories..."
    
    mkdir -p docker/custom-configs
    mkdir -p docker/nginx/ssl
    mkdir -p logs
    
    success "Directories created"
}

# Generate SSL certificates
generate_ssl_certificates() {
    log "Generating SSL certificates..."
    
    if command -v openssl &> /dev/null; then
        openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
            -keyout docker/nginx/ssl/nginx.key \
            -out docker/nginx/ssl/nginx.crt \
            -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost" \
            2>/dev/null
        
        success "SSL certificates generated"
    else
        warning "OpenSSL not found, using HTTP only"
    fi
}

# Deploy services
deploy_services() {
    log "Starting VPN Server deployment..."
    
    echo
    echo "This will:"
    echo "  • Build and start all containers"
    echo "  • Generate VPN certificates automatically"
    echo "  • Set up monitoring dashboard"
    echo "  • Configure database and Redis"
    echo "  • Start web interfaces"
    echo
    
    read -p "Continue? (y/N): " -n 1 -r
    echo
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Deployment cancelled."
        exit 0
    fi
    
    log "Building and starting containers..."
    
    if docker compose up -d --build; then
        success "Containers started successfully"
    else
        error "Deployment failed!"
        echo "Check the logs with: docker compose logs"
        exit 1
    fi
}

# Wait for services
wait_for_services() {
    log "Waiting for services to start..."
    sleep 10
    
    log "Checking service health..."
    docker compose ps
}

# Display results
display_results() {
    echo
    success "VPN Server deployed successfully!"
    echo
    echo -e "${BLUE}📊 Access Points:${NC}"
    echo "  • VPN Server:        Port 1194 (UDP)"
    echo "  • Web Interface:     http://localhost:8080"
    echo "  • HTTPS Interface:   https://localhost:8443"
    echo "  • Monitoring:        http://localhost:3000"
    echo "  • Nginx Proxy:       http://localhost:80"
    echo
    echo -e "${BLUE}🔧 Management Commands:${NC}"
    echo "  • View logs:         docker compose logs -f"
    echo "  • Stop services:     docker compose down"
    echo "  • Restart:           docker compose restart"
    echo "  • Update:            docker compose pull && docker compose up -d"
    echo
    echo -e "${BLUE}📋 Default Credentials:${NC}"
    echo "  • Admin User:        admin"
    echo "  • Admin Password:    SecureVPN2025!"
    echo
    echo -e "${GREEN}🎉 Deployment complete!${NC}"
    echo
    echo -e "${BLUE}💡 Next steps:${NC}"
    echo "  1. Configure your VPN clients with generated certificates"
    echo "  2. Access the monitoring dashboard to view statistics"
    echo "  3. Customize settings in the web interface"
    echo
    
    read -p "Open monitoring dashboard? (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if command -v xdg-open &> /dev/null; then
            xdg-open http://localhost:3000
        elif command -v open &> /dev/null; then
            open http://localhost:3000
        else
            echo "Please open http://localhost:3000 in your browser"
        fi
    fi
}

# Cleanup function
cleanup() {
    if [[ $? -ne 0 ]]; then
        error "Deployment failed!"
        echo
        echo "Troubleshooting:"
        echo "  • Check Docker is running: docker info"
        echo "  • View container logs: docker compose logs"
        echo "  • Check port availability: netstat -tulpn | grep :1194"
        echo "  • Restart deployment: docker compose down && docker compose up -d"
    fi
}

# Set trap for cleanup
trap cleanup EXIT

# Main execution
main() {
    check_prerequisites
    create_directories
    generate_ssl_certificates
    deploy_services
    wait_for_services
    display_results
}

# Run main function
main "$@"
