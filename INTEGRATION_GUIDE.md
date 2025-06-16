# 🌐 VPN Integration Guide for Production Websites

This guide helps AI systems and developers integrate the VPN solution into production websites for real IP changing functionality.

## 🎯 Production Integration Options

### Option 1: Server-Side Integration (Recommended for Real IP Change)
**Best for:** Actual IP changing on all website pages
**Requirements:** Server access, Python backend

```python
# Backend integration example
from unified_vpn import UNIFIED_STATE, connect_real_vpn, get_current_ip

# Check if VPN can change IP for real
def can_change_ip():
    return {
        'real_vpn': True,      # Actually changes server IP
        'proxy_modes': False   # Only routes specific requests
    }

# Integrate VPN into your web app
def integrate_vpn_backend():
    # This will change the server's IP for all requests
    success, message = connect_real_vpn('usa_real')
    return {
        'success': success,
        'message': message,
        'new_ip': get_current_ip(),
        'affects_all_pages': True
    }
```

### Option 2: Client-Side Proxy (Limited IP Change)
**Best for:** Browser-based proxy routing
**Limitations:** Only affects requests made through the proxy

```javascript
// Frontend integration example
class VPNIntegration {
    constructor() {
        this.baseUrl = 'http://your-vpn-server.com:8080';
        this.proxyActive = false;
    }
    
    // Route requests through VPN proxy
    async makeProxiedRequest(url) {
        if (this.proxyActive) {
            return fetch(`${this.baseUrl}/proxy/${encodeURIComponent(url)}`);
        }
        return fetch(url);
    }
    
    // Connect to VPN
    async connect(serverKey = 'cloudflare_warp') {
        const response = await fetch(`${this.baseUrl}/api/unified/connect/${serverKey}`, {
            method: 'POST'
        });
        const result = await response.json();
        this.proxyActive = result.success;
        return result;
    }
}
```

## 🔧 Production Deployment Commands

### For Real IP Change (Server-Level)
```bash
# 1. Install on production server
git clone https://github.com/Jabsama/FREE-VPN.git
cd FREE-VPN

# 2. Install dependencies
pip install -r requirements_api.txt

# 3. Install OpenVPN (for real IP change)
# Ubuntu/Debian:
sudo apt update && sudo apt install openvpn

# CentOS/RHEL:
sudo yum install openvpn

# 4. Run with production WSGI server
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8080 unified_vpn:app

# 5. Setup reverse proxy (nginx example)
# /etc/nginx/sites-available/vpn
server {
    listen 80;
    server_name your-domain.com;
    
    location /vpn/ {
        proxy_pass http://127.0.0.1:8080/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### For Browser Proxy (Client-Level)
```bash
# Simpler deployment - no OpenVPN needed
python unified_vpn.py

# Or with Docker
docker run -p 8080:8080 -v $(pwd):/app python:3.9 python /app/unified_vpn.py
```

## 🌐 Website Integration Examples

### WordPress Integration
```php
<?php
// wp-content/themes/your-theme/vpn-integration.php

class VPNIntegration {
    private $vpn_server = 'http://localhost:8080';
    
    public function connect_vpn($server = 'usa_real') {
        $response = wp_remote_post($this->vpn_server . '/api/unified/connect/' . $server);
        return json_decode(wp_remote_retrieve_body($response), true);
    }
    
    public function get_vpn_status() {
        $response = wp_remote_get($this->vpn_server . '/api/unified/status');
        return json_decode(wp_remote_retrieve_body($response), true);
    }
    
    public function proxy_request($url) {
        $proxy_url = $this->vpn_server . '/proxy/' . urlencode($url);
        return wp_remote_get($proxy_url);
    }
}

// Usage in theme
$vpn = new VPNIntegration();
$status = $vpn->get_vpn_status();
if (!$status['connected']) {
    $vpn->connect_vpn('cloudflare_warp');
}
?>
```

### React/Next.js Integration
```javascript
// components/VPNProvider.js
import { createContext, useContext, useState, useEffect } from 'react';

const VPNContext = createContext();

export function VPNProvider({ children }) {
    const [vpnStatus, setVpnStatus] = useState(null);
    const [isConnected, setIsConnected] = useState(false);
    
    const vpnApi = {
        baseUrl: process.env.NEXT_PUBLIC_VPN_SERVER || 'http://localhost:8080',
        
        async connect(serverKey = 'cloudflare_warp') {
            const response = await fetch(`${this.baseUrl}/api/unified/connect/${serverKey}`, {
                method: 'POST'
            });
            const result = await response.json();
            setIsConnected(result.success);
            return result;
        },
        
        async getStatus() {
            const response = await fetch(`${this.baseUrl}/api/unified/status`);
            const status = await response.json();
            setVpnStatus(status);
            setIsConnected(status.connected);
            return status;
        },
        
        async proxyFetch(url, options = {}) {
            if (isConnected) {
                const proxyUrl = `${this.baseUrl}/proxy/${encodeURIComponent(url)}`;
                return fetch(proxyUrl, options);
            }
            return fetch(url, options);
        }
    };
    
    useEffect(() => {
        vpnApi.getStatus();
        const interval = setInterval(vpnApi.getStatus, 30000);
        return () => clearInterval(interval);
    }, []);
    
    return (
        <VPNContext.Provider value={{ vpnApi, vpnStatus, isConnected }}>
            {children}
        </VPNContext.Provider>
    );
}

export const useVPN = () => useContext(VPNContext);
```

### Django Integration
```python
# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json

VPN_SERVER = 'http://localhost:8080'

@csrf_exempt
def vpn_connect(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        server_key = data.get('server', 'cloudflare_warp')
        
        response = requests.post(f'{VPN_SERVER}/api/unified/connect/{server_key}')
        return JsonResponse(response.json())

def vpn_status(request):
    response = requests.get(f'{VPN_SERVER}/api/unified/status')
    return JsonResponse(response.json())

def proxy_view(request):
    url = request.GET.get('url')
    if url:
        proxy_response = requests.get(f'{VPN_SERVER}/proxy/{url}')
        return JsonResponse({
            'content': proxy_response.text,
            'status': proxy_response.status_code
        })
```

## 🚀 AI Implementation Commands

### For AI Systems Deploying This
```bash
# 1. Quick deployment check
curl -X GET http://localhost:8080/api/unified/status

# 2. Test VPN connection
curl -X POST http://localhost:8080/api/unified/connect/cloudflare_warp

# 3. Verify IP change
curl -X GET http://localhost:8080/proxy/api.ipify.org?format=json

# 4. Health check endpoint
curl -X GET http://localhost:8080/api/unified/servers

# 5. Disconnect when done
curl -X POST http://localhost:8080/api/unified/disconnect
```

### Production Compatibility Check
```python
# compatibility_check.py
import requests
import subprocess
import sys

def check_production_compatibility():
    checks = {
        'python_version': sys.version_info >= (3, 7),
        'flask_available': False,
        'requests_available': False,
        'openvpn_available': False,
        'admin_rights': False
    }
    
    try:
        import flask
        checks['flask_available'] = True
    except ImportError:
        pass
    
    try:
        import requests
        checks['requests_available'] = True
    except ImportError:
        pass
    
    try:
        subprocess.run(['openvpn', '--version'], capture_output=True, check=True)
        checks['openvpn_available'] = True
    except:
        pass
    
    # Check admin rights (simplified)
    try:
        with open('/etc/test', 'w') as f:
            f.write('test')
        checks['admin_rights'] = True
    except:
        pass
    
    return checks

# Recommend best mode based on capabilities
def recommend_vpn_mode(checks):
    if checks['openvpn_available'] and checks['admin_rights']:
        return 'real'  # Can actually change IP
    elif checks['flask_available'] and checks['requests_available']:
        return 'zero'  # Browser proxy mode
    else:
        return 'demo'  # Simulation only

if __name__ == '__main__':
    compatibility = check_production_compatibility()
    recommended_mode = recommend_vpn_mode(compatibility)
    
    print(f"Production Compatibility: {compatibility}")
    print(f"Recommended VPN Mode: {recommended_mode}")
    print(f"Can Change Real IP: {recommended_mode == 'real'}")
```

## ⚠️ Important Notes for AI Implementation

### Real IP Change Limitations
1. **Server-Side Only**: Real IP change requires server-level VPN installation
2. **Browser Limitations**: Client-side JavaScript cannot change the server's IP
3. **Proxy vs VPN**: Proxy routes specific requests, VPN changes all traffic

### Production Recommendations
1. **For Real IP Change**: Use `real` mode with OpenVPN on server
2. **For Browser Proxy**: Use `zero` or `mobile` modes
3. **For Development**: Use `demo` mode for testing

### Security Considerations
```python
# Production security settings
PRODUCTION_CONFIG = {
    'allowed_origins': ['https://yourdomain.com'],
    'rate_limiting': True,
    'authentication': True,
    'logging': True,
    'ssl_required': True
}
```

## 🎯 Quick Start for AI Systems

```bash
# 1. Clone and setup
git clone https://github.com/Jabsama/FREE-VPN.git && cd FREE-VPN

# 2. Install minimal dependencies
pip install flask flask-cors requests

# 3. Start VPN server
python unified_vpn.py

# 4. Test connection (in another terminal)
curl -X POST http://localhost:8080/api/unified/connect/cloudflare_warp

# 5. Verify it works
curl -X GET http://localhost:8080/api/unified/status
```

**Result**: VPN server running on port 8080, ready for website integration with proxy capabilities for IP routing.
