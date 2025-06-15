<div align="center">

# 🇨🇳 FREE VPN - China Solution for WeChat

### 🚀 Free Open Source VPN - Specially designed for WeChat & Bot Development

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-blue)](https://github.com/Jabsama/FREE-VPN)
[![OpenVPN](https://img.shields.io/badge/OpenVPN-2.6+-green)](https://openvpn.net/)
[![WeChat](https://img.shields.io/badge/WeChat-Compatible-brightgreen)](https://mp.weixin.qq.com/)

**2-Second Installation • Automatic Configuration • Ready to Use**

[🚀 Quick Install](#-ultra-fast-installation) • [📖 Documentation](#-documentation) • [🤖 WeChat Bots](#-wechat-bot-development) • [🌐 Own Server](#-deploy-your-own-server)

</div>

---

## 🎯 **Why This VPN?**

### ❌ **Problems Solved:**
- **WeChat SMS not received** with French/European mobile operators
- **IP restrictions** on Chinese services (mp.weixin.qq.com blocked)
- **WeChat verification impossible** from Europe
- **Bot development** complicated outside China

### ✅ **Solutions Provided:**
- **Authentic Chinese IP** for WeChat
- **Optimized DNS** for Tencent services
- **Automatic configuration** in 2 clicks
- **Complete bot support** (Wechaty, itchat)

---

## 🚀 **Ultra-Fast Installation**

### 🎯 **ONE-CLICK START (Recommended)**
```cmd
# 1. Download the project
# 2. Right-click "🚀 START HERE.bat"
# 3. "Run as administrator"
# 4. Choose your experience!
```

**Interactive launcher with 8 options - perfect for beginners and pros!**

### 🌍 **Direct Access Options**

#### **China VPN (Quick)**
```cmd
Right-click "ONE-CLICK-VPN.bat" → "Run as administrator"
```

#### **Flexible VPN (15 Countries)**
```cmd
Right-click "FLEXIBLE-VPN.bat" → "Run as administrator"
```

#### **Web Interface**
```cmd
pip install -r requirements.txt
python web_interface.py
# Access: http://localhost:8080
```

#### **Linux/macOS**
```bash
sudo ./scripts/setup-linux.sh
```

---

## 🎮 **Simple Usage**

### **After installation:**

1. **📝 Configure**: Edit `configs/china-vpn.ovpn` with your server
2. **🔐 Certificates**: Add your VPN certificates
3. **🚀 Connect**: Double-click desktop icon "🇨🇳 China VPN"
4. **✅ Test**: Go to https://mp.weixin.qq.com/

### **Available commands (Linux/macOS):**
```bash
china-vpn-connect      # Connect
china-vpn-disconnect   # Disconnect  
china-vpn-status       # Check status
```

---

## 🏗️ **Technical Architecture**

```
FREE-VPN/
├── 🚀 LAUNCH-VPN.bat          # Windows 1-click installation
├── 📋 configs/
│   ├── china-vpn.ovpn         # Optimized client configuration
│   └── server.conf            # Server configuration
├── 🛠️ scripts/
│   ├── setup-windows.bat      # Windows installation
│   └── setup-linux.sh         # Linux/macOS installation
├── 🔧 tools/
│   └── generate-certificates.sh # Certificate generation
└── 📚 docs/
    ├── wechat-bot-integration.md
    └── server-setup-guide.md
```

---

## 🤖 **WeChat Bot Development**

### **Supported Frameworks:**
- **Wechaty** (Node.js) - Recommended
- **itchat** (Python)
- **WeChat4U** (Node.js)
- **BOT-SHA-256** (Multi-platform) - Perfect Integration ⭐

### **Quick Example:**
```javascript
// bot.js
const { Wechaty } = require('wechaty')

const bot = new Wechaty({ name: 'china-bot' })

bot.on('message', async msg => {
  if (msg.text() === 'ping') {
    await msg.say('pong from China! 🇨🇳')
  }
})

bot.start()
```

### **🚀 BOT-SHA-256 Integration (Recommended)**
Perfect for **VoltageGPU affiliate marketing** across 8 platforms:
- ✅ **WeChat, Bilibili, Zhihu, Weibo** (requires our VPN)
- ✅ **Twitter, Telegram, Reddit, LinkedIn** (global)
- ✅ **1,700+ posts/day** with Chinese market access
- ✅ **+$3,375/month** additional revenue potential

**📖 Complete Guides:** 
- [WeChat Bot Integration](docs/wechat-bot-integration.md)
- [BOT-SHA-256 Integration](docs/bot-sha-256-integration.md) ⭐

---

## 🌐 **Deploy Your Own Server**

### **Recommended Locations:**
1. **🇭🇰 Hong Kong** (Optimal)
2. **🇸🇬 Singapore** 
3. **🇹🇼 Taiwan**
4. **🇯🇵 Japan (Tokyo)**

### **Tested Providers:**
- **DigitalOcean** - Simple and fast
- **Vultr** - Multiple Asia locations
- **Linode** - Reliable infrastructure

**📖 Complete server guide:** [docs/server-setup-guide.md](docs/server-setup-guide.md)

---

## 🔧 **Advanced Features**

### **Security:**
- 🔐 **AES-256-CBC Encryption**
- 🛡️ **Integrated Kill Switch**
- 🚫 **DNS Leak Protection**
- 🔑 **TLS Authentication**

### **Performance:**
- ⚡ **China-Optimized**
- 🌐 **Tencent DNS** (119.29.29.29)
- 📡 **UDP/TCP Protocols**
- 🚀 **LZO Compression**

### **Compatibility:**
- 🪟 **Windows** 10/11
- 🐧 **Linux** (Ubuntu, CentOS, Arch)
- 🍎 **macOS** (Intel/Apple Silicon)

---

## 📊 **Project Statistics**

- ⭐ **100% Open Source** - Completely free code
- 🆓 **Free** - No hidden costs
- 🔒 **No logs** - Privacy respected
- 🌍 **Multi-platform** - Works everywhere
- 🤖 **Bot-ready** - Ready for development

---

## 🆘 **Support & Community**

### **Common Issues:**
```bash
# VPN won't connect?
china-vpn-status

# WeChat SMS not received?
curl ifconfig.me  # Check Chinese IP

# Bot not working?
ping mp.weixin.qq.com
```

### **Get Help:**
- 📖 **Documentation**: `docs/` folder
- 🐛 **Bug Report**: GitHub Issues
- 💬 **Discussions**: GitHub Discussions

---

## ⚖️ **Responsible Usage**

### **✅ Authorized Uses:**
- Legitimate WeChat bot development
- Application testing for Chinese market
- WeChat services access for businesses
- Research and education

### **❌ Prohibited Uses:**
- Circumventing legal restrictions
- Illegal or malicious activities
- Platform terms of service violations
- Unauthorized commercial usage

---

## 🤝 **Contributing**

This project is **100% open source** and welcomes contributions!

```bash
# Clone the project
git clone https://github.com/Jabsama/FREE-VPN.git

# Create a branch
git checkout -b feature/improvement

# Make your changes
# ...

# Submit your changes
git push origin feature/improvement
```

---

## 📄 **License**

**MIT License** - Free use with attribution

```
Copyright (c) 2025 FREE-VPN Project
For legitimate purposes only
```

---

<div align="center">

### 🌟 **If this project helps you, give it a star!** ⭐

**Made with ❤️ for the developer community**

[⬆️ Back to top](#-free-vpn---china-solution-for-wechat)

</div>
