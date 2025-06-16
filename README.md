# 🌐 FREE VPN - Open Source VPN Dashboard

A complete, unified VPN solution with multiple modes for different use cases. Single file deployment with web dashboard interface.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Open Source](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://opensource.org/)

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/Jabsama/FREE-VPN.git
cd FREE-VPN

# Install dependencies
pip install -r requirements_api.txt

# Run the unified VPN dashboard
python unified_vpn.py
```

**Access:** http://localhost:8080

## ✨ Features

### 🎯 **Unified Dashboard**
- **Single file deployment** - Everything in `unified_vpn.py`
- **Auto-detection** - Automatically recommends best mode for your device
- **Web interface** - Modern, responsive dashboard
- **REST API** - Complete API for integration

### 🌍 **Multiple VPN Modes**

| Mode | Description | Requirements | Use Case |
|------|-------------|--------------|----------|
| **🖥️ Real VPN** | Actual internet routing via OpenVPN | OpenVPN + Admin rights | Desktop users wanting real VPN |
| **📱 Mobile** | Mobile-optimized proxy solution | None | Mobile devices and tablets |
| **🚀 Zero Install** | Browser-only, no installation | None | Quick access, no setup |
| **🧪 Demo** | Testing and development | None | Developers and testing |

### 🌐 **Server Network**
- **13 total servers** across 4 modes
- **Multiple countries** - USA, UK, Netherlands, Japan, Germany
- **Free servers** - ProtonVPN free tier integration
- **Proxy servers** - HTTP/HTTPS proxy support

## 📋 Requirements

### Minimal Requirements (Zero Install & Mobile modes)
- Python 3.7+
- Web browser
- Internet connection

### Full Requirements (Real VPN mode)
- Python 3.7+
- OpenVPN installed
- Administrator/root privileges
- Internet connection

## 🛠️ Installation

### Option 1: Quick Setup (Recommended)
```bash
git clone https://github.com/Jabsama/FREE-VPN.git
cd FREE-VPN
pip install flask flask-cors requests
python unified_vpn.py
```

### Option 2: With Requirements File
```bash
git clone https://github.com/Jabsama/FREE-VPN.git
cd FREE-VPN
pip install -r requirements_api.txt
python unified_vpn.py
```

### Option 3: OpenVPN Setup (for Real VPN mode)

**Windows:**
```bash
winget install OpenVPN.OpenVPN
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install openvpn
```

**macOS:**
```bash
brew install openvpn
```

## 🎮 Usage

### Web Dashboard
1. Start the server: `python unified_vpn.py`
2. Open browser: http://localhost:8080
3. Select your preferred mode (Real/Mobile/Zero/Demo)
4. Choose a server and click "Connect"

### API Usage
```python
import requests

# Get status
response = requests.get('http://localhost:8080/api/unified/status')
print(response.json())

# Connect to server
response = requests.post('http://localhost:8080/api/unified/connect/usa_real')
print(response.json())

# Disconnect
response = requests.post('http://localhost:8080/api/unified/disconnect')
print(response.json())
```

## 🔧 API Reference

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/unified/status` | Get current VPN status |
| `GET` | `/api/unified/servers` | List all available servers |
| `GET` | `/api/unified/servers?mode=real` | Filter servers by mode |
| `POST` | `/api/unified/connect/<server_key>` | Connect to specific server |
| `POST` | `/api/unified/disconnect` | Disconnect from VPN |
| `GET` | `/proxy/<url>` | Proxy endpoint for web requests |

### Response Format
```json
{
  "connected": true,
  "current_server": "usa_real",
  "current_mode": "real",
  "current_ip": "192.168.1.100",
  "recommended_mode": "real",
  "available_modes": ["real", "mobile", "zero", "demo"],
  "timestamp": "2025-06-16T17:30:00"
}
```

## 🌟 Modes Explained

### 🖥️ Real VPN Mode
- **What it does:** Routes all internet traffic through VPN servers
- **Requirements:** OpenVPN installed, admin privileges
- **Best for:** Desktop users wanting complete VPN protection
- **Servers:** ProtonVPN free tier (USA, Netherlands, Japan)

### 📱 Mobile Mode
- **What it does:** HTTP proxy optimized for mobile browsers
- **Requirements:** None
- **Best for:** Mobile devices, tablets, quick browsing
- **Servers:** Mobile-optimized proxy servers

### 🚀 Zero Install Mode
- **What it does:** Browser-based proxy using public services
- **Requirements:** None
- **Best for:** Quick access, no installation, restricted environments
- **Servers:** Cloudflare WARP, Google Translate, Archive.org, CORS proxies

### 🧪 Demo Mode
- **What it does:** Simulates VPN connection for testing
- **Requirements:** None
- **Best for:** Developers, testing, demonstrations
- **Servers:** Demo servers for development

## 🔒 Security Features

- **AES-256-CBC encryption** (Real VPN mode)
- **SHA256 authentication** (Real VPN mode)
- **DNS leak protection** (Real VPN mode)
- **HTTPS proxy connections** (Mobile/Zero modes)
- **No logging policy** - No user data stored
- **Open source** - Full code transparency

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch:** `git checkout -b feature/amazing-feature`
3. **Commit your changes:** `git commit -m 'Add amazing feature'`
4. **Push to the branch:** `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Setup
```bash
git clone https://github.com/Jabsama/FREE-VPN.git
cd FREE-VPN
pip install -r requirements_api.txt
python unified_vpn.py
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This software is provided for educational and research purposes. Users are responsible for complying with their local laws and regulations. The authors are not responsible for any misuse of this software.

## 🆘 Support

- **Issues:** [GitHub Issues](https://github.com/Jabsama/FREE-VPN/issues)
- **Discussions:** [GitHub Discussions](https://github.com/Jabsama/FREE-VPN/discussions)
- **Documentation:** This README and inline code comments

## 🎯 Roadmap

- [ ] Add more VPN providers
- [ ] Implement WireGuard support
- [ ] Add bandwidth monitoring
- [ ] Create mobile app
- [ ] Add user authentication
- [ ] Implement server load balancing

## 📊 Statistics

- **4 VPN modes** supported
- **13 servers** across multiple countries
- **Single file** deployment
- **Zero configuration** for most modes
- **Open source** and free to use

---

**Made with ❤️ for the open source community**

**Star ⭐ this repository if you find it useful!**
