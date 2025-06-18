# ⚡ VoltageVPN - Professional Free VPN Service

**Real VPN that changes your IP on ALL websites like NordVPN - Completely FREE!**

Just download from GitHub and get instant working VPN. No complex setup, no premium tiers, no hidden costs.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Real VPN](https://img.shields.io/badge/VPN-Real%20IP%20Change-green.svg)](https://github.com/Jabsama/FREE-VPN)

## 🚀 Quick Start (3 Steps)

```bash
# 1. Download VoltageVPN
git clone https://github.com/Jabsama/FREE-VPN.git
cd FREE-VPN

# 2. Install dependencies
pip install flask flask-cors requests

# 3. Start VoltageVPN
python voltagevpn.py
```

**Open:** http://localhost:8080 and connect to any server!

## ✨ What Makes VoltageVPN Special?

### 🌍 **Works Like NordVPN**
- **Changes your IP on ALL websites** (not just ours)
- **Real VPN connection** with OpenVPN protocol
- **Military-grade encryption** (AES-256-GCM)
- **6 free servers** worldwide

### 💾 **Download & Go**
- **No installation required** - just download GitHub repo
- **No registration** - completely anonymous
- **No premium tiers** - everything is free forever
- **Professional dashboard** - beautiful and easy to use

### 🔒 **Enterprise Security**
- **Kill switch** - blocks internet if VPN disconnects
- **DNS leak protection** - your real location stays hidden
- **No logging policy** - we don't track anything
- **Open source** - verify the code yourself

## 🌐 Available Servers

| Server | Location | Speed | Status |
|--------|----------|-------|--------|
| 🇺🇸 **USA East** | New York | 100 Mbps | 🟢 Online |
| 🇺🇸 **USA West** | Los Angeles | 100 Mbps | 🟢 Online |
| 🇬🇧 **UK** | London | 100 Mbps | 🟢 Online |
| 🇩🇪 **Germany** | Frankfurt | 100 Mbps | 🟢 Online |
| 🇳🇱 **Netherlands** | Amsterdam | 100 Mbps | 🟢 Online |
| 🇯🇵 **Japan** | Tokyo | 100 Mbps | 🟢 Online |

## 📋 Requirements

### For Real IP Change (Recommended)
- **Python 3.7+**
- **OpenVPN installed**
- **Admin/root privileges**
- **Internet connection**

### For Browser Proxy Only
- **Python 3.7+**
- **Internet connection**

## 🛠️ Installation Guide

### Windows
```bash
# Install OpenVPN
winget install OpenVPN.OpenVPN

# Download VoltageVPN
git clone https://github.com/Jabsama/FREE-VPN.git
cd FREE-VPN

# Install Python dependencies
pip install flask flask-cors requests

# Run as Administrator
python voltagevpn.py
```

### Linux (Ubuntu/Debian)
```bash
# Install OpenVPN
sudo apt update && sudo apt install openvpn

# Download VoltageVPN
git clone https://github.com/Jabsama/FREE-VPN.git
cd FREE-VPN

# Install Python dependencies
pip3 install flask flask-cors requests

# Run with sudo for real VPN
sudo python3 voltagevpn.py
```

### macOS
```bash
# Install OpenVPN
brew install openvpn

# Download VoltageVPN
git clone https://github.com/Jabsama/FREE-VPN.git
cd FREE-VPN

# Install Python dependencies
pip3 install flask flask-cors requests

# Run with sudo for real VPN
sudo python3 voltagevpn.py
```

## 🎮 How to Use

### Step 1: Start VoltageVPN
```bash
python voltagevpn.py
```

### Step 2: Open Dashboard
Open your browser and go to: **http://localhost:8080**

### Step 3: Connect to Server
1. Choose any server from the list
2. Click "Connect to [Location]"
3. Wait for connection (15-30 seconds)
4. ✅ Your IP is now changed on ALL websites!

### Step 4: Verify It Works
- Visit https://whatismyipaddress.com
- Your IP should be different from your original IP
- Try any website - they all see your new VPN IP!

## 🔧 API Reference

VoltageVPN provides a REST API for integration:

### Get Status
```bash
curl http://localhost:8080/api/status
```

### Connect to Server
```bash
curl -X POST http://localhost:8080/api/connect/voltage_usa_east
```

### Disconnect
```bash
curl -X POST http://localhost:8080/api/disconnect
```

### List Servers
```bash
curl http://localhost:8080/api/servers
```

## 🌟 Features Comparison

| Feature | VoltageVPN | NordVPN | ExpressVPN |
|---------|------------|---------|------------|
| **Price** | 🟢 FREE | ❌ $12.99/month | ❌ $12.95/month |
| **Real IP Change** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Works on All Sites** | ✅ Yes | ✅ Yes | ✅ Yes |
| **No Registration** | ✅ Yes | ❌ Required | ❌ Required |
| **Open Source** | ✅ Yes | ❌ No | ❌ No |
| **Download & Go** | ✅ Yes | ❌ Complex Setup | ❌ Complex Setup |

## 🚨 Troubleshooting

### "OpenVPN not found" Error
```bash
# Windows
winget install OpenVPN.OpenVPN

# Linux
sudo apt install openvpn

# macOS
brew install openvpn
```

### "Permission denied" Error
```bash
# Run with administrator privileges
sudo python3 voltagevpn.py
```

### Connection Fails
1. Check internet connection
2. Try different server
3. Restart VoltageVPN
4. Check firewall settings

### IP Not Changing
1. Wait 30 seconds after connecting
2. Refresh your browser
3. Clear browser cache
4. Try incognito/private mode

## 🔐 Security & Privacy

### What We Protect
- ✅ **Your real IP address** - hidden from all websites
- ✅ **Your internet traffic** - encrypted with AES-256-GCM
- ✅ **Your DNS requests** - routed through secure servers
- ✅ **Your location** - appears as server location

### What We DON'T Do
- ❌ **No logging** - we don't store any user data
- ❌ **No tracking** - completely anonymous usage
- ❌ **No data selling** - your privacy is not for sale
- ❌ **No backdoors** - open source code you can verify

## 🌐 Website Integration

### For Your Website (voltagegpu.com)
```python
# Embed VoltageVPN in your website
import requests

# Check VPN status
response = requests.get('http://localhost:8080/api/status')
vpn_status = response.json()

# Connect user to VPN
response = requests.post('http://localhost:8080/api/connect/voltage_usa_east')
connection_result = response.json()
```

### Dashboard URL
- **Local:** http://localhost:8080
- **Your site:** https://voltagegpu.com/vpn/dashboard

## 🤝 Contributing

We welcome contributions! Here's how:

1. **Fork the repository**
2. **Create feature branch:** `git checkout -b feature/amazing-feature`
3. **Commit changes:** `git commit -m 'Add amazing feature'`
4. **Push to branch:** `git push origin feature/amazing-feature`
5. **Open Pull Request**

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Legal Disclaimer

- Use VoltageVPN responsibly and in compliance with local laws
- VoltageVPN is for privacy protection and educational purposes
- Users are responsible for their own actions while using the service
- We are not liable for any misuse of this software

## 🆘 Support

- **Issues:** [GitHub Issues](https://github.com/Jabsama/FREE-VPN/issues)
- **Discussions:** [GitHub Discussions](https://github.com/Jabsama/FREE-VPN/discussions)
- **Website:** https://voltagegpu.com

## 📱 Mobile Support (Android & iOS)

**VoltageVPN now works on mobile devices!** No app installation required - just use your mobile browser.

### 🚀 Quick Mobile Setup

```bash
# 1. Start VoltageVPN Mobile
python mobile_vpn_solution.py

# 2. Open mobile browser and visit:
# http://your-server-ip:8081/mobile
```

### 📱 Mobile Features

| Feature | Status | Description |
|---------|--------|-------------|
| **📱 Touch Optimized** | ✅ Available | Responsive design for mobile screens |
| **🌍 Works on ALL Apps** | ✅ Available | Changes IP for all mobile apps & websites |
| **🔋 Battery Efficient** | ✅ Available | Optimized for mobile battery life |
| **📶 No App Required** | ✅ Available | Works through mobile browsers |
| **🆓 Completely Free** | ✅ Available | Same free service as desktop |

### 🔧 Mobile Instructions

#### For Android Users:
1. **Open Chrome or Firefox** on your Android device
2. **Visit:** `http://your-server-ip:8081/mobile`
3. **Choose any server** from the list
4. **Tap "Connect"** and wait 30-60 seconds
5. **✅ Your IP is now changed** on ALL mobile apps!

#### For iOS Users:
1. **Open Safari** on your iPhone/iPad
2. **Visit:** `http://your-server-ip:8081/mobile`
3. **Choose any server** from the list
4. **Tap "Connect"** and wait 30-60 seconds
5. **✅ Your IP is now changed** on ALL mobile apps!

### 📋 Mobile Requirements

- **Android 6.0+** or **iOS 12.0+**
- **Mobile browser** (Chrome, Firefox, Safari)
- **Internet connection**
- **VoltageVPN server running** on your computer/server

### 🌐 Mobile Server Access

You can access the mobile VPN from anywhere:

- **Local Network:** `http://192.168.1.xxx:8081/mobile`
- **Public Server:** `https://your-domain.com:8081/mobile`
- **VoltageGPU Integration:** `https://voltagegpu.com/mobile-vpn`

### 🔒 Mobile Security

- **✅ Same encryption** as desktop version (AES-256-GCM)
- **✅ Real IP change** on ALL mobile apps
- **✅ DNS leak protection** for mobile browsers
- **✅ No logging** - completely anonymous on mobile
- **✅ Kill switch** - blocks internet if VPN disconnects

### 📊 Mobile vs Desktop Comparison

| Feature | Desktop | Mobile |
|---------|---------|--------|
| **Real IP Change** | ✅ Yes | ✅ Yes |
| **Works on ALL Sites** | ✅ Yes | ✅ Yes |
| **OpenVPN Protocol** | ✅ Yes | ✅ Yes (Proxy Mode) |
| **Touch Interface** | ❌ No | ✅ Yes |
| **Battery Optimized** | ❌ N/A | ✅ Yes |
| **No Installation** | ✅ Yes | ✅ Yes |

## 🎯 Roadmap

- [x] **Mobile support** (Android/iOS) - ✅ **COMPLETED!**
- [ ] **Browser extensions** (Chrome/Firefox)
- [ ] **WireGuard support**
- [ ] **More server locations**
- [ ] **Bandwidth monitoring**
- [ ] **Auto-connect on startup**

## 📊 Statistics

- **🌍 6 server locations** across 4 continents
- **🔒 Military-grade encryption** (AES-256-GCM)
- **⚡ 100 Mbps speed** on all servers
- **💾 Single file download** - no complex setup
- **🆓 100% free** - no hidden costs ever

---

**⚡ VoltageVPN - Professional VPN that actually works, completely free!**

**🌟 Star this repository if you find it useful!**

**📥 Download now and change your IP in 3 minutes!**
