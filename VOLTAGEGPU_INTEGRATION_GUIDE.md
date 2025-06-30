# 🛡️ VoltageGPU VPN Integration Guide

## Overview
This guide shows how to integrate the FREE VPN dashboard directly into your voltagegpu.com website, allowing users to control VPN connections from your site.

## 🚀 Quick Integration

### Step 1: Start the VPN Server
```bash
python vpn.py
```
The VPN server will run on `http://localhost:8080` with API endpoints available.

### Step 2: Add VPN Widget to Your Website
Include the VPN widget script in your HTML:

```html
<!-- Add this to your HTML head -->
<script src="https://your-domain.com/vpn_widget.js"></script>

<!-- Add this container where you want the VPN dashboard -->
<div id="vpn-widget"></div>
```

### Step 3: Automatic Initialization
The widget automatically initializes when the page loads and connects to your local VPN server.

## 🔧 Advanced Configuration

### Custom Configuration
```javascript
// Custom widget configuration
const vpnWidget = new VoltageVPNWidget({
    apiUrl: 'http://localhost:8080/api',  // VPN server API
    containerId: 'my-vpn-container',      // Custom container ID
    autoRefresh: true,                    // Auto-refresh status
    refreshInterval: 3000                 // Refresh every 3 seconds
});
```

### Multiple Widgets
```javascript
// Dashboard widget
const dashboardVPN = new VoltageVPNWidget({
    containerId: 'dashboard-vpn',
    autoRefresh: true
});

// Sidebar widget (minimal)
const sidebarVPN = new VoltageVPNWidget({
    containerId: 'sidebar-vpn',
    autoRefresh: false
});
```

## 📡 API Endpoints

The VPN server provides these API endpoints:

### Status
```
GET /api/status
```
Returns current VPN connection status and IP information.

### Servers
```
GET /api/servers
```
Returns list of available VPN servers.

### Connect
```
POST /api/connect/{server_id}
```
Connect to a specific VPN server.

### Disconnect
```
POST /api/disconnect
```
Disconnect from VPN.

## 🌍 Server Integration

### For voltagegpu.com Integration

1. **Upload Files to Your Server:**
   - `vpn_widget.js` - The VPN widget script
   - `voltagegpu_vpn_demo.html` - Demo page (optional)

2. **Add to Your Existing Pages:**
   ```html
   <!-- In your dashboard page -->
   <div class="vpn-section">
       <h2>🛡️ VPN Protection</h2>
       <div id="vpn-widget"></div>
   </div>
   
   <script src="/assets/js/vpn_widget.js"></script>
   ```

3. **Styling Integration:**
   The widget includes its own CSS, but you can customize it:
   ```css
   .voltage-vpn-widget {
       /* Your custom styles */
       background: your-brand-color;
       border-radius: your-border-radius;
   }
   ```

## 🔒 Security Considerations

### CORS Configuration
If running on different domains, configure CORS in your VPN server:

```python
# In vpn.py, add CORS headers
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=['https://voltagegpu.com'])
```

### HTTPS Support
For production, ensure your VPN server supports HTTPS:
```bash
# Run with SSL certificate
python vpn.py --ssl --cert=cert.pem --key=key.pem
```

## 📱 Mobile Support

The widget is fully responsive and works on:
- ✅ Desktop browsers
- ✅ Mobile browsers (iOS Safari, Android Chrome)
- ✅ Tablets
- ✅ Progressive Web Apps

## 🎨 Customization Examples

### VoltageGPU Theme Integration
```css
.voltage-vpn-widget {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 15px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}

.server-card {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
}
```

### Minimal Integration
```html
<!-- Minimal VPN status indicator -->
<div id="vpn-status-mini"></div>

<script>
const miniVPN = new VoltageVPNWidget({
    containerId: 'vpn-status-mini',
    minimal: true  // Show only status
});
</script>
```

## 🚀 Production Deployment

### 1. Server Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run VPN server
python vpn.py --host=0.0.0.0 --port=8080
```

### 2. Reverse Proxy (Nginx)
```nginx
location /vpn/ {
    proxy_pass http://localhost:8080/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

### 3. Process Management (PM2)
```bash
# Install PM2
npm install -g pm2

# Start VPN server with PM2
pm2 start vpn.py --name "voltage-vpn" --interpreter python3
```

## 🔧 Troubleshooting

### Common Issues

1. **Widget not loading:**
   - Check if VPN server is running
   - Verify API URL in widget configuration
   - Check browser console for errors

2. **CORS errors:**
   - Add your domain to CORS origins
   - Ensure proper headers are set

3. **Connection failures:**
   - Verify VPN server is accessible
   - Check firewall settings
   - Ensure proper network configuration

### Debug Mode
```javascript
const vpnWidget = new VoltageVPNWidget({
    debug: true,  // Enable debug logging
    apiUrl: 'http://localhost:8080/api'
});
```

## 📊 Analytics Integration

Track VPN usage on your site:
```javascript
// Google Analytics example
voltageVPN.on('connect', (server) => {
    gtag('event', 'vpn_connect', {
        'server_location': server.location,
        'server_id': server.id
    });
});

voltageVPN.on('disconnect', () => {
    gtag('event', 'vpn_disconnect');
});
```

## 🎯 Use Cases for VoltageGPU

1. **GPU Rental Security:** Protect users when accessing remote GPU instances
2. **Privacy Protection:** Secure connections to GPU computing resources
3. **Geo-restriction Bypass:** Access GPU services from restricted regions
4. **Enhanced Security:** Add VPN layer to GPU cloud computing

## 📞 Support

For integration support:
- 📧 Email: support@voltagegpu.com
- 💬 Discord: VoltageGPU Community
- 📖 Documentation: https://docs.voltagegpu.com/vpn

## 🔄 Updates

The VPN widget auto-updates its status every 5 seconds by default. You can customize this:

```javascript
const vpnWidget = new VoltageVPNWidget({
    refreshInterval: 2000  // Update every 2 seconds
});
```

---

**Ready to integrate?** Start with the demo page and customize it for your needs!
