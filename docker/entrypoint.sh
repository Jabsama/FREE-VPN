#!/bin/bash

# =============================================================================
# VPN Server Docker Entrypoint Script
# Handles initialization, certificate generation, and service startup
# =============================================================================

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Logging function
log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}" >&2
}

success() {
    echo -e "${GREEN}[SUCCESS] $1${NC}"
}

warning() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

# Environment variables with defaults
VPN_SERVER_NAME=${VPN_SERVER_NAME:-"secure-vpn.local"}
VPN_SERVER_IP=${VPN_SERVER_IP:-"10.8.0.1"}
VPN_CLIENT_NETWORK=${VPN_CLIENT_NETWORK:-"10.8.0.0"}
VPN_CLIENT_NETMASK=${VPN_CLIENT_NETMASK:-"255.255.255.0"}
VPN_DNS1=${VPN_DNS1:-"8.8.8.8"}
VPN_DNS2=${VPN_DNS2:-"8.8.4.4"}
WEB_ADMIN_USER=${WEB_ADMIN_USER:-"admin"}
WEB_ADMIN_PASS=${WEB_ADMIN_PASS:-"SecureVPN2025!"}
MONITORING_ENABLED=${MONITORING_ENABLED:-"true"}
LOG_LEVEL=${LOG_LEVEL:-"INFO"}

# Directories
CERT_DIR="/opt/vpn-manager/certificates"
SECURE_DIR="/opt/vpn-manager/secure-storage"
CONFIG_DIR="/etc/openvpn/server"
LOG_DIR="/var/log/openvpn"

# Initialize directories
init_directories() {
    log "Initializing directories..."
    
    mkdir -p "$CERT_DIR" "$SECURE_DIR" "$CONFIG_DIR" "$LOG_DIR"
    
    # Set proper permissions
    chmod 700 "$SECURE_DIR"
    chmod 755 "$CERT_DIR" "$CONFIG_DIR" "$LOG_DIR"
    
    success "Directories initialized"
}

# Generate certificates if they don't exist
init_certificates() {
    log "Checking certificates..."
    
    if [[ ! -f "$CERT_DIR/ca.crt" ]]; then
        warning "Certificates not found, generating new ones..."
        
        cd /opt/vpn-manager
        ./secure-certificate-manager.sh create-all "$VPN_SERVER_NAME" "" "client"
        
        success "Certificates generated successfully"
    else
        log "Certificates already exist, skipping generation"
    fi
}

# Configure OpenVPN server
configure_openvpn() {
    log "Configuring OpenVPN server..."
    
    # Create server configuration
    cat > "$CONFIG_DIR/server.conf" << EOF
# OpenVPN Server Configuration - Docker Edition
# Generated on $(date)

# Network settings
port 1194
proto udp
dev tun

# SSL/TLS root certificate (ca), certificate (cert), and private key (key)
ca $CERT_DIR/ca.crt
cert $CERT_DIR/server.crt
key $CERT_DIR/server.key.enc
dh $CERT_DIR/dh4096.pem

# Network topology
topology subnet
server $VPN_CLIENT_NETWORK $VPN_CLIENT_NETMASK

# Maintain a record of client <-> virtual IP address associations
ifconfig-pool-persist /var/lib/openvpn/ipp.txt

# Push routes to the client
push "redirect-gateway def1 bypass-dhcp"
push "dhcp-option DNS $VPN_DNS1"
push "dhcp-option DNS $VPN_DNS2"

# Client-to-client communication
client-to-client

# Keep alive
keepalive 10 120

# Cryptographic cipher
cipher AES-256-GCM
auth SHA256

# Enable compression
compress lz4-v2
push "compress lz4-v2"

# Maximum number of concurrently connected clients
max-clients 100

# Run with reduced privileges
user vpnuser
group vpnuser

# Persist certain options
persist-key
persist-tun

# Output a short status file
status /var/log/openvpn/openvpn-status.log

# Log settings
log-append /var/log/openvpn/openvpn.log
verb 3
mute 20

# TLS security
tls-auth $CERT_DIR/ta.key 0
tls-version-min 1.2
tls-cipher TLS-ECDHE-RSA-WITH-AES-256-GCM-SHA384

# Additional security
remote-cert-tls client
EOF

    success "OpenVPN server configured"
}

# Setup iptables rules
setup_iptables() {
    log "Setting up iptables rules..."
    
    # Enable IP forwarding
    echo 1 > /proc/sys/net/ipv4/ip_forward
    
    # NAT rules for VPN traffic
    iptables -t nat -A POSTROUTING -s $VPN_CLIENT_NETWORK/$VPN_CLIENT_NETMASK -o eth0 -j MASQUERADE
    iptables -A INPUT -i tun+ -j ACCEPT
    iptables -A FORWARD -i tun+ -j ACCEPT
    iptables -A FORWARD -i tun+ -o eth0 -m state --state RELATED,ESTABLISHED -j ACCEPT
    iptables -A FORWARD -i eth0 -o tun+ -m state --state RELATED,ESTABLISHED -j ACCEPT
    
    # Allow VPN port
    iptables -A INPUT -p udp --dport 1194 -j ACCEPT
    
    # Allow web interface ports
    iptables -A INPUT -p tcp --dport 8080 -j ACCEPT
    iptables -A INPUT -p tcp --dport 8443 -j ACCEPT
    
    success "iptables rules configured"
}

# Create web interface configuration
setup_web_interface() {
    log "Setting up web interface..."
    
    # Create web admin credentials
    echo "$WEB_ADMIN_USER:$(openssl passwd -apr1 $WEB_ADMIN_PASS)" > /opt/monitoring/.htpasswd
    
    # Create web interface config
    cat > /opt/monitoring/config.py << EOF
# Web Interface Configuration
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '$(openssl rand -hex 32)'
    VPN_SERVER_NAME = '$VPN_SERVER_NAME'
    VPN_SERVER_IP = '$VPN_SERVER_IP'
    VPN_CLIENT_NETWORK = '$VPN_CLIENT_NETWORK'
    VPN_CLIENT_NETMASK = '$VPN_CLIENT_NETMASK'
    MONITORING_ENABLED = $MONITORING_ENABLED
    LOG_LEVEL = '$LOG_LEVEL'
    CERT_DIR = '$CERT_DIR'
    LOG_DIR = '$LOG_DIR'
    ADMIN_USER = '$WEB_ADMIN_USER'
    ADMIN_PASS = '$WEB_ADMIN_PASS'
EOF

    success "Web interface configured"
}

# Create monitoring dashboard
create_monitoring_dashboard() {
    log "Creating monitoring dashboard..."
    
    cat > /opt/monitoring/monitor.py << 'EOF'
#!/usr/bin/env python3
"""
VPN Monitoring Dashboard
Real-time monitoring of VPN server and connected clients
"""

from flask import Flask, render_template, jsonify, request
import psutil
import subprocess
import json
import os
import re
from datetime import datetime, timedelta
import sqlite3

app = Flask(__name__)

class VPNMonitor:
    def __init__(self):
        self.log_file = '/var/log/openvpn/openvpn.log'
        self.status_file = '/var/log/openvpn/openvpn-status.log'
        self.db_file = '/opt/monitoring/data/vpn_stats.db'
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database for storing statistics"""
        os.makedirs(os.path.dirname(self.db_file), exist_ok=True)
        
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS connection_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                client_ip TEXT,
                virtual_ip TEXT,
                action TEXT,
                bytes_received INTEGER DEFAULT 0,
                bytes_sent INTEGER DEFAULT 0
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS server_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                cpu_usage REAL,
                memory_usage REAL,
                disk_usage REAL,
                network_in INTEGER,
                network_out INTEGER,
                active_connections INTEGER
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_server_stats(self):
        """Get server system statistics"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            network = psutil.net_io_counters()
            
            return {
                'cpu_usage': cpu_percent,
                'memory_usage': memory.percent,
                'memory_total': memory.total,
                'memory_used': memory.used,
                'disk_usage': disk.percent,
                'disk_total': disk.total,
                'disk_used': disk.used,
                'network_bytes_sent': network.bytes_sent,
                'network_bytes_recv': network.bytes_recv,
                'uptime': self.get_uptime()
            }
        except Exception as e:
            return {'error': str(e)}
    
    def get_uptime(self):
        """Get system uptime"""
        try:
            with open('/proc/uptime', 'r') as f:
                uptime_seconds = float(f.readline().split()[0])
                return str(timedelta(seconds=int(uptime_seconds)))
        except:
            return "Unknown"
    
    def get_connected_clients(self):
        """Parse OpenVPN status file to get connected clients"""
        clients = []
        
        try:
            if os.path.exists(self.status_file):
                with open(self.status_file, 'r') as f:
                    content = f.read()
                    
                # Parse client list
                client_section = False
                for line in content.split('\n'):
                    if line.startswith('Common Name,Real Address,Bytes Received,Bytes Sent,Connected Since'):
                        client_section = True
                        continue
                    elif line.startswith('ROUTING TABLE'):
                        client_section = False
                        continue
                    
                    if client_section and line.strip():
                        parts = line.split(',')
                        if len(parts) >= 5:
                            clients.append({
                                'name': parts[0],
                                'real_address': parts[1],
                                'bytes_received': int(parts[2]) if parts[2].isdigit() else 0,
                                'bytes_sent': int(parts[3]) if parts[3].isdigit() else 0,
                                'connected_since': parts[4],
                                'duration': self.calculate_duration(parts[4])
                            })
        except Exception as e:
            print(f"Error parsing status file: {e}")
        
        return clients
    
    def calculate_duration(self, connected_since):
        """Calculate connection duration"""
        try:
            connect_time = datetime.strptime(connected_since, '%a %b %d %H:%M:%S %Y')
            duration = datetime.now() - connect_time
            return str(duration).split('.')[0]  # Remove microseconds
        except:
            return "Unknown"
    
    def get_recent_logs(self, lines=50):
        """Get recent log entries"""
        logs = []
        
        try:
            if os.path.exists(self.log_file):
                result = subprocess.run(['tail', '-n', str(lines), self.log_file], 
                                      capture_output=True, text=True)
                
                for line in result.stdout.split('\n'):
                    if line.strip():
                        logs.append({
                            'timestamp': self.extract_timestamp(line),
                            'message': line.strip(),
                            'level': self.extract_log_level(line)
                        })
        except Exception as e:
            logs.append({'timestamp': datetime.now().isoformat(), 
                        'message': f'Error reading logs: {e}', 'level': 'ERROR'})
        
        return logs
    
    def extract_timestamp(self, log_line):
        """Extract timestamp from log line"""
        # Try to extract timestamp from OpenVPN log format
        match = re.search(r'(\w{3} \w{3} \d{1,2} \d{2}:\d{2}:\d{2} \d{4})', log_line)
        if match:
            return match.group(1)
        return datetime.now().strftime('%a %b %d %H:%M:%S %Y')
    
    def extract_log_level(self, log_line):
        """Extract log level from log line"""
        if 'ERROR' in log_line.upper():
            return 'ERROR'
        elif 'WARNING' in log_line.upper() or 'WARN' in log_line.upper():
            return 'WARNING'
        elif 'INFO' in log_line.upper():
            return 'INFO'
        else:
            return 'DEBUG'
    
    def save_stats(self):
        """Save current statistics to database"""
        stats = self.get_server_stats()
        clients = self.get_connected_clients()
        
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO server_stats 
            (cpu_usage, memory_usage, disk_usage, network_in, network_out, active_connections)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            stats.get('cpu_usage', 0),
            stats.get('memory_usage', 0),
            stats.get('disk_usage', 0),
            stats.get('network_bytes_recv', 0),
            stats.get('network_bytes_sent', 0),
            len(clients)
        ))
        
        conn.commit()
        conn.close()

# Initialize monitor
monitor = VPNMonitor()

@app.route('/')
def dashboard():
    """Main dashboard"""
    return render_template('dashboard.html')

@app.route('/api/stats')
def api_stats():
    """API endpoint for server statistics"""
    stats = monitor.get_server_stats()
    clients = monitor.get_connected_clients()
    
    return jsonify({
        'server': stats,
        'clients': clients,
        'client_count': len(clients),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/logs')
def api_logs():
    """API endpoint for recent logs"""
    lines = request.args.get('lines', 50, type=int)
    logs = monitor.get_recent_logs(lines)
    
    return jsonify({
        'logs': logs,
        'count': len(logs),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/clients')
def api_clients():
    """API endpoint for connected clients"""
    clients = monitor.get_connected_clients()
    
    return jsonify({
        'clients': clients,
        'count': len(clients),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'vpn-monitor'
    })

if __name__ == '__main__':
    # Save initial stats
    monitor.save_stats()
    
    # Start Flask app
    app.run(host='0.0.0.0', port=3000, debug=False)
EOF

    chmod +x /opt/monitoring/monitor.py
    success "Monitoring dashboard created"
}

# Create supervisor configuration
create_supervisor_config() {
    log "Creating supervisor configuration..."
    
    cat > /etc/supervisor/conf.d/supervisord.conf << EOF
[supervisord]
nodaemon=true
user=root
logfile=/var/log/supervisor/supervisord.log
pidfile=/var/run/supervisord.pid

[program:openvpn]
command=/usr/local/sbin/openvpn --config /etc/openvpn/server/server.conf
user=root
autostart=true
autorestart=true
stderr_logfile=/var/log/supervisor/openvpn.err.log
stdout_logfile=/var/log/supervisor/openvpn.out.log
priority=100

[program:monitoring]
command=python3 /opt/monitoring/monitor.py
user=vpnuser
autostart=true
autorestart=true
stderr_logfile=/var/log/supervisor/monitoring.err.log
stdout_logfile=/var/log/supervisor/monitoring.out.log
priority=200

[program:nginx]
command=/usr/sbin/nginx -g "daemon off;"
user=root
autostart=true
autorestart=true
stderr_logfile=/var/log/supervisor/nginx.err.log
stdout_logfile=/var/log/supervisor/nginx.out.log
priority=300
EOF

    success "Supervisor configuration created"
}

# Main initialization
main() {
    log "Starting VPN Server initialization..."
    
    # Initialize components
    init_directories
    init_certificates
    configure_openvpn
    setup_iptables
    setup_web_interface
    create_monitoring_dashboard
    create_supervisor_config
    
    success "VPN Server initialization completed!"
    
    # Start services
    log "Starting services..."
    exec "$@"
}

# Run main function with all arguments
main "$@"
EOF
