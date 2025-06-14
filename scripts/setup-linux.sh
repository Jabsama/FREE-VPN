#!/bin/bash

echo "========================================"
echo "China VPN Setup for Linux/macOS"
echo "========================================"
echo

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "ERROR: This script must be run as root (use sudo)"
    echo "Usage: sudo ./setup-linux.sh"
    exit 1
fi

echo "Running as root - OK"
echo

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
    echo "Detected: Linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
    echo "Detected: macOS"
else
    echo "Unsupported OS: $OSTYPE"
    exit 1
fi

echo
echo "Installing OpenVPN..."

# Install OpenVPN based on OS
if [ "$OS" == "linux" ]; then
    # Detect Linux distribution
    if [ -f /etc/debian_version ]; then
        # Debian/Ubuntu
        apt-get update
        apt-get install -y openvpn resolvconf
    elif [ -f /etc/redhat-release ]; then
        # RedHat/CentOS/Fedora
        if command -v dnf &> /dev/null; then
            dnf install -y openvpn
        else
            yum install -y openvpn
        fi
    elif [ -f /etc/arch-release ]; then
        # Arch Linux
        pacman -S --noconfirm openvpn
    else
        echo "Unsupported Linux distribution"
        echo "Please install OpenVPN manually"
        exit 1
    fi
elif [ "$OS" == "macos" ]; then
    # Check if Homebrew is installed
    if ! command -v brew &> /dev/null; then
        echo "Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    
    echo "Installing OpenVPN via Homebrew..."
    brew install openvpn
fi

echo
echo "Setting up VPN configuration..."

# Create OpenVPN config directory
mkdir -p /etc/openvpn/client

# Copy configuration file
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cp "$SCRIPT_DIR/../configs/china-vpn.ovpn" /etc/openvpn/client/

echo
echo "Creating systemd service (Linux only)..."

if [ "$OS" == "linux" ]; then
    # Create systemd service file
    cat > /etc/systemd/system/china-vpn.service << EOF
[Unit]
Description=China VPN OpenVPN Client
After=network.target

[Service]
Type=notify
PrivateTmp=true
WorkingDirectory=/etc/openvpn/client
ExecStart=/usr/sbin/openvpn --suppress-timestamps --nobind --config china-vpn.ovpn
CapabilityBoundingSet=CAP_IPC_LOCK CAP_NET_ADMIN CAP_NET_RAW CAP_SETGID CAP_SETUID CAP_SYS_CHROOT CAP_DAC_OVERRIDE
LimitNPROC=10
DeviceAllow=/dev/null rw
DeviceAllow=/dev/net/tun rw
ProtectSystem=true
ProtectHome=true
KillMode=process
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
EOF

    # Reload systemd and enable service
    systemctl daemon-reload
    systemctl enable china-vpn.service
    
    echo "Systemd service created and enabled"
fi

echo
echo "Creating connection scripts..."

# Create connection script
cat > /usr/local/bin/china-vpn-connect << 'EOF'
#!/bin/bash

echo "Connecting to China VPN..."

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux - use systemd service
    if systemctl is-active --quiet china-vpn.service; then
        echo "VPN is already connected"
    else
        systemctl start china-vpn.service
        echo "VPN connection started"
        echo "Check status with: systemctl status china-vpn.service"
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS - direct OpenVPN call
    if pgrep -f "openvpn.*china-vpn" > /dev/null; then
        echo "VPN is already connected"
    else
        echo "Starting VPN connection..."
        sudo openvpn --config /etc/openvpn/client/china-vpn.ovpn --daemon
        echo "VPN connection started in background"
    fi
fi
EOF

# Create disconnection script
cat > /usr/local/bin/china-vpn-disconnect << 'EOF'
#!/bin/bash

echo "Disconnecting China VPN..."

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux - use systemd service
    if systemctl is-active --quiet china-vpn.service; then
        systemctl stop china-vpn.service
        echo "VPN disconnected"
    else
        echo "VPN is not connected"
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS - kill OpenVPN process
    if pgrep -f "openvpn.*china-vpn" > /dev/null; then
        sudo pkill -f "openvpn.*china-vpn"
        echo "VPN disconnected"
    else
        echo "VPN is not connected"
    fi
fi
EOF

# Create status script
cat > /usr/local/bin/china-vpn-status << 'EOF'
#!/bin/bash

echo "China VPN Status:"
echo "=================="

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux - check systemd service
    if systemctl is-active --quiet china-vpn.service; then
        echo "Status: CONNECTED"
        echo "Service: Active"
        systemctl status china-vpn.service --no-pager -l
    else
        echo "Status: DISCONNECTED"
        echo "Service: Inactive"
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS - check process
    if pgrep -f "openvpn.*china-vpn" > /dev/null; then
        echo "Status: CONNECTED"
        echo "Process: Running"
    else
        echo "Status: DISCONNECTED"
        echo "Process: Not running"
    fi
fi

echo
echo "Network Information:"
echo "==================="
echo "Current IP: $(curl -s ifconfig.me 2>/dev/null || echo 'Unable to detect')"
echo "DNS Servers: $(cat /etc/resolv.conf | grep nameserver | awk '{print $2}' | tr '\n' ' ')"
EOF

# Make scripts executable
chmod +x /usr/local/bin/china-vpn-connect
chmod +x /usr/local/bin/china-vpn-disconnect
chmod +x /usr/local/bin/china-vpn-status

echo
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo
echo "Available commands:"
echo "  china-vpn-connect    - Connect to VPN"
echo "  china-vpn-disconnect - Disconnect from VPN"
echo "  china-vpn-status     - Check VPN status"
echo
echo "Next steps:"
echo "1. Update the server address in /etc/openvpn/client/china-vpn.ovpn"
echo "2. Add your certificates and keys to the config file"
echo "3. Run 'china-vpn-connect' to connect"
echo
echo "For WeChat access:"
echo "- Connect to VPN first using 'china-vpn-connect'"
echo "- Open https://mp.weixin.qq.com/"
echo "- Your IP will appear as Chinese location"
echo
