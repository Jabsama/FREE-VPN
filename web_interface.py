#!/usr/bin/env python3
"""
Flexible VPN Web Interface
Professional web control panel for VPN management
Compatible with website integration via API
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import subprocess
import requests
import json
import os
import threading
import time
from datetime import datetime

app = Flask(__name__)

# VPN Server Configuration
VPN_SERVERS = {
    'china': {
        'name': 'Hong Kong (China)',
        'server': 'hk-01.freevpn.world',
        'flag': '🇨🇳',
        'description': 'Best for WeChat, Bilibili, Chinese services',
        'category': 'asia'
    },
    'singapore': {
        'name': 'Singapore',
        'server': 'sg-01.freevpn.world',
        'flag': '🇸🇬',
        'description': 'Fast Asian connection, low latency',
        'category': 'asia'
    },
    'japan': {
        'name': 'Tokyo, Japan',
        'server': 'jp-01.freevpn.world',
        'flag': '🇯🇵',
        'description': 'Gaming optimized, anime streaming',
        'category': 'asia'
    },
    'korea': {
        'name': 'Seoul, South Korea',
        'server': 'kr-01.freevpn.world',
        'flag': '🇰🇷',
        'description': 'K-pop streaming, Korean services',
        'category': 'asia'
    },
    'taiwan': {
        'name': 'Taiwan',
        'server': 'tw-01.freevpn.world',
        'flag': '🇹🇼',
        'description': 'Chinese services, regional content',
        'category': 'asia'
    },
    'usa_ny': {
        'name': 'New York, USA',
        'server': 'us-ny-01.freevpn.world',
        'flag': '🇺🇸',
        'description': 'Netflix US, East Coast',
        'category': 'americas'
    },
    'usa_la': {
        'name': 'Los Angeles, USA',
        'server': 'us-la-01.freevpn.world',
        'flag': '🇺🇸',
        'description': 'Hollywood content, West Coast',
        'category': 'americas'
    },
    'uk': {
        'name': 'London, UK',
        'server': 'uk-01.freevpn.world',
        'flag': '🇬🇧',
        'description': 'BBC iPlayer, UK content',
        'category': 'europe'
    },
    'germany': {
        'name': 'Frankfurt, Germany',
        'server': 'de-01.freevpn.world',
        'flag': '🇩🇪',
        'description': 'EU privacy laws, central Europe',
        'category': 'europe'
    },
    'france': {
        'name': 'Paris, France',
        'server': 'fr-01.freevpn.world',
        'flag': '🇫🇷',
        'description': 'French content, EU location',
        'category': 'europe'
    },
    'netherlands': {
        'name': 'Netherlands',
        'server': 'nl-01.freevpn.world',
        'flag': '🇳🇱',
        'description': 'Privacy friendly, torrenting',
        'category': 'europe'
    },
    'canada': {
        'name': 'Toronto, Canada',
        'server': 'ca-01.freevpn.world',
        'flag': '🇨🇦',
        'description': 'North America, privacy laws',
        'category': 'americas'
    },
    'australia': {
        'name': 'Sydney, Australia',
        'server': 'au-01.freevpn.world',
        'flag': '🇦🇺',
        'description': 'Oceania region, Australian content',
        'category': 'oceania'
    },
    'brazil': {
        'name': 'São Paulo, Brazil',
        'server': 'br-01.freevpn.world',
        'flag': '🇧🇷',
        'description': 'South America, Portuguese content',
        'category': 'americas'
    },
    'india': {
        'name': 'Mumbai, India',
        'server': 'in-01.freevpn.world',
        'flag': '🇮🇳',
        'description': 'Bollywood, Indian services',
        'category': 'asia'
    }
}

# Global state
current_connection = None
connection_status = 'disconnected'
connection_start_time = None

def get_current_ip():
    """Get current public IP and location"""
    try:
        response = requests.get('https://ipapi.co/json/', timeout=10)
        return response.json()
    except:
        return {'ip': 'Unknown', 'country_name': 'Unknown', 'city': 'Unknown'}

def check_vpn_status():
    """Check if VPN is currently connected"""
    try:
        result = subprocess.run(['powershell', '-Command', 'Get-VpnConnection | Where-Object {$_.ConnectionStatus -eq "Connected"}'], 
                              capture_output=True, text=True, timeout=10)
        return 'connected' if result.stdout.strip() else 'disconnected'
    except:
        return 'disconnected'

def connect_vpn(location_key):
    """Connect to VPN server"""
    global current_connection, connection_status, connection_start_time
    
    if location_key not in VPN_SERVERS:
        return {'success': False, 'message': 'Invalid location'}
    
    server_info = VPN_SERVERS[location_key]
    connection_name = f"FlexibleVPN-{server_info['name']}"
    
    try:
        # Disconnect existing connections
        subprocess.run(['powershell', '-Command', 'Get-VpnConnection | Remove-VpnConnection -Force -ErrorAction SilentlyContinue'], 
                      timeout=10)
        
        # Create new connection
        cmd = f"Add-VpnConnection -Name '{connection_name}' -ServerAddress '{server_info['server']}' -TunnelType 'Automatic' -EncryptionLevel 'Optional' -AuthenticationMethod 'MSChapv2' -Force"
        subprocess.run(['powershell', '-Command', cmd], timeout=10)
        
        # Connect
        result = subprocess.run(['powershell', '-Command', f"rasdial '{connection_name}'"], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            current_connection = location_key
            connection_status = 'connected'
            connection_start_time = datetime.now()
            return {'success': True, 'message': f'Connected to {server_info["name"]}'}
        else:
            return {'success': False, 'message': 'Connection failed'}
            
    except Exception as e:
        return {'success': False, 'message': f'Error: {str(e)}'}

def disconnect_vpn():
    """Disconnect VPN"""
    global current_connection, connection_status, connection_start_time
    
    try:
        subprocess.run(['powershell', '-Command', 'rasdial /disconnect'], timeout=10)
        subprocess.run(['powershell', '-Command', 'Get-VpnConnection | Remove-VpnConnection -Force -ErrorAction SilentlyContinue'], 
                      timeout=10)
        
        current_connection = None
        connection_status = 'disconnected'
        connection_start_time = None
        return {'success': True, 'message': 'VPN disconnected'}
        
    except Exception as e:
        return {'success': False, 'message': f'Error: {str(e)}'}

@app.route('/')
def index():
    """Main web interface"""
    return render_template('index.html', servers=VPN_SERVERS)

@app.route('/api/status')
def api_status():
    """API endpoint for VPN status"""
    ip_info = get_current_ip()
    status = check_vpn_status()
    
    uptime = None
    if connection_start_time and status == 'connected':
        uptime = str(datetime.now() - connection_start_time).split('.')[0]
    
    return jsonify({
        'status': status,
        'current_location': current_connection,
        'ip_address': ip_info.get('ip', 'Unknown'),
        'country': ip_info.get('country_name', 'Unknown'),
        'city': ip_info.get('city', 'Unknown'),
        'uptime': uptime,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/connect', methods=['POST'])
def api_connect():
    """API endpoint to connect VPN"""
    data = request.get_json()
    location = data.get('location')
    
    if not location:
        return jsonify({'success': False, 'message': 'Location required'})
    
    result = connect_vpn(location)
    return jsonify(result)

@app.route('/api/disconnect', methods=['POST'])
def api_disconnect():
    """API endpoint to disconnect VPN"""
    result = disconnect_vpn()
    return jsonify(result)

@app.route('/api/servers')
def api_servers():
    """API endpoint to get available servers"""
    return jsonify(VPN_SERVERS)

@app.route('/api/best-for-bot')
def api_best_for_bot():
    """API endpoint to get best server for bot usage"""
    # Return China/Hong Kong as best for bot usage
    return jsonify({
        'recommended': 'china',
        'server': VPN_SERVERS['china'],
        'reason': 'Best for WeChat, Bilibili, and Chinese bot platforms'
    })

# Website integration endpoints
@app.route('/widget')
def widget():
    """Embeddable widget for websites"""
    return render_template('widget.html')

@app.route('/button')
def button():
    """Simple button for website integration"""
    return render_template('button.html')

if __name__ == '__main__':
    # Create templates directory and files
    os.makedirs('templates', exist_ok=True)
    
    # Create main interface template
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌍 Flexible VPN Control Panel</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: white;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header { text-align: center; margin-bottom: 30px; }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .status-card { 
            background: rgba(255,255,255,0.1); 
            border-radius: 15px; 
            padding: 20px; 
            margin-bottom: 30px;
            backdrop-filter: blur(10px);
        }
        .servers-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
            gap: 20px; 
        }
        .server-card { 
            background: rgba(255,255,255,0.1); 
            border-radius: 15px; 
            padding: 20px; 
            cursor: pointer;
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
        }
        .server-card:hover { 
            background: rgba(255,255,255,0.2); 
            transform: translateY(-5px);
        }
        .server-card.connected { 
            background: rgba(76, 175, 80, 0.3); 
            border: 2px solid #4CAF50;
        }
        .flag { font-size: 2em; margin-bottom: 10px; }
        .server-name { font-size: 1.2em; font-weight: bold; margin-bottom: 5px; }
        .server-desc { opacity: 0.8; font-size: 0.9em; }
        .btn { 
            background: #4CAF50; 
            color: white; 
            border: none; 
            padding: 12px 24px; 
            border-radius: 25px; 
            cursor: pointer; 
            font-size: 1em;
            transition: all 0.3s ease;
        }
        .btn:hover { background: #45a049; transform: scale(1.05); }
        .btn-disconnect { background: #f44336; }
        .btn-disconnect:hover { background: #da190b; }
        .status-indicator { 
            display: inline-block; 
            width: 12px; 
            height: 12px; 
            border-radius: 50%; 
            margin-right: 8px;
        }
        .status-connected { background: #4CAF50; }
        .status-disconnected { background: #f44336; }
        .api-section { 
            margin-top: 40px; 
            background: rgba(255,255,255,0.1); 
            border-radius: 15px; 
            padding: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌍 Flexible VPN Control Panel</h1>
            <p>Professional VPN solution with global server network</p>
        </div>
        
        <div class="status-card">
            <h3>Connection Status</h3>
            <div id="status-info">
                <span class="status-indicator status-disconnected"></span>
                <span id="status-text">Disconnected</span>
            </div>
            <div id="connection-details" style="margin-top: 10px; opacity: 0.8;"></div>
            <button id="disconnect-btn" class="btn btn-disconnect" style="margin-top: 15px; display: none;">Disconnect</button>
        </div>
        
        <div class="servers-grid" id="servers-grid">
            <!-- Servers will be loaded here -->
        </div>
        
        <div class="api-section">
            <h3>🔗 Website Integration</h3>
            <p>Integrate this VPN into your website:</p>
            <div style="margin-top: 15px;">
                <button class="btn" onclick="window.open('/widget', '_blank')">📱 Get Widget Code</button>
                <button class="btn" onclick="window.open('/button', '_blank')">🔘 Get Button Code</button>
            </div>
            <div style="margin-top: 15px; font-family: monospace; background: rgba(0,0,0,0.3); padding: 15px; border-radius: 10px;">
                <strong>API Endpoints:</strong><br>
                GET /api/status - Get VPN status<br>
                POST /api/connect - Connect to location<br>
                POST /api/disconnect - Disconnect VPN<br>
                GET /api/servers - Get server list
            </div>
        </div>
    </div>

    <script>
        let currentStatus = 'disconnected';
        
        async function loadServers() {
            try {
                const response = await fetch('/api/servers');
                const servers = await response.json();
                const grid = document.getElementById('servers-grid');
                
                grid.innerHTML = '';
                
                Object.entries(servers).forEach(([key, server]) => {
                    const card = document.createElement('div');
                    card.className = 'server-card';
                    card.innerHTML = `
                        <div class="flag">${server.flag}</div>
                        <div class="server-name">${server.name}</div>
                        <div class="server-desc">${server.description}</div>
                    `;
                    card.onclick = () => connectToServer(key);
                    grid.appendChild(card);
                });
            } catch (error) {
                console.error('Error loading servers:', error);
            }
        }
        
        async function updateStatus() {
            try {
                const response = await fetch('/api/status');
                const status = await response.json();
                
                const indicator = document.querySelector('.status-indicator');
                const statusText = document.getElementById('status-text');
                const details = document.getElementById('connection-details');
                const disconnectBtn = document.getElementById('disconnect-btn');
                
                if (status.status === 'connected') {
                    indicator.className = 'status-indicator status-connected';
                    statusText.textContent = 'Connected';
                    details.innerHTML = `
                        📍 Location: ${status.country}, ${status.city}<br>
                        🌐 IP Address: ${status.ip_address}<br>
                        ⏱️ Uptime: ${status.uptime || 'Unknown'}
                    `;
                    disconnectBtn.style.display = 'inline-block';
                    
                    // Highlight connected server
                    document.querySelectorAll('.server-card').forEach(card => {
                        card.classList.remove('connected');
                    });
                    
                } else {
                    indicator.className = 'status-indicator status-disconnected';
                    statusText.textContent = 'Disconnected';
                    details.innerHTML = `🌐 IP Address: ${status.ip_address}<br>📍 Location: ${status.country}`;
                    disconnectBtn.style.display = 'none';
                }
                
                currentStatus = status.status;
                
            } catch (error) {
                console.error('Error updating status:', error);
            }
        }
        
        async function connectToServer(location) {
            if (currentStatus === 'connected') {
                if (!confirm('Disconnect current connection and connect to new server?')) {
                    return;
                }
            }
            
            try {
                const response = await fetch('/api/connect', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ location: location })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    alert('✅ ' + result.message);
                    updateStatus();
                } else {
                    alert('❌ ' + result.message);
                }
                
            } catch (error) {
                alert('❌ Connection error: ' + error.message);
            }
        }
        
        async function disconnect() {
            try {
                const response = await fetch('/api/disconnect', {
                    method: 'POST'
                });
                
                const result = await response.json();
                
                if (result.success) {
                    alert('✅ ' + result.message);
                    updateStatus();
                } else {
                    alert('❌ ' + result.message);
                }
                
            } catch (error) {
                alert('❌ Disconnect error: ' + error.message);
            }
        }
        
        document.getElementById('disconnect-btn').onclick = disconnect;
        
        // Initialize
        loadServers();
        updateStatus();
        
        // Update status every 10 seconds
        setInterval(updateStatus, 10000);
    </script>
</body>
</html>''')
    
    # Create widget template
    with open('templates/widget.html', 'w', encoding='utf-8') as f:
        f.write('''<!DOCTYPE html>
<html>
<head>
    <title>VPN Widget Code</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        .code-block { background: #f4f4f4; padding: 15px; border-radius: 5px; margin: 10px 0; }
        pre { white-space: pre-wrap; word-wrap: break-word; }
    </style>
</head>
<body>
    <h2>🔗 Website Integration Code</h2>
    
    <h3>Embeddable Widget (iframe)</h3>
    <div class="code-block">
        <pre>&lt;iframe src="http://localhost:8080/widget" width="400" height="300" frameborder="0"&gt;&lt;/iframe&gt;</pre>
    </div>
    
    <h3>JavaScript API Integration</h3>
    <div class="code-block">
        <pre>// Connect to VPN
fetch('http://localhost:8080/api/connect', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ location: 'china' })
})
.then(response => response.json())
.then(data => console.log(data));

// Check status
fetch('http://localhost:8080/api/status')
.then(response => response.json())
.then(data => console.log(data));</pre>
    </div>
    
    <h3>Simple Button Integration</h3>
    <div class="code-block">
        <pre>&lt;button onclick="activateVPN()"&gt;🇨🇳 Activate China VPN&lt;/button&gt;

&lt;script&gt;
function activateVPN() {
    fetch('http://localhost:8080/api/connect', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ location: 'china' })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('✅ VPN Connected!');
        } else {
            alert('❌ Connection failed: ' + data.message);
        }
    });
}
&lt;/script&gt;</pre>
    </div>
</body>
</html>''')
    
    # Create button template
    with open('templates/button.html', 'w', encoding='utf-8') as f:
        f.write('''<!DOCTYPE html>
<html>
<head>
    <title>VPN Button</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; text-align: center; }
        .vpn-btn { 
            background: linear-gradient(45deg, #4CAF50, #45a049);
            color: white; 
            border: none; 
            padding: 15px 30px; 
            font-size: 18px; 
            border-radius: 25px; 
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        }
        .vpn-btn:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,0.3); }
    </style>
</head>
<body>
    <h2>🔘 VPN Activation Button</h2>
    <p>Copy this code to your website:</p>
    
    <button class="vpn-btn" onclick="activateVPN()">🇨🇳 Activate China VPN for Bots</button>
    
    <div style="margin-top: 30px; text-align: left; background: #f4f4f4; padding: 15px; border-radius: 5px;">
        <strong>HTML + JavaScript Code:</strong>
        <pre>&lt;button class="vpn-btn" onclick="activateVPN()"&gt;🇨🇳 Activate China VPN&lt;/button&gt;

&lt;style&gt;
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
&lt;/style&gt;

&lt;script&gt;
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
    })
    .catch(error => {
        alert('❌ Error: ' + error.message);
    });
}
&lt;/script&gt;</pre>
    </div>
    
    <script>
        function activateVPN() {
            fetch('/api/connect', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ location: 'china' })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('✅ China VPN Activated!');
                } else {
                    alert('❌ Connection failed: ' + data.message);
                }
            });
        }
    </script>
</body>
</html>''')
    
    print("🌐 Starting Flexible VPN Web Interface...")
    print("📱 Access at: http://localhost:8080")
    print("🔗 Widget: http://localhost:8080/widget")
    print("🔘 Button: http://localhost:8080/button")
    print("📡 API: http://localhost:8080/api/status")
    
    app.run(host='0.0.0.0', port=8080, debug=False)
