#!/usr/bin/env python3
"""
Mobile VPN Solution - Optimized for mobile devices
Provides VPN functionality accessible from mobile browsers
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import requests
import json
import time
from datetime import datetime
import socket

app = Flask(__name__)
CORS(app)

# Mobile-optimized VPN state
MOBILE_VPN_STATE = {
    'connected': False,
    'connecting': False,
    'current_server': None,
    'connection_start_time': None,
    'user_ip': None,
    'proxy_active': False
}

# Mobile-friendly VPN servers (proxy-based for mobile compatibility)
MOBILE_VPN_SERVERS = {
    'usa_mobile': {
        'name': 'USA Mobile Server',
        'flag': '🇺🇸',
        'proxy_host': 'us-proxy.vpngate.net',
        'proxy_port': 8080,
        'type': 'http_proxy',
        'mobile_compatible': True
    },
    'uk_mobile': {
        'name': 'UK Mobile Server',
        'flag': '🇬🇧',
        'proxy_host': 'uk-proxy.vpngate.net',
        'proxy_port': 8080,
        'type': 'http_proxy',
        'mobile_compatible': True
    },
    'japan_mobile': {
        'name': 'Japan Mobile Server',
        'flag': '🇯🇵',
        'proxy_host': 'jp-proxy.vpngate.net',
        'proxy_port': 8080,
        'type': 'http_proxy',
        'mobile_compatible': True
    }
}

def get_current_ip():
    """Get current public IP"""
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=10)
        return response.json()['ip']
    except:
        return 'Unknown'

def get_server_ip():
    """Automatically detect server IP address"""
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        external_ip = response.json()['ip']
        return external_ip
    except:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except:
            return "localhost"

def simulate_mobile_vpn_connection(server_key):
    """Simulate VPN connection for mobile (proxy-based)"""
    try:
        server = MOBILE_VPN_SERVERS[server_key]
        
        # Simulate connection process
        time.sleep(2)
        
        # For mobile, we simulate the connection since real VPN requires root/admin
        MOBILE_VPN_STATE['proxy_active'] = True
        
        return True, f"Mobile VPN connected to {server['name']} (proxy mode)"
        
    except Exception as e:
        return False, str(e)

def disconnect_mobile_vpn():
    """Disconnect mobile VPN"""
    try:
        MOBILE_VPN_STATE['proxy_active'] = False
        time.sleep(1)
        return True, "Mobile VPN disconnected"
    except Exception as e:
        return False, str(e)

# API Endpoints
@app.route('/api/mobile/status', methods=['GET'])
def mobile_api_status():
    """Get mobile VPN status"""
    current_ip = get_current_ip()
    
    return jsonify({
        'connected': MOBILE_VPN_STATE['connected'],
        'connecting': MOBILE_VPN_STATE['connecting'],
        'current_server': MOBILE_VPN_STATE['current_server'],
        'current_ip': current_ip,
        'proxy_active': MOBILE_VPN_STATE['proxy_active'],
        'mobile_mode': True,
        'connection_time': MOBILE_VPN_STATE['connection_start_time'].isoformat() if MOBILE_VPN_STATE['connection_start_time'] else None,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/mobile/servers', methods=['GET'])
def mobile_api_servers():
    """Get mobile-compatible servers"""
    return jsonify({
        'servers': MOBILE_VPN_SERVERS,
        'total_servers': len(MOBILE_VPN_SERVERS),
        'mobile_optimized': True,
        'last_updated': datetime.now().isoformat()
    })

@app.route('/api/mobile/connect/<server_key>', methods=['POST'])
def mobile_api_connect(server_key):
    """Connect to mobile VPN server"""
    if MOBILE_VPN_STATE['connecting']:
        return jsonify({'success': False, 'message': 'Connection already in progress'}), 400
    
    if server_key not in MOBILE_VPN_SERVERS:
        return jsonify({'success': False, 'message': f'Server {server_key} not available'}), 404
    
    if MOBILE_VPN_STATE['connected']:
        return jsonify({'success': False, 'message': 'Already connected. Disconnect first.'}), 400
    
    MOBILE_VPN_STATE['connecting'] = True
    
    try:
        success, message = simulate_mobile_vpn_connection(server_key)
        
        if success:
            MOBILE_VPN_STATE['connected'] = True
            MOBILE_VPN_STATE['current_server'] = server_key
            MOBILE_VPN_STATE['connection_start_time'] = datetime.now()
            
            return jsonify({
                'success': True,
                'message': message,
                'server': MOBILE_VPN_SERVERS[server_key],
                'mobile_mode': True,
                'connection_time': datetime.now().isoformat()
            })
        else:
            return jsonify({'success': False, 'message': message}), 500
            
    finally:
        MOBILE_VPN_STATE['connecting'] = False

@app.route('/api/mobile/disconnect', methods=['POST'])
def mobile_api_disconnect():
    """Disconnect mobile VPN"""
    if not MOBILE_VPN_STATE['connected']:
        return jsonify({'success': False, 'message': 'Not connected'}), 400
    
    try:
        success, message = disconnect_mobile_vpn()
        
        if success:
            MOBILE_VPN_STATE['connected'] = False
            MOBILE_VPN_STATE['current_server'] = None
            MOBILE_VPN_STATE['connection_start_time'] = None
            
            return jsonify({
                'success': True,
                'message': message,
                'mobile_mode': True,
                'disconnection_time': datetime.now().isoformat()
            })
        else:
            return jsonify({'success': False, 'message': message}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/mobile')
def mobile_dashboard():
    """Mobile-optimized dashboard"""
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>📱 Mobile VPN</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
            padding: 10px;
            font-size: 16px;
        }
        .container { max-width: 100%; margin: 0 auto; }
        .header { text-align: center; margin-bottom: 20px; padding: 20px 0; }
        .card { 
            background: rgba(255,255,255,0.15);
            border-radius: 20px;
            padding: 20px;
            margin: 15px 0;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }
        .status { 
            font-size: 1.4em;
            margin: 15px 0;
            text-align: center;
            padding: 15px;
            border-radius: 15px;
            background: rgba(255,255,255,0.1);
        }
        .connected { background: rgba(76, 175, 80, 0.3); }
        .disconnected { background: rgba(244, 67, 54, 0.3); }
        .btn { 
            background: #4CAF50;
            color: white;
            border: none;
            padding: 15px 25px;
            border-radius: 25px;
            cursor: pointer;
            margin: 8px;
            font-size: 16px;
            width: 100%;
            max-width: 300px;
            display: block;
            margin: 10px auto;
            touch-action: manipulation;
        }
        .btn:hover, .btn:active { background: #45a049; transform: scale(0.98); }
        .btn-danger { background: #f44336; }
        .btn-danger:hover, .btn-danger:active { background: #d32f2f; }
        .server-item {
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 15px;
            margin: 10px 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .server-info { flex: 1; }
        .server-btn { 
            background: #2196F3;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 14px;
        }
        .ip-info {
            background: rgba(0,0,0,0.2);
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
            font-family: monospace;
            font-size: 14px;
        }
        .warning {
            background: rgba(255, 193, 7, 0.3);
            border-radius: 10px;
            padding: 15px;
            margin: 15px 0;
            border-left: 4px solid #FFC107;
        }
        @media (max-width: 480px) {
            body { font-size: 14px; padding: 5px; }
            .card { padding: 15px; margin: 10px 0; }
            .btn { padding: 12px 20px; font-size: 14px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📱 Mobile VPN</h1>
            <p>VPN optimisé pour mobile</p>
        </div>
        
        <div class="warning">
            <strong>⚠️ Limitation Mobile</strong><br>
            Les navigateurs mobiles ne peuvent pas installer de vrais VPN. Cette solution utilise un proxy HTTP pour simuler un VPN.
        </div>
        
        <div class="card">
            <h2>📊 Statut</h2>
            <div id="status" class="status">Chargement...</div>
            <div id="ip-info" class="ip-info"></div>
        </div>
        
        <div class="card">
            <h2>🌍 Serveurs Mobiles</h2>
            <div id="servers">Chargement...</div>
        </div>
        
        <div class="card">
            <h2>🎛️ Contrôles</h2>
            <button class="btn" onclick="refreshStatus()">🔄 Actualiser</button>
            <button class="btn btn-danger" onclick="disconnect()">🔌 Déconnecter</button>
        </div>
        
        <div class="card">
            <h2>📱 Compatibilité Mobile</h2>
            <p><strong>✅ Fonctionne sur :</strong></p>
            <ul style="margin: 10px 0; padding-left: 20px;">
                <li>Safari (iOS)</li>
                <li>Chrome (Android)</li>
                <li>Firefox Mobile</li>
                <li>Edge Mobile</li>
            </ul>
            <p><strong>⚠️ Limitations :</strong></p>
            <ul style="margin: 10px 0; padding-left: 20px;">
                <li>Proxy HTTP seulement (pas de vrai VPN)</li>
                <li>Pas de changement d'IP réel</li>
                <li>Nécessite configuration manuelle du proxy</li>
            </ul>
        </div>
    </div>

    <script>
        async function refreshStatus() {
            try {
                const response = await fetch('/api/mobile/status');
                const data = await response.json();
                
                const statusEl = document.getElementById('status');
                const ipEl = document.getElementById('ip-info');
                
                if (data.connected) {
                    statusEl.innerHTML = `✅ Connecté à ${data.current_server}`;
                    statusEl.className = 'status connected';
                    ipEl.innerHTML = `
                        <strong>IP Actuelle:</strong> ${data.current_ip}<br>
                        <strong>Mode:</strong> Mobile Proxy<br>
                        <strong>Connecté depuis:</strong> ${new Date(data.connection_time).toLocaleString()}
                    `;
                } else if (data.connecting) {
                    statusEl.innerHTML = `🔄 Connexion...`;
                    statusEl.className = 'status';
                    ipEl.innerHTML = `<strong>IP Actuelle:</strong> ${data.current_ip}`;
                } else {
                    statusEl.innerHTML = `❌ Déconnecté`;
                    statusEl.className = 'status disconnected';
                    ipEl.innerHTML = `<strong>IP Actuelle:</strong> ${data.current_ip}`;
                }
            } catch (error) {
                document.getElementById('status').innerHTML = `❌ Erreur: ${error.message}`;
            }
        }
        
        async function loadServers() {
            try {
                const response = await fetch('/api/mobile/servers');
                const data = await response.json();
                
                const serversEl = document.getElementById('servers');
                serversEl.innerHTML = '';
                
                Object.entries(data.servers).forEach(([key, server]) => {
                    const serverDiv = document.createElement('div');
                    serverDiv.className = 'server-item';
                    serverDiv.innerHTML = `
                        <div class="server-info">
                            <strong>${server.flag} ${server.name}</strong><br>
                            <small>Proxy HTTP - Mobile Compatible</small>
                        </div>
                        <button class="server-btn" onclick="connect('${key}')">Connecter</button>
                    `;
                    serversEl.appendChild(serverDiv);
                });
            } catch (error) {
                document.getElementById('servers').innerHTML = `Erreur: ${error.message}`;
            }
        }
        
        async function connect(serverKey) {
            try {
                const response = await fetch(`/api/mobile/connect/${serverKey}`, { method: 'POST' });
                const data = await response.json();
                
                if (data.success) {
                    alert('✅ ' + data.message);
                } else {
                    alert('❌ ' + data.message);
                }
                
                refreshStatus();
            } catch (error) {
                alert('❌ Erreur de connexion: ' + error.message);
            }
        }
        
        async function disconnect() {
            try {
                const response = await fetch('/api/mobile/disconnect', { method: 'POST' });
                const data = await response.json();
                
                if (data.success) {
                    alert('✅ ' + data.message);
                } else {
                    alert('❌ ' + data.message);
                }
                
                refreshStatus();
            } catch (error) {
                alert('❌ Erreur de déconnexion: ' + error.message);
            }
        }
        
        // Initialisation
        refreshStatus();
        loadServers();
        
        // Auto-actualisation toutes les 15 secondes
        setInterval(refreshStatus, 15000);
        
        // Optimisation tactile
        document.addEventListener('touchstart', function() {}, true);
    </script>
</body>
</html>
    ''')

@app.route('/')
def main_dashboard():
    """Main dashboard with mobile detection"""
    user_agent = request.headers.get('User-Agent', '').lower()
    is_mobile = any(mobile in user_agent for mobile in ['mobile', 'android', 'iphone', 'ipad'])
    
    if is_mobile:
        return mobile_dashboard()
    else:
        return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>🌐 VPN Multi-Platform</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; margin: 0; padding: 20px; }
        .container { max-width: 800px; margin: 0 auto; text-align: center; }
        .card { background: rgba(255,255,255,0.1); border-radius: 15px; padding: 20px; margin: 20px 0; backdrop-filter: blur(10px); }
        .btn { background: #4CAF50; color: white; border: none; padding: 15px 30px; border-radius: 25px; cursor: pointer; margin: 10px; font-size: 16px; text-decoration: none; display: inline-block; }
        .btn:hover { background: #45a049; }
        .btn-mobile { background: #2196F3; }
        .btn-mobile:hover { background: #1976D2; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌐 VPN Multi-Platform</h1>
        <p>Choisissez votre plateforme</p>
        
        <div class="card">
            <h2>💻 Desktop / Ordinateur</h2>
            <p>VPN complet avec OpenVPN - Navigation internet réelle</p>
            <a href="/desktop" class="btn">🖥️ Version Desktop</a>
        </div>
        
        <div class="card">
            <h2>📱 Mobile / Tablette</h2>
            <p>Version optimisée mobile - Proxy HTTP</p>
            <a href="/mobile" class="btn btn-mobile">📱 Version Mobile</a>
        </div>
        
        <div class="card">
            <h2>⚠️ Différences importantes</h2>
            <table style="width: 100%; text-align: left; margin: 20px 0;">
                <tr style="background: rgba(255,255,255,0.1);">
                    <th style="padding: 10px;">Fonctionnalité</th>
                    <th style="padding: 10px;">Desktop</th>
                    <th style="padding: 10px;">Mobile</th>
                </tr>
                <tr>
                    <td style="padding: 10px;">Navigation internet réelle</td>
                    <td style="padding: 10px;">✅ Oui</td>
                    <td style="padding: 10px;">❌ Simulation</td>
                </tr>
                <tr style="background: rgba(255,255,255,0.05);">
                    <td style="padding: 10px;">Changement d'IP</td>
                    <td style="padding: 10px;">✅ Réel</td>
                    <td style="padding: 10px;">❌ Simulé</td>
                </tr>
                <tr>
                    <td style="padding: 10px;">Installation requise</td>
                    <td style="padding: 10px;">🟡 OpenVPN</td>
                    <td style="padding: 10px;">✅ Aucune</td>
                </tr>
                <tr style="background: rgba(255,255,255,0.05);">
                    <td style="padding: 10px;">Facilité d'utilisation</td>
                    <td style="padding: 10px;">🟡 Moyenne</td>
                    <td style="padding: 10px;">✅ Facile</td>
                </tr>
            </table>
        </div>
    </div>
</body>
</html>
        ''')

if __name__ == '__main__':
    SERVER_PORT = 8080
    detected_ip = get_server_ip()
    
    print("📱 Starting Mobile VPN Solution...")
    print(f"📡 Available at: http://{detected_ip}:{SERVER_PORT}")
    print(f"📱 Mobile interface: http://{detected_ip}:{SERVER_PORT}/mobile")
    print()
    print("📱 Mobile Compatibility:")
    print("   • iOS Safari: ✅ Compatible")
    print("   • Android Chrome: ✅ Compatible")
    print("   • Mobile browsers: ✅ Compatible")
    print("   • Real VPN: ❌ Limited (proxy only)")
    print()
    print("⚠️ Mobile Limitations:")
    print("   • No real VPN (browser security)")
    print("   • HTTP proxy simulation only")
    print("   • No IP address change")
    print("   • Manual proxy configuration needed")
    print()
    
    app.run(host='0.0.0.0', port=SERVER_PORT, debug=False)
