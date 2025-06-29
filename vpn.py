#!/usr/bin/env python3
"""
FREE VPN - Open Source VPN Solution
Professional VPN service that works without OpenVPN dependency
GitHub: https://github.com/Jabsama/FREE-VPN
"""

import sys
import os
import json
import time
import threading
import subprocess
import requests
import socket
import random
from datetime import datetime
from pathlib import Path

# Import autonomous VPN module
from vpn_core import AutonomousVPN

try:
    from flask import Flask, request, jsonify, render_template_string
    from flask_cors import CORS
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    print("⚠️  Flask not installed. Install with: pip install flask flask-cors")

# VPN Configuration
VPN_CONFIG = {
    "name": "FREE VPN",
    "version": "2.0.0",
    "port": 8080,
    "autonomous": True,
    "no_openvpn_required": True,
    "servers": [
        {
            "id": "us",
            "name": "United States",
            "location": "New York",
            "flag": "🇺🇸",
            "host": "us-proxy.free-vpn.net",
            "port": 8080,
            "speed": "100 Mbps",
            "load": "Low"
        },
        {
            "id": "uk",
            "name": "United Kingdom", 
            "location": "London",
            "flag": "🇬🇧",
            "host": "uk-proxy.free-vpn.net",
            "port": 8080,
            "speed": "100 Mbps",
            "load": "Low"
        },
        {
            "id": "de",
            "name": "Germany",
            "location": "Frankfurt", 
            "flag": "🇩🇪",
            "host": "de-proxy.free-vpn.net",
            "port": 8080,
            "speed": "100 Mbps",
            "load": "Medium"
        },
        {
            "id": "nl",
            "name": "Netherlands",
            "location": "Amsterdam",
            "flag": "🇳🇱", 
            "host": "nl-proxy.free-vpn.net",
            "port": 8080,
            "speed": "100 Mbps",
            "load": "Low"
        },
        {
            "id": "ca",
            "name": "Canada",
            "location": "Toronto",
            "flag": "🇨🇦",
            "host": "ca-proxy.free-vpn.net", 
            "port": 8080,
            "speed": "100 Mbps",
            "load": "Medium"
        },
        {
            "id": "jp",
            "name": "Japan",
            "location": "Tokyo",
            "flag": "🇯🇵",
            "host": "jp-proxy.free-vpn.net",
            "port": 8080,
            "speed": "100 Mbps",
            "load": "Low"
        }
    ]
}

# Flask Web Interface (if Flask is available)
if FLASK_AVAILABLE:
    app = Flask(__name__)
    CORS(app)
    vpn_core = AutonomousVPN()
    
    @app.route('/api/status', methods=['GET'])
    def api_status():
        """Get VPN status"""
        status = vpn_core.status()
        status["servers"] = VPN_CONFIG['servers']
        return jsonify(status)
    
    @app.route('/api/servers', methods=['GET'])
    def api_servers():
        """Get available servers"""
        return jsonify({
            "servers": VPN_CONFIG['servers'],
            "total": len(VPN_CONFIG['servers']),
            "timestamp": datetime.now().isoformat()
        })
    
    @app.route('/api/connect/<server_id>', methods=['POST'])
    def api_connect(server_id):
        """Connect to server"""
        success, message = vpn_core.connect(server_id)
        return jsonify({
            "success": success,
            "message": message,
            "server": vpn_core.current_server,
            "timestamp": datetime.now().isoformat()
        })
    
    @app.route('/api/disconnect', methods=['POST'])
    def api_disconnect():
        """Disconnect VPN"""
        success, message = vpn_core.disconnect()
        return jsonify({
            "success": success,
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
    
    @app.route('/api/health', methods=['GET'])
    def api_health():
        """Health check"""
        return jsonify({
            "status": "healthy",
            "version": VPN_CONFIG['version'],
            "timestamp": datetime.now().isoformat()
        })
    
    @app.route('/')
    def dashboard():
        """Main dashboard"""
        return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FREE VPN - Open Source VPN Solution</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
        }
        .header {
            background: rgba(0,0,0,0.2);
            padding: 20px 0;
            text-align: center;
            backdrop-filter: blur(10px);
        }
        .logo {
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 10px;
            background: linear-gradient(45deg, #FFD700, #FFA500);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 30px 20px;
        }
        .status-card {
            background: rgba(255,255,255,0.15);
            border-radius: 20px;
            padding: 30px;
            margin: 20px 0;
            backdrop-filter: blur(15px);
            text-align: center;
        }
        .servers-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        .server-card {
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 25px;
            transition: all 0.3s ease;
            border: 2px solid transparent;
        }
        .server-card:hover {
            transform: translateY(-5px);
            background: rgba(255,255,255,0.2);
            border-color: rgba(255,215,0,0.5);
        }
        .connect-btn {
            width: 100%;
            background: linear-gradient(45deg, #4CAF50, #45a049);
            color: white;
            border: none;
            padding: 15px;
            border-radius: 25px;
            font-size: 1.1em;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .connect-btn:hover {
            background: linear-gradient(45deg, #45a049, #4CAF50);
            transform: scale(1.05);
        }
        .connect-btn:disabled {
            background: #666;
            cursor: not-allowed;
            transform: none;
        }
        .controls {
            text-align: center;
            margin: 30px 0;
        }
        .control-btn {
            background: rgba(255,255,255,0.2);
            color: white;
            border: 2px solid rgba(255,255,255,0.3);
            padding: 12px 25px;
            border-radius: 25px;
            margin: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .control-btn:hover {
            background: rgba(255,255,255,0.3);
            transform: translateY(-2px);
        }
        .disconnect-btn {
            background: linear-gradient(45deg, #f44336, #d32f2f);
            border-color: #f44336;
        }
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        .feature {
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
        }
        .feature-icon {
            font-size: 2.5em;
            margin-bottom: 15px;
            color: #FFD700;
        }
        @media (max-width: 768px) {
            .servers-grid { grid-template-columns: 1fr; }
            .features { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="logo">🛡️ FREE VPN</div>
        <div>Open Source VPN Solution</div>
        <div style="opacity: 0.8; margin-top: 5px;">Professional • Secure • Free Forever</div>
    </div>
    
    <div class="container">
        <div class="status-card">
            <div id="status-indicator" style="font-size: 4em; margin-bottom: 20px;">🔒</div>
            <div id="status-text" style="font-size: 1.5em; margin-bottom: 10px;">Checking connection...</div>
            <div id="ip-info" style="background: rgba(0,0,0,0.2); border-radius: 15px; padding: 20px; margin: 20px 0;">Loading IP information...</div>
        </div>
        
        <div class="features">
            <div class="feature">
                <div class="feature-icon">🌍</div>
                <h4>Global Servers</h4>
                <p>6 worldwide locations for optimal performance</p>
            </div>
            <div class="feature">
                <div class="feature-icon">🔒</div>
                <h4>Secure & Private</h4>
                <p>Military-grade encryption and privacy protection</p>
            </div>
            <div class="feature">
                <div class="feature-icon">⚡</div>
                <h4>Easy Setup</h4>
                <p>No complex configuration - just run and connect</p>
            </div>
            <div class="feature">
                <div class="feature-icon">🆓</div>
                <h4>100% Free</h4>
                <p>Open source and completely free forever</p>
            </div>
        </div>
        
        <h2 style="text-align: center; margin: 40px 0 20px 0;">🌍 Choose Your Server</h2>
        <div id="servers" class="servers-grid">Loading servers...</div>
        
        <div class="controls">
            <button class="control-btn" onclick="refreshStatus()">🔄 Refresh Status</button>
            <button class="control-btn disconnect-btn" onclick="disconnect()">🔴 Disconnect VPN</button>
        </div>
    </div>

    <script>
        let isConnecting = false;
        
        async function refreshStatus() {
            try {
                const response = await fetch('/api/status');
                const data = await response.json();
                
                const statusIndicator = document.getElementById('status-indicator');
                const statusText = document.getElementById('status-text');
                const ipInfo = document.getElementById('ip-info');
                
                if (data.connected) {
                    statusIndicator.innerHTML = '🟢';
                    statusText.innerHTML = '✅ Connected to FREE VPN';
                    statusText.style.color = '#4CAF50';
                    
                    ipInfo.innerHTML = `
                        <strong>🌐 Your IP Address:</strong> ${data.current_ip}<br>
                        <strong>📍 Original IP:</strong> ${data.original_ip}<br>
                        <strong>🔄 IP Changed:</strong> ${data.ip_changed ? '✅ YES' : '❌ NO'}<br>
                        <strong>🛡️ OpenVPN Available:</strong> ${data.openvpn_available ? '✅ YES' : '❌ NO'}<br>
                        <strong>⏱️ Connected since:</strong> ${data.connection_time ? new Date(data.connection_time).toLocaleString() : 'N/A'}
                    `;
                } else if (data.connecting || isConnecting) {
                    statusIndicator.innerHTML = '🟡';
                    statusText.innerHTML = '🔄 Connecting to VPN...';
                    statusText.style.color = '#FF9800';
                    ipInfo.innerHTML = `<strong>Current IP:</strong> ${data.current_ip}<br><em>Establishing VPN connection...</em>`;
                } else {
                    statusIndicator.innerHTML = '🔴';
                    statusText.innerHTML = '❌ Not Connected';
                    statusText.style.color = '#f44336';
                    ipInfo.innerHTML = `
                        <strong>Your IP Address:</strong> ${data.current_ip}<br>
                        <strong>🛡️ OpenVPN Available:</strong> ${data.openvpn_available ? '✅ YES (Real VPN)' : '❌ NO (Proxy Mode)'}<br>
                        <em>Connect to a server to protect your privacy</em>
                    `;
                }
                
                updateServerButtons(data.connected || isConnecting);
                
            } catch (error) {
                document.getElementById('status-text').innerHTML = `❌ Error: ${error.message}`;
            }
        }
        
        async function loadServers() {
            try {
                const response = await fetch('/api/servers');
                const data = await response.json();
                
                const serversEl = document.getElementById('servers');
                serversEl.innerHTML = '';
                
                data.servers.forEach(server => {
                    const serverDiv = document.createElement('div');
                    serverDiv.className = 'server-card';
                    serverDiv.innerHTML = `
                        <div style="display: flex; align-items: center; margin-bottom: 15px;">
                            <div style="font-size: 2em; margin-right: 15px;">${server.flag}</div>
                            <div>
                                <h3>${server.name}</h3>
                                <div style="opacity: 0.8;">${server.location}</div>
                            </div>
                        </div>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 15px 0;">
                            <div style="background: rgba(0,0,0,0.2); padding: 10px; border-radius: 8px; text-align: center;">
                                <div style="font-size: 0.8em; opacity: 0.7;">Speed</div>
                                <div style="font-weight: bold; color: #4CAF50;">${server.speed}</div>
                            </div>
                            <div style="background: rgba(0,0,0,0.2); padding: 10px; border-radius: 8px; text-align: center;">
                                <div style="font-size: 0.8em; opacity: 0.7;">Load</div>
                                <div style="font-weight: bold; color: #4CAF50;">${server.load}</div>
                            </div>
                        </div>
                        <button class="connect-btn" onclick="connect('${server.id}')" id="btn-${server.id}">
                            🔌 Connect to ${server.location}
                        </button>
                    `;
                    serversEl.appendChild(serverDiv);
                });
            } catch (error) {
                document.getElementById('servers').innerHTML = `<div style="text-align: center; color: #f44336;">Error loading servers: ${error.message}</div>`;
            }
        }
        
        function updateServerButtons(disabled) {
            const buttons = document.querySelectorAll('.connect-btn');
            buttons.forEach(btn => {
                btn.disabled = disabled;
                if (disabled && isConnecting) {
                    btn.innerHTML = '⏳ Connecting...';
                }
            });
        }
        
        async function connect(serverId) {
            if (isConnecting) return;
            
            isConnecting = true;
            updateServerButtons(true);
            
            try {
                const response = await fetch(`/api/connect/${serverId}`, { method: 'POST' });
                const data = await response.json();
                
                if (data.success) {
                    alert(`✅ VPN Connected Successfully!\\n🌍 Server: ${data.server.name}\\n🔄 Your connection is now protected!`);
                    refreshStatus();
                } else {
                    alert('❌ Connection failed: ' + data.message);
                }
            } catch (error) {
                alert('❌ Connection error: ' + error.message);
            } finally {
                isConnecting = false;
                loadServers();
            }
        }
        
        async function disconnect() {
            try {
                const response = await fetch('/api/disconnect', { method: 'POST' });
                const data = await response.json();
                
                if (data.success) {
                    alert('✅ VPN Disconnected Successfully!\\n🔄 Your connection is back to normal.');
                    refreshStatus();
                } else {
                    alert('❌ Disconnection failed: ' + data.message);
                }
            } catch (error) {
                alert('❌ Disconnection error: ' + error.message);
            }
        }
        
        // Initialize dashboard
        refreshStatus();
        loadServers();
        
        // Auto-refresh every 30 seconds
        setInterval(refreshStatus, 30000);
    </script>
</body>
</html>
        ''')

def main():
    """Main entry point"""
    print("🛡️  FREE VPN - Open Source VPN Solution")
    print("=" * 60)
    print(f"📍 Your current IP: {AutonomousVPN().get_ip()}")
    print()
    
    if FLASK_AVAILABLE:
        print("🚀 Starting web interface...")
        print(f"🌐 Dashboard: http://localhost:{VPN_CONFIG['port']}")
        print("🔒 Professional VPN service ready!")
        print("📱 Works on all devices and browsers")
        print()
        print("⚡ Press Ctrl+C to stop the server")
        print()
        
        try:
            app.run(host='0.0.0.0', port=VPN_CONFIG['port'], debug=False)
        except KeyboardInterrupt:
            print("\n🔴 Shutting down FREE VPN...")
            vpn_core.disconnect()
    else:
        print("❌ Flask not available. Install with: pip install flask flask-cors")
        print("🔧 Running in CLI mode...")
        
        # Simple CLI interface
        vpn = AutonomousVPN()
        
        while True:
            print("\n🛡️  FREE VPN - CLI Mode")
            print("1. Show status")
            print("2. Connect to server")
            print("3. Disconnect")
            print("4. Exit")
            
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == '1':
                status = vpn.status()
                print(f"\n📊 Status: {'Connected' if status['connected'] else 'Disconnected'}")
                print(f"🌐 Current IP: {status['current_ip']}")
                if status['server']:
                    print(f"🌍 Server: {status['server']['name']}")
                    
            elif choice == '2':
                print("\n🌍 Available servers:")
                for i, server in enumerate(VPN_CONFIG['servers'], 1):
                    print(f"{i}. {server['flag']} {server['name']} - {server['location']}")
                
                try:
                    server_choice = int(input("\nSelect server (1-6): ")) - 1
                    if 0 <= server_choice < len(VPN_CONFIG['servers']):
                        server_id = VPN_CONFIG['servers'][server_choice]['id']
                        success, message = vpn.connect(server_id)
                        print(f"\n{'✅' if success else '❌'} {message}")
                    else:
                        print("❌ Invalid server selection")
                except ValueError:
                    print("❌ Invalid input")
                    
            elif choice == '3':
                success, message = vpn.disconnect()
                print(f"\n{'✅' if success else '❌'} {message}")
                
            elif choice == '4':
                vpn.disconnect()
                print("\n👋 Goodbye!")
                break
                
            else:
                print("❌ Invalid choice")

if __name__ == "__main__":
    main()
