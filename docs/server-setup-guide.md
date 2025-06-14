# VPN Server Setup Guide

This guide explains how to set up your own OpenVPN server optimized for China access and WeChat services.

## 🎯 Overview

Setting up your own VPN server gives you full control over the connection, better performance, and enhanced privacy. This guide covers server setup on various cloud providers with China-optimized configurations.

## 🌐 Recommended Server Locations

For optimal WeChat and Chinese service access, choose servers in these locations:

### Tier 1 (Best Performance)
- **Hong Kong** - Closest to mainland China, excellent for WeChat
- **Singapore** - Good performance, reliable connectivity
- **Taiwan** - Close proximity, good for Chinese services

### Tier 2 (Good Performance)
- **Japan (Tokyo)** - Decent latency to China
- **South Korea (Seoul)** - Good regional connectivity
- **Malaysia** - Alternative Southeast Asia option

### Cloud Providers
- **DigitalOcean** - Simple setup, good performance
- **Vultr** - Multiple Asia locations
- **Linode** - Reliable infrastructure
- **AWS** - Enterprise-grade (more expensive)
- **Google Cloud** - Global network

## 🚀 Quick Server Setup

### Prerequisites
- VPS with Ubuntu 20.04+ or CentOS 8+
- Root access
- Public IP address
- At least 1GB RAM, 1 CPU core

### Step 1: Initial Server Setup

```bash
# Update system
apt update && apt upgrade -y

# Install required packages
apt install -y openvpn easy-rsa ufw curl wget

# Create OpenVPN directory
mkdir -p /etc/openvpn/server
cd /etc/openvpn/server
```

### Step 2: Certificate Generation

```bash
# Copy our certificate generation script
wget https://raw.githubusercontent.com/your-repo/china-vpn/main/tools/generate-certificates.sh
chmod +x generate-certificates.sh

# Generate certificates
./generate-certificates.sh

# Move certificates to OpenVPN directory
mv certificates/* /etc/openvpn/server/
```

### Step 3: Server Configuration

```bash
# Copy server configuration
wget https://raw.githubusercontent.com/your-repo/china-vpn/main/configs/server.conf -O /etc/openvpn/server/server.conf

# Edit configuration with your server's public IP
sed -i 's/china-vpn-server.example.com/YOUR_SERVER_IP/g' /etc/openvpn/server/server.conf
```

### Step 4: Network Configuration

```bash
# Enable IP forwarding
echo 'net.ipv4.ip_forward=1' >> /etc/sysctl.conf
sysctl -p

# Configure firewall
ufw allow 1194/udp
ufw allow ssh
ufw --force enable

# Configure NAT
iptables -t nat -A POSTROUTING -s 10.8.0.0/24 -o eth0 -j MASQUERADE
iptables -A INPUT -i tun+ -j ACCEPT
iptables -A FORWARD -i tun+ -j ACCEPT
iptables -A FORWARD -i tun+ -o eth0 -m state --state RELATED,ESTABLISHED -j ACCEPT
iptables -A FORWARD -i eth0 -o tun+ -m state --state RELATED,ESTABLISHED -j ACCEPT

# Save iptables rules
iptables-save > /etc/iptables/rules.v4
```

### Step 5: Start OpenVPN Service

```bash
# Enable and start OpenVPN
systemctl enable openvpn-server@server
systemctl start openvpn-server@server

# Check status
systemctl status openvpn-server@server
```

## 🔧 Advanced Server Configuration

### Performance Optimization for China

```bash
# Add to /etc/openvpn/server/server.conf

# TCP optimization
tcp-nodelay
push "tcp-nodelay"

# Buffer sizes for better performance
sndbuf 393216
rcvbuf 393216
push "sndbuf 393216"
push "rcvbuf 393216"

# Compression
comp-lzo adaptive
push "comp-lzo adaptive"

# Fast reconnection
fast-io
```

### DNS Configuration for Chinese Services

```bash
# Add to server.conf
push "dhcp-option DNS 119.29.29.29"    # Tencent DNS
push "dhcp-option DNS 182.254.116.116" # Tencent DNS
push "dhcp-option DNS 8.8.8.8"         # Google DNS (backup)
push "dhcp-option DNS 8.8.4.4"         # Google DNS (backup)
```

### Multiple Protocol Support

Create TCP configuration for areas with UDP restrictions:

```bash
# Copy UDP config to TCP
cp /etc/openvpn/server/server.conf /etc/openvpn/server/server-tcp.conf

# Modify for TCP
sed -i 's/proto udp/proto tcp/' /etc/openvpn/server/server-tcp.conf
sed -i 's/port 1194/port 443/' /etc/openvpn/server/server-tcp.conf

# Start TCP service
systemctl enable openvpn-server@server-tcp
systemctl start openvpn-server@server-tcp

# Allow TCP port
ufw allow 443/tcp
```

## 👥 Client Management

### Generate Client Configuration

```bash
#!/bin/bash
# generate-client.sh

CLIENT_NAME=$1
if [ -z "$CLIENT_NAME" ]; then
    echo "Usage: $0 <client-name>"
    exit 1
fi

cd /etc/openvpn/server

# Generate client certificate
openssl genrsa -out ${CLIENT_NAME}.key 4096
openssl req -new -key ${CLIENT_NAME}.key -out ${CLIENT_NAME}.csr -subj "/C=CN/ST=Beijing/L=Beijing/O=China VPN/OU=IT Department/CN=${CLIENT_NAME}"
openssl x509 -req -days 3650 -in ${CLIENT_NAME}.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out ${CLIENT_NAME}.crt

# Create client config
cat > ${CLIENT_NAME}.ovpn << EOF
client
dev tun
proto udp
remote $(curl -s ifconfig.me) 1194
resolv-retry infinite
nobind
persist-key
persist-tun
cipher AES-256-CBC
auth SHA256
key-direction 1
remote-cert-tls server
comp-lzo
verb 3

<ca>
$(cat ca.crt)
</ca>

<cert>
$(cat ${CLIENT_NAME}.crt)
</cert>

<key>
$(cat ${CLIENT_NAME}.key)
</key>

<tls-auth>
$(cat ta.key)
</tls-auth>
EOF

echo "Client configuration created: ${CLIENT_NAME}.ovpn"

# Cleanup
rm ${CLIENT_NAME}.csr
```

### Revoke Client Certificate

```bash
#!/bin/bash
# revoke-client.sh

CLIENT_NAME=$1
if [ -z "$CLIENT_NAME" ]; then
    echo "Usage: $0 <client-name>"
    exit 1
fi

cd /etc/openvpn/server

# Revoke certificate
openssl ca -revoke ${CLIENT_NAME}.crt -keyfile ca.key -cert ca.crt

# Generate CRL
openssl ca -gencrl -keyfile ca.key -cert ca.crt -out crl.pem

# Update server config to use CRL
echo "crl-verify /etc/openvpn/server/crl.pem" >> server.conf

# Restart service
systemctl restart openvpn-server@server

echo "Client ${CLIENT_NAME} revoked"
```

## 📊 Monitoring and Maintenance

### Server Monitoring Script

```bash
#!/bin/bash
# monitor-server.sh

echo "=== OpenVPN Server Status ==="
systemctl status openvpn-server@server --no-pager

echo -e "\n=== Connected Clients ==="
if [ -f /var/log/openvpn/openvpn-status.log ]; then
    grep "^CLIENT_LIST" /var/log/openvpn/openvpn-status.log | while read line; do
        echo $line | awk -F',' '{print "Client: " $2 " | IP: " $3 " | Connected: " $4}'
    done
else
    echo "No status log found"
fi

echo -e "\n=== Server Resources ==="
echo "CPU Usage: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | awk -F'%' '{print $1}')%"
echo "Memory Usage: $(free | grep Mem | awk '{printf("%.2f%%", $3/$2 * 100.0)}')"
echo "Disk Usage: $(df -h / | awk 'NR==2{printf "%s", $5}')"

echo -e "\n=== Network Traffic ==="
if command -v vnstat &> /dev/null; then
    vnstat -i eth0 --oneline | awk -F';' '{print "Today: " $4 " | This Month: " $6}'
else
    echo "Install vnstat for traffic monitoring: apt install vnstat"
fi
```

### Log Rotation

```bash
# Create logrotate config
cat > /etc/logrotate.d/openvpn << EOF
/var/log/openvpn/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 root root
    postrotate
        systemctl reload openvpn-server@server
    endscript
}
EOF
```

### Automated Backup

```bash
#!/bin/bash
# backup-vpn.sh

BACKUP_DIR="/root/vpn-backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup certificates and configs
tar -czf $BACKUP_DIR/vpn-backup-$DATE.tar.gz \
    /etc/openvpn/server/ \
    /etc/systemd/system/openvpn-server@* \
    /etc/iptables/rules.v4

# Keep only last 30 backups
find $BACKUP_DIR -name "vpn-backup-*.tar.gz" -mtime +30 -delete

echo "Backup completed: vpn-backup-$DATE.tar.gz"
```

## 🔒 Security Hardening

### Fail2Ban Configuration

```bash
# Install fail2ban
apt install fail2ban

# Create OpenVPN jail
cat > /etc/fail2ban/jail.d/openvpn.conf << EOF
[openvpn]
enabled = true
port = 1194
protocol = udp
filter = openvpn
logpath = /var/log/openvpn/openvpn.log
maxretry = 3
bantime = 3600
findtime = 600
EOF

# Create filter
cat > /etc/fail2ban/filter.d/openvpn.conf << EOF
[Definition]
failregex = ^.*TLS Error: incoming packet authentication failed from \[AF_INET\]<HOST>:\d+.*$
            ^.*VERIFY ERROR: depth=0, error=certificate verify failed: certificate has expired: C=.*, ST=.*, L=.*, O=.*, OU=.*, CN=.*, name=.*, emailAddress=.*$
            ^.*TLS_ERROR: BIO read tls_read_plaintext error: error:.*:SSL routines:ssl3_get_record:wrong version number$
            ^.*Fatal TLS error \(check_tls_errors_co\), restarting$
ignoreregex =
EOF

systemctl restart fail2ban
```

### Regular Security Updates

```bash
# Create update script
cat > /root/security-updates.sh << 'EOF'
#!/bin/bash
apt update
apt upgrade -y
apt autoremove -y

# Restart OpenVPN if updated
if [ -f /var/run/reboot-required ]; then
    echo "Reboot required after updates"
    # Uncomment next line for automatic reboot
    # reboot
fi
EOF

# Add to crontab for weekly updates
echo "0 2 * * 0 /root/security-updates.sh" | crontab -
```

## 🌍 Multi-Location Setup

### Load Balancer Configuration

For high availability, set up multiple servers:

```bash
# DNS round-robin setup
# Add multiple A records for your domain:
# vpn.yourdomain.com -> Server1_IP
# vpn.yourdomain.com -> Server2_IP
# vpn.yourdomain.com -> Server3_IP

# Client config with multiple remotes
remote vpn.yourdomain.com 1194 udp
remote vpn-backup.yourdomain.com 1194 udp
remote-random
```

## 🛠️ Troubleshooting

### Common Issues

#### 1. Connection Timeouts
```bash
# Check firewall
ufw status
iptables -L

# Check service status
systemctl status openvpn-server@server

# Check logs
tail -f /var/log/openvpn/openvpn.log
```

#### 2. DNS Resolution Issues
```bash
# Test DNS from server
nslookup mp.weixin.qq.com 119.29.29.29

# Check client DNS
# Add to client config:
dhcp-option DNS 119.29.29.29
```

#### 3. Performance Issues
```bash
# Check server resources
htop
iotop
nethogs

# Optimize kernel parameters
echo 'net.core.rmem_max = 134217728' >> /etc/sysctl.conf
echo 'net.core.wmem_max = 134217728' >> /etc/sysctl.conf
sysctl -p
```

## 📈 Performance Tuning

### Kernel Optimization

```bash
# Add to /etc/sysctl.conf
net.core.rmem_default = 262144
net.core.rmem_max = 16777216
net.core.wmem_default = 262144
net.core.wmem_max = 16777216
net.ipv4.tcp_rmem = 4096 65536 16777216
net.ipv4.tcp_wmem = 4096 65536 16777216
net.ipv4.tcp_congestion_control = bbr

# Apply changes
sysctl -p
```

### OpenVPN Tuning

```bash
# Add to server.conf
tun-mtu 1500
fragment 1300
mssfix 1300
sndbuf 0
rcvbuf 0
```

This comprehensive server setup guide provides everything needed to deploy a production-ready VPN server optimized for China access and WeChat services.
