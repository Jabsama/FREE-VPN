# 🌍 Flexible VPN Guide - Like NordVPN

Complete guide for the flexible VPN solution with country selection and web interface.

## 🎯 Overview

The Flexible VPN transforms your basic China VPN into a **professional multi-country VPN solution** similar to NordVPN, with:

- **15 global server locations**
- **Web-based control panel**
- **API for website integration**
- **One-click country switching**
- **Professional interface**

## 🚀 Quick Start

### Method 1: Desktop Application
```cmd
# Right-click "FLEXIBLE-VPN.bat" and "Run as administrator"
FLEXIBLE-VPN.bat
```

### Method 2: Web Interface
```cmd
# Install Python dependencies
pip install -r requirements.txt

# Launch web interface
python web_interface.py

# Access at: http://localhost:8080
```

## 🌍 Available Locations

### 🇦🇸 Asia-Pacific
| Country | Server | Best For |
|---------|--------|----------|
| 🇨🇳 Hong Kong | `hk-01.freevpn.world` | WeChat, Bilibili, Chinese services |
| 🇸🇬 Singapore | `sg-01.freevpn.world` | Fast Asian connection, low latency |
| 🇯🇵 Japan | `jp-01.freevpn.world` | Gaming, anime streaming |
| 🇰🇷 South Korea | `kr-01.freevpn.world` | K-pop streaming, Korean services |
| 🇹🇼 Taiwan | `tw-01.freevpn.world` | Chinese services, regional content |
| 🇮🇳 India | `in-01.freevpn.world` | Bollywood, Indian services |
| 🇦🇺 Australia | `au-01.freevpn.world` | Oceania region, Australian content |

### 🇺🇸 Americas
| Country | Server | Best For |
|---------|--------|----------|
| 🇺🇸 USA East | `us-ny-01.freevpn.world` | Netflix US, East Coast |
| 🇺🇸 USA West | `us-la-01.freevpn.world` | Hollywood content, West Coast |
| 🇨🇦 Canada | `ca-01.freevpn.world` | North America, privacy laws |
| 🇧🇷 Brazil | `br-01.freevpn.world` | South America, Portuguese content |

### 🇪🇺 Europe
| Country | Server | Best For |
|---------|--------|----------|
| 🇬🇧 UK | `uk-01.freevpn.world` | BBC iPlayer, UK content |
| 🇩🇪 Germany | `de-01.freevpn.world` | EU privacy laws, central Europe |
| 🇫🇷 France | `fr-01.freevpn.world` | French content, EU location |
| 🇳🇱 Netherlands | `nl-01.freevpn.world` | Privacy friendly, torrenting |

## 🖥️ Desktop Interface Features

### Main Menu Options
```
🌍 Available VPN Locations:

🇨🇳 1. China (Hong Kong)     - Best for WeChat, Bilibili
🇸🇬 2. Singapore             - Fast Asian connection
🇯🇵 3. Japan (Tokyo)         - Gaming optimized
🇰🇷 4. South Korea (Seoul)   - K-pop streaming
🇹🇼 5. Taiwan               - Chinese services
🇺🇸 6. USA (New York)        - Netflix US
🇺🇸 7. USA (Los Angeles)     - West Coast
🇬🇧 8. UK (London)          - BBC iPlayer
🇩🇪 9. Germany (Frankfurt)   - EU privacy
🇫🇷 10. France (Paris)       - Local content
🇳🇱 11. Netherlands          - Torrenting
🇨🇦 12. Canada (Toronto)     - North America
🇦🇺 13. Australia (Sydney)   - Oceania
🇧🇷 14. Brazil (São Paulo)   - South America
🇮🇳 15. India (Mumbai)       - Bollywood

🤖 16. AUTO (Best for Bots)   - Automatic selection
🔄 17. DISCONNECT            - Stop VPN
🌐 18. WEB INTERFACE         - Launch web control
```

### Usage Examples
```cmd
# Connect to China for WeChat bots
Choose location (1-18): 1

# Connect to USA for Netflix
Choose location (1-18): 6

# Auto-select best for bots
Choose location (1-18): 16

# Launch web interface
Choose location (1-18): 18
```

## 🌐 Web Interface Features

### Professional Dashboard
- **Real-time connection status**
- **IP address and location display**
- **Connection uptime tracking**
- **Server selection with flags**
- **One-click connect/disconnect**

### API Endpoints
```javascript
// Get current status
GET /api/status
Response: {
  "status": "connected",
  "current_location": "china",
  "ip_address": "103.XXX.XXX.XXX",
  "country": "Hong Kong",
  "city": "Hong Kong",
  "uptime": "0:15:32",
  "timestamp": "2025-06-15T17:53:00"
}

// Connect to location
POST /api/connect
Body: {"location": "china"}
Response: {"success": true, "message": "Connected to Hong Kong (China)"}

// Disconnect VPN
POST /api/disconnect
Response: {"success": true, "message": "VPN disconnected"}

// Get available servers
GET /api/servers
Response: {server configuration object}

// Get best server for bots
GET /api/best-for-bot
Response: {
  "recommended": "china",
  "server": {...},
  "reason": "Best for WeChat, Bilibili, and Chinese bot platforms"
}
```

## 🔗 Website Integration

### Simple Button Integration
```html
<button class="vpn-btn" onclick="activateVPN()">🇨🇳 Activate China VPN</button>

<style>
.vpn-btn { 
    background: linear-gradient(45deg, #4CAF50, #45a049);
    color: white; border: none; padding: 15px 30px; 
    font-size: 18px; border-radius: 25px; cursor: pointer;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    transition: all 0.3s ease;
}
.vpn-btn:hover { 
    transform: translateY(-2px); 
    box-shadow: 0 6px 20px rgba(0,0,0,0.3); 
}
</style>

<script>
function activateVPN() {
    fetch('http://localhost:8080/api/connect', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ location: 'china' })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('✅ China VPN Activated! Perfect for WeChat bots.');
        } else {
            alert('❌ Connection failed: ' + data.message);
        }
    });
}
</script>
```

### Advanced Widget Integration
```html
<!-- Embeddable VPN widget -->
<iframe src="http://localhost:8080/widget" width="400" height="300" frameborder="0"></iframe>
```

### JavaScript API Integration
```javascript
// VPN Manager Class
class VPNManager {
    constructor(apiUrl = 'http://localhost:8080') {
        this.apiUrl = apiUrl;
    }
    
    async getStatus() {
        const response = await fetch(`${this.apiUrl}/api/status`);
        return await response.json();
    }
    
    async connect(location) {
        const response = await fetch(`${this.apiUrl}/api/connect`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ location })
        });
        return await response.json();
    }
    
    async disconnect() {
        const response = await fetch(`${this.apiUrl}/api/disconnect`, {
            method: 'POST'
        });
        return await response.json();
    }
    
    async getBestForBot() {
        const response = await fetch(`${this.apiUrl}/api/best-for-bot`);
        return await response.json();
    }
}

// Usage example
const vpn = new VPNManager();

// Connect to best server for bots
vpn.getBestForBot().then(result => {
    vpn.connect(result.recommended).then(response => {
        console.log('VPN Status:', response);
    });
});

// Check status
vpn.getStatus().then(status => {
    console.log('Current status:', status);
});
```

## 🤖 Bot Integration

### Automatic VPN for Chinese Platforms
```python
# Enhanced bot integration
import requests
import subprocess

class FlexibleVPNManager:
    def __init__(self):
        self.api_url = "http://localhost:8080"
        self.chinese_platforms = ['wechat', 'bilibili', 'zhihu', 'weibo']
    
    def get_status(self):
        """Get current VPN status"""
        try:
            response = requests.get(f"{self.api_url}/api/status")
            return response.json()
        except:
            return {'status': 'disconnected'}
    
    def connect_for_platform(self, platform):
        """Connect to optimal server for platform"""
        if platform.lower() in self.chinese_platforms:
            # Use China server for Chinese platforms
            return self.connect('china')
        else:
            # Use best general server
            return self.connect('usa_ny')
    
    def connect(self, location):
        """Connect to specific location"""
        try:
            response = requests.post(f"{self.api_url}/api/connect", 
                                   json={'location': location})
            return response.json()
        except:
            return {'success': False, 'message': 'API unavailable'}
    
    def disconnect(self):
        """Disconnect VPN"""
        try:
            response = requests.post(f"{self.api_url}/api/disconnect")
            return response.json()
        except:
            return {'success': False, 'message': 'API unavailable'}
    
    def ensure_connection_for_bot(self, platforms):
        """Ensure VPN is connected for bot platforms"""
        chinese_platforms_used = any(p in self.chinese_platforms for p in platforms)
        
        if chinese_platforms_used:
            status = self.get_status()
            if status['status'] != 'connected' or status.get('current_location') != 'china':
                print("🇨🇳 Connecting to China VPN for Chinese platforms...")
                result = self.connect('china')
                if result['success']:
                    print("✅ Connected to China VPN")
                    return True
                else:
                    print(f"❌ Connection failed: {result['message']}")
                    return False
        return True

# Usage in your bot
vpn = FlexibleVPNManager()

def run_bot_with_flexible_vpn():
    platforms = ['twitter', 'telegram', 'wechat', 'bilibili']  # Your bot platforms
    
    if vpn.ensure_connection_for_bot(platforms):
        print("🤖 Starting bot with optimal VPN connection...")
        # Start your bot here
        run_your_bot()
    else:
        print("⚠️ VPN connection failed, running without Chinese platforms")
        # Run bot without Chinese platforms
        run_bot_global_only()
```

### Smart Platform Routing
```python
# Platform-specific VPN routing
PLATFORM_VPN_MAP = {
    'wechat': 'china',
    'bilibili': 'china', 
    'zhihu': 'china',
    'weibo': 'china',
    'twitter': 'usa_ny',
    'reddit': 'usa_ny',
    'telegram': 'netherlands',  # Privacy-friendly
    'linkedin': 'usa_ny'
}

def run_platform_with_vpn(platform, action):
    """Run platform action with optimal VPN"""
    required_location = PLATFORM_VPN_MAP.get(platform, 'usa_ny')
    
    # Check if we need to switch VPN
    current_status = vpn.get_status()
    if current_status.get('current_location') != required_location:
        print(f"🔄 Switching to {required_location} for {platform}")
        vpn.connect(required_location)
    
    # Run platform action
    return action()

# Example usage
def post_to_wechat():
    return run_platform_with_vpn('wechat', lambda: your_wechat_post_function())

def post_to_twitter():
    return run_platform_with_vpn('twitter', lambda: your_twitter_post_function())
```

## 🔧 Advanced Configuration

### Custom Server Configuration
```python
# Add custom servers to web_interface.py
CUSTOM_SERVERS = {
    'custom_server': {
        'name': 'My Custom Server',
        'server': 'my-server.example.com',
        'flag': '🏴',
        'description': 'My personal VPN server',
        'category': 'custom'
    }
}

# Merge with existing servers
VPN_SERVERS.update(CUSTOM_SERVERS)
```

### Environment Configuration
```bash
# Create .env file for configuration
VPN_API_PORT=8080
VPN_API_HOST=0.0.0.0
DEFAULT_LOCATION=china
AUTO_CONNECT_FOR_BOTS=true
LOG_LEVEL=INFO
```

### Production Deployment
```python
# production_config.py
import os

class ProductionConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')
    VPN_API_PORT = int(os.environ.get('VPN_API_PORT', 8080))
    VPN_API_HOST = os.environ.get('VPN_API_HOST', '0.0.0.0')
    SSL_CERT = os.environ.get('SSL_CERT_PATH')
    SSL_KEY = os.environ.get('SSL_KEY_PATH')

# Run with SSL
if __name__ == '__main__':
    config = ProductionConfig()
    if config.SSL_CERT and config.SSL_KEY:
        app.run(
            host=config.VPN_API_HOST,
            port=config.VPN_API_PORT,
            ssl_context=(config.SSL_CERT, config.SSL_KEY)
        )
    else:
        app.run(host=config.VPN_API_HOST, port=config.VPN_API_PORT)
```

## 📊 Monitoring and Analytics

### Connection Analytics
```python
# Add to web_interface.py
import sqlite3
from datetime import datetime

def log_connection(location, action, success):
    """Log VPN connections for analytics"""
    conn = sqlite3.connect('vpn_analytics.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS connections (
            id INTEGER PRIMARY KEY,
            timestamp TEXT,
            location TEXT,
            action TEXT,
            success BOOLEAN,
            ip_address TEXT
        )
    ''')
    
    cursor.execute('''
        INSERT INTO connections (timestamp, location, action, success, ip_address)
        VALUES (?, ?, ?, ?, ?)
    ''', (datetime.now().isoformat(), location, action, success, get_current_ip()['ip']))
    
    conn.commit()
    conn.close()

@app.route('/api/analytics')
def api_analytics():
    """Get connection analytics"""
    conn = sqlite3.connect('vpn_analytics.db')
    cursor = conn.cursor()
    
    # Get connection stats
    cursor.execute('''
        SELECT location, COUNT(*) as count, 
               SUM(CASE WHEN success THEN 1 ELSE 0 END) as successful
        FROM connections 
        WHERE action = 'connect'
        GROUP BY location
    ''')
    
    stats = cursor.fetchall()
    conn.close()
    
    return jsonify({
        'total_connections': sum(row[1] for row in stats),
        'success_rate': sum(row[2] for row in stats) / sum(row[1] for row in stats) if stats else 0,
        'location_stats': [{'location': row[0], 'count': row[1], 'success_rate': row[2]/row[1]} for row in stats]
    })
```

## 🛡️ Security Features

### API Authentication
```python
# Add API key authentication
import hashlib
import secrets

API_KEYS = {
    'your-website': hashlib.sha256('your-secret-key'.encode()).hexdigest()
}

def require_api_key(f):
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key or api_key not in API_KEYS.values():
            return jsonify({'error': 'Invalid API key'}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/api/connect', methods=['POST'])
@require_api_key
def api_connect():
    # Your existing connect code
    pass
```

### Rate Limiting
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

@app.route('/api/connect', methods=['POST'])
@limiter.limit("10 per minute")
def api_connect():
    # Your existing connect code
    pass
```

## 🚀 Performance Optimization

### Connection Caching
```python
import time

class ConnectionCache:
    def __init__(self):
        self.cache = {}
        self.cache_duration = 300  # 5 minutes
    
    def get_cached_status(self):
        if 'status' in self.cache:
            if time.time() - self.cache['status']['timestamp'] < self.cache_duration:
                return self.cache['status']['data']
        return None
    
    def cache_status(self, status):
        self.cache['status'] = {
            'data': status,
            'timestamp': time.time()
        }

cache = ConnectionCache()

@app.route('/api/status')
def api_status():
    # Try cache first
    cached = cache.get_cached_status()
    if cached:
        return jsonify(cached)
    
    # Get fresh status
    status = get_fresh_status()
    cache.cache_status(status)
    return jsonify(status)
```

## 🎉 Success Indicators

Your Flexible VPN is working perfectly when:

- ✅ **Desktop interface** shows all 15 countries
- ✅ **Web interface** loads at http://localhost:8080
- ✅ **API endpoints** respond correctly
- ✅ **Country switching** works in seconds
- ✅ **Website integration** button functions
- ✅ **Bot integration** auto-connects for Chinese platforms

## 🔮 Future Enhancements

### Planned Features
- **Mobile app** (React Native)
- **Browser extension** (Chrome/Firefox)
- **Desktop GUI** (Electron)
- **Load balancing** across multiple servers
- **Speed testing** for optimal server selection
- **Kill switch** implementation
- **Split tunneling** for specific apps

---

**You now have a professional VPN solution comparable to NordVPN!** 🌍✨
