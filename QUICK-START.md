# 🚀 Quick Start Guide - China VPN for WeChat

Get up and running with the China VPN solution in minutes!

## 📋 What You Get

This open-source VPN solution helps you:
- ✅ Access WeChat Web (https://mp.weixin.qq.com/) without restrictions
- ✅ Receive WeChat SMS verification codes reliably
- ✅ Develop and test WeChat bots from outside China
- ✅ Bypass IP restrictions on Chinese services

## 🎯 Choose Your Setup Method

### Option 1: Ultra-Fast Installation (Recommended)

#### Windows Users:
```cmd
# Right-click "LAUNCH-VPN.bat" and select "Run as Administrator"
LAUNCH-VPN.bat
```

#### Linux/macOS Users:
```bash
sudo ./scripts/setup-linux.sh
```

### Option 2: Use Existing VPN Service
If you already have a VPN server or service with Chinese IP addresses:

1. **Download the client config**: Use `configs/china-vpn.ovpn`
2. **Update server details**: Replace `china-vpn-server.example.com` with your server
3. **Add your certificates**: Replace the placeholder certificates with real ones
4. **Connect and test**: Access https://mp.weixin.qq.com/

### Option 3: Set Up Your Own Server (Full Control)
Follow the complete server setup guide: `docs/server-setup-guide.md`

## 🔧 Quick Configuration

### 1. Update Server Address
Edit `configs/china-vpn.ovpn`:
```
# Change this line:
remote china-vpn-server.example.com 1194

# To your server:
remote YOUR_SERVER_IP 1194
```

### 2. Add Certificates
Replace the placeholder certificates in `china-vpn.ovpn` with real ones:
- `<ca>` section: Your CA certificate
- `<cert>` section: Your client certificate  
- `<key>` section: Your client private key
- `<tls-auth>` section: Your TLS auth key

### 3. Generate Certificates (If Needed)
```bash
# Linux/macOS
cd tools
./generate-certificates.sh

# Windows (use Git Bash or WSL)
cd tools
bash generate-certificates.sh
```

## 🤖 WeChat Bot Integration

### Quick Bot Test
1. **Connect to VPN**:
   ```bash
   # Linux/macOS
   china-vpn-connect
   
   # Windows: Run "Connect China VPN.bat"
   ```

2. **Verify Chinese IP**:
   ```bash
   curl ifconfig.me
   # Should show a Chinese IP address
   ```

3. **Test WeChat Web Access**:
   - Open browser
   - Go to https://mp.weixin.qq.com/
   - Should load without restrictions

4. **Install Bot Framework**:
   ```bash
   # Node.js (Wechaty)
   npm install -g wechaty
   
   # Python (itchat)
   pip install itchat
   ```

5. **Run Sample Bot**:
   See examples in `docs/wechat-bot-integration.md`

## 🌐 Recommended Server Locations

For best WeChat performance, use servers in:
1. **Hong Kong** (Best)
2. **Singapore** 
3. **Taiwan**
4. **Japan (Tokyo)**
5. **South Korea (Seoul)**

## 🔍 Troubleshooting

### Common Issues:

#### VPN Won't Connect
```bash
# Check config file
cat configs/china-vpn.ovpn | grep remote

# Test server connectivity
ping YOUR_SERVER_IP

# Check OpenVPN logs
tail -f /var/log/openvpn/openvpn.log
```

#### WeChat SMS Not Received
```bash
# Verify VPN connection
china-vpn-status

# Check IP location
curl ifconfig.me

# Try different phone number format
# Instead of: +33123456789
# Try: 0033123456789
```

#### WeChat Web Access Denied
```bash
# Clear browser cache
# Restart browser
# Verify Chinese IP
curl ifconfig.me
```

## 📚 Documentation

- **WeChat Bot Guide**: `docs/wechat-bot-integration.md`
- **Server Setup**: `docs/server-setup-guide.md`
- **Main README**: `README.md`

## 🆘 Getting Help

1. **Check logs**: Look for error messages in VPN logs
2. **Test connectivity**: Use `china-vpn-status` command
3. **Verify certificates**: Ensure all certificates are valid
4. **Check firewall**: Make sure ports 1194 (UDP) and 443 (TCP) are open

## ⚡ Pro Tips

### For Better Performance:
- Use UDP protocol when possible (faster)
- Choose servers geographically close to China
- Use compression (`comp-lzo`) for slower connections
- Enable `fast-io` for better throughput

### For WeChat Bots:
- Always connect VPN before starting bot
- Use Chinese DNS servers (119.29.29.29)
- Implement reconnection logic in your bot
- Monitor VPN connection status

### For Security:
- Regularly update certificates
- Use strong authentication
- Monitor connection logs
- Keep OpenVPN client updated

## 🎉 Success Indicators

You'll know everything is working when:
- ✅ `china-vpn-status` shows "CONNECTED"
- ✅ `curl ifconfig.me` returns a Chinese IP
- ✅ https://mp.weixin.qq.com/ loads without restrictions
- ✅ WeChat SMS verification works
- ✅ Your bot can connect to WeChat services

## 🚨 Important Notes

- **Legal Compliance**: Use only for legitimate purposes
- **Terms of Service**: Respect WeChat's and other platforms' ToS
- **Privacy**: This is open-source - no data collection
- **Support**: Community-driven project

---

**Ready to get started?** Choose your setup method above and follow the steps!

For detailed documentation, see the `docs/` folder.
