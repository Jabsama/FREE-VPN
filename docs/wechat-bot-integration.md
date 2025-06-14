# WeChat Bot Integration Guide

This guide explains how to use the China VPN solution specifically for WeChat bot development and access to WeChat services.

## 🎯 Overview

WeChat has strict geographical restrictions and verification processes that can be challenging when developing bots or accessing WeChat services from outside mainland China. This VPN solution helps overcome these limitations.

## 🚧 Common WeChat Issues Outside China

### 1. SMS Verification Problems
- **Issue**: French and other non-Chinese mobile operators often don't receive WeChat SMS verification codes
- **Solution**: VPN connection makes WeChat think you're in China, improving SMS delivery rates

### 2. IP Restrictions
- **Issue**: Many WeChat services redirect to restricted pages for non-China IPs
- **Solution**: VPN provides Chinese IP address for full access

### 3. WeChat Web Access
- **Issue**: https://mp.weixin.qq.com/ may be restricted or limited outside China
- **Solution**: VPN enables full access to WeChat Web platform

## 🤖 Bot Development Setup

### Prerequisites
1. China VPN connection established
2. WeChat developer account
3. Bot development framework (recommended: wechaty, itchat, or similar)

### Step-by-Step Bot Setup

#### 1. Connect to VPN
```bash
# Linux/macOS
china-vpn-connect

# Windows
# Run "Connect China VPN.bat" from desktop
```

#### 2. Verify Connection
```bash
# Check your IP location
curl ifconfig.me

# Should show a Chinese IP address
china-vpn-status
```

#### 3. Access WeChat Web
1. Open browser
2. Navigate to https://mp.weixin.qq.com/
3. You should now have full access without restrictions

#### 4. Bot Framework Installation

##### Option A: Wechaty (Recommended)
```bash
# Install Node.js if not already installed
npm install -g wechaty

# Create new bot project
mkdir my-wechat-bot
cd my-wechat-bot
npm init -y
npm install wechaty
```

##### Option B: Python itchat
```bash
pip install itchat
```

### 5. Basic Bot Example

#### Wechaty Example (JavaScript)
```javascript
// bot.js
const { Wechaty } = require('wechaty')

const bot = new Wechaty({
  name: 'china-vpn-bot',
  puppet: 'wechaty-puppet-wechat',
})

bot
  .on('scan', (qrcode, status) => {
    console.log(`Scan QR Code to login: ${status}`)
    console.log(`https://wechaty.js.org/qrcode/${encodeURIComponent(qrcode)}`)
  })
  .on('login', user => {
    console.log(`User ${user} logged in`)
  })
  .on('message', async message => {
    console.log(`Message: ${message}`)
    
    if (message.text() === 'ping') {
      await message.say('pong')
    }
  })

bot.start()
  .then(() => console.log('Bot started'))
  .catch(console.error)
```

#### Python itchat Example
```python
# bot.py
import itchat

@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    if msg.text == 'ping':
        return 'pong'

# Login with QR code
itchat.auto_login(hotReload=True)

# Keep the bot running
itchat.run()
```

## 🔧 Advanced Configuration

### Custom DNS for WeChat Services
Add these DNS entries to your VPN configuration for optimal WeChat access:

```
# WeChat-specific DNS servers
push "dhcp-option DNS 119.29.29.29"  # Tencent DNS
push "dhcp-option DNS 182.254.116.116"  # Tencent DNS
```

### Firewall Rules for WeChat
Ensure these ports are open for WeChat services:

```bash
# WeChat Web ports
iptables -A OUTPUT -p tcp --dport 80 -j ACCEPT
iptables -A OUTPUT -p tcp --dport 443 -j ACCEPT
iptables -A OUTPUT -p tcp --dport 8080 -j ACCEPT

# WeChat app ports
iptables -A OUTPUT -p tcp --dport 80 -j ACCEPT
iptables -A OUTPUT -p tcp --dport 443 -j ACCEPT
iptables -A OUTPUT -p tcp --dport 8080 -j ACCEPT
iptables -A OUTPUT -p udp --dport 53 -j ACCEPT
```

## 📱 WeChat Account Verification

### Phone Number Verification
1. **Connect to VPN first**
2. Open WeChat registration
3. Enter your phone number (French numbers work better with VPN)
4. Wait for SMS (should arrive within 1-2 minutes with VPN)
5. Complete verification

### QR Code Login
1. **Ensure VPN is connected**
2. Generate QR code through your bot
3. Scan with WeChat mobile app
4. Confirm login on mobile device

## 🛠️ Troubleshooting

### Common Issues and Solutions

#### 1. SMS Not Received
```bash
# Check VPN connection
china-vpn-status

# Reconnect if needed
china-vpn-disconnect
china-vpn-connect

# Try different phone number format
# Instead of: +33123456789
# Try: 0033123456789
```

#### 2. WeChat Web Access Denied
```bash
# Clear browser cache and cookies
# Restart browser
# Verify IP location
curl ifconfig.me

# Should show Chinese IP
```

#### 3. Bot Connection Issues
```bash
# Check if WeChat servers are accessible
ping mp.weixin.qq.com

# Test HTTPS connection
curl -I https://mp.weixin.qq.com/

# Should return 200 OK
```

#### 4. VPN Disconnection During Bot Operation
```bash
# Set up automatic reconnection
# Add to crontab:
*/5 * * * * /usr/local/bin/china-vpn-status | grep -q "DISCONNECTED" && /usr/local/bin/china-vpn-connect
```

## 🔒 Security Best Practices

### 1. Bot Security
- Never hardcode credentials in your bot code
- Use environment variables for sensitive data
- Implement rate limiting to avoid WeChat restrictions
- Log all bot activities for debugging

### 2. VPN Security
- Regularly update VPN certificates
- Monitor VPN connection logs
- Use strong authentication methods
- Keep OpenVPN client updated

### 3. WeChat Compliance
- Follow WeChat's Terms of Service
- Implement proper user consent mechanisms
- Respect user privacy and data protection
- Avoid spam or automated mass messaging

## 📊 Monitoring and Logging

### VPN Connection Monitoring
```bash
# Create monitoring script
cat > /usr/local/bin/monitor-china-vpn << 'EOF'
#!/bin/bash
while true; do
    if ! china-vpn-status | grep -q "CONNECTED"; then
        echo "$(date): VPN disconnected, reconnecting..."
        china-vpn-connect
    fi
    sleep 60
done
EOF

chmod +x /usr/local/bin/monitor-china-vpn
```

### Bot Activity Logging
```javascript
// Add to your bot code
const fs = require('fs')

function logActivity(message) {
    const timestamp = new Date().toISOString()
    const logEntry = `${timestamp}: ${message}\n`
    fs.appendFileSync('bot-activity.log', logEntry)
}

// Use in your bot
bot.on('message', async message => {
    logActivity(`Received: ${message.text()}`)
    // ... rest of your message handling
})
```

## 🚀 Production Deployment

### Docker Deployment
```dockerfile
# Dockerfile
FROM node:16-alpine

# Install OpenVPN
RUN apk add --no-cache openvpn

# Copy VPN config
COPY configs/china-vpn.ovpn /etc/openvpn/

# Copy bot code
COPY . /app
WORKDIR /app

# Install dependencies
RUN npm install

# Start script that connects VPN then starts bot
CMD ["sh", "-c", "openvpn --config /etc/openvpn/china-vpn.ovpn --daemon && npm start"]
```

### Systemd Service
```ini
# /etc/systemd/system/wechat-bot.service
[Unit]
Description=WeChat Bot with China VPN
After=network.target china-vpn.service
Requires=china-vpn.service

[Service]
Type=simple
User=wechat-bot
WorkingDirectory=/opt/wechat-bot
ExecStart=/usr/bin/node bot.js
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

## 📞 Support and Resources

### WeChat Developer Resources
- [WeChat Official Documentation](https://developers.weixin.qq.com/doc/)
- [Wechaty Documentation](https://wechaty.js.org/)
- [WeChat Bot Examples](https://github.com/wechaty/wechaty-getting-started)

### VPN Support
- Check VPN logs: `tail -f /var/log/openvpn/openvpn.log`
- Test connectivity: `china-vpn-status`
- Community support: Create issues in the project repository

## ⚖️ Legal Considerations

**Important**: This tool is provided for legitimate business and educational purposes only. Users must:

1. Comply with local laws and regulations
2. Respect WeChat's Terms of Service
3. Follow data protection regulations (GDPR, etc.)
4. Use responsibly and ethically

The developers are not responsible for any misuse of this software or violations of terms of service.
