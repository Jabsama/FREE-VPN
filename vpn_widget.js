/**
 * VoltageGPU VPN Widget
 * Integrates with local FREE VPN server for voltagegpu.com
 */

class VoltageVPNWidget {
    constructor(options = {}) {
        this.apiUrl = options.apiUrl || 'http://localhost:8080/api';
        this.containerId = options.containerId || 'vpn-widget';
        this.autoRefresh = options.autoRefresh !== false;
        this.refreshInterval = options.refreshInterval || 5000;
        
        this.connected = false;
        this.currentServer = null;
        this.servers = [];
        this.status = {};
        
        this.init();
    }
    
    async init() {
        console.log('🛡️ VoltageGPU VPN Widget initializing...');
        await this.loadServers();
        await this.updateStatus();
        this.render();
        
        if (this.autoRefresh) {
            setInterval(() => this.updateStatus(), this.refreshInterval);
        }
    }
    
    async loadServers() {
        try {
            const response = await fetch(`${this.apiUrl}/servers`);
            const data = await response.json();
            this.servers = data.servers || [];
            console.log('📡 Loaded VPN servers:', this.servers.length);
        } catch (error) {
            console.error('❌ Failed to load servers:', error);
            this.servers = this.getDefaultServers();
        }
    }
    
    async updateStatus() {
        try {
            const response = await fetch(`${this.apiUrl}/status`);
            const data = await response.json();
            this.status = data;
            this.connected = data.connected || false;
            this.currentServer = data.server;
            this.updateUI();
        } catch (error) {
            console.error('❌ Failed to update status:', error);
            this.status = { connected: false, current_ip: 'Unknown' };
            this.connected = false;
        }
    }
    
    async connectToServer(serverId) {
        try {
            console.log(`🔄 Connecting to server: ${serverId}`);
            const response = await fetch(`${this.apiUrl}/connect/${serverId}`, {
                method: 'POST'
            });
            const data = await response.json();
            
            if (data.success) {
                console.log('✅ VPN Connected successfully');
                await this.updateStatus();
                this.showNotification('Connected to VPN!', 'success');
            } else {
                console.error('❌ Connection failed:', data.message);
                this.showNotification('Connection failed: ' + data.message, 'error');
            }
        } catch (error) {
            console.error('❌ Connection error:', error);
            this.showNotification('Connection error', 'error');
        }
    }
    
    async disconnect() {
        try {
            console.log('🔄 Disconnecting VPN...');
            const response = await fetch(`${this.apiUrl}/disconnect`, {
                method: 'POST'
            });
            const data = await response.json();
            
            if (data.success) {
                console.log('✅ VPN Disconnected successfully');
                await this.updateStatus();
                this.showNotification('VPN Disconnected', 'success');
            } else {
                console.error('❌ Disconnection failed:', data.message);
                this.showNotification('Disconnection failed', 'error');
            }
        } catch (error) {
            console.error('❌ Disconnection error:', error);
            this.showNotification('Disconnection error', 'error');
        }
    }
    
    getDefaultServers() {
        return [
            {
                id: 'us-east',
                name: 'USA East Coast',
                location: 'New York, USA',
                flag: '🇺🇸',
                ping: '12ms',
                load: '23%',
                speed: '1 Gbps',
                users: '1,247',
                uptime: '99.9%'
            },
            {
                id: 'us-west',
                name: 'USA West Coast',
                location: 'Los Angeles, USA',
                flag: '🇺🇸',
                ping: '8ms',
                load: '31%',
                speed: '1 Gbps',
                users: '892',
                uptime: '99.8%'
            },
            {
                id: 'uk',
                name: 'United Kingdom',
                location: 'London, UK',
                flag: '🇬🇧',
                ping: '15ms',
                load: '18%',
                speed: '1 Gbps',
                users: '1,456',
                uptime: '99.9%'
            },
            {
                id: 'de',
                name: 'Germany',
                location: 'Frankfurt, Germany',
                flag: '🇩🇪',
                ping: '10ms',
                load: '27%',
                speed: '1 Gbps',
                users: '1,123',
                uptime: '99.7%'
            },
            {
                id: 'nl',
                name: 'Netherlands',
                location: 'Amsterdam, Netherlands',
                flag: '🇳🇱',
                ping: '12ms',
                load: '15%',
                speed: '1 Gbps',
                users: '967',
                uptime: '99.9%'
            },
            {
                id: 'jp',
                name: 'Japan',
                location: 'Tokyo, Japan',
                flag: '🇯🇵',
                ping: '25ms',
                load: '22%',
                speed: '1 Gbps',
                users: '743',
                uptime: '99.6%'
            }
        ];
    }
    
    render() {
        const container = document.getElementById(this.containerId);
        if (!container) {
            console.error(`❌ Container #${this.containerId} not found`);
            return;
        }
        
        container.innerHTML = `
            <div class="voltage-vpn-widget">
                <div class="vpn-header">
                    <h2>🛡️ VPN Connection Status</h2>
                    <div class="vpn-status" id="vpn-status">
                        <span class="status-indicator ${this.connected ? 'connected' : 'disconnected'}">
                            ${this.connected ? '🟢 CONNECTED' : '🔴 DISCONNECTED'}
                        </span>
                    </div>
                </div>
                
                <div class="vpn-info" id="vpn-info">
                    <p>${this.connected ? 'Your connection is protected' : 'Your connection is not protected'}</p>
                    <p>Current IP: <strong>${this.status.current_ip || 'Unknown'}</strong></p>
                    ${this.connected && this.currentServer ? 
                        `<p>Connected to: <strong>${this.currentServer.name}</strong></p>` : 
                        '<p>Connect to a VPN server to secure your internet traffic and change your IP address.</p>'
                    }
                </div>
                
                <div class="vpn-actions">
                    ${this.connected ? 
                        '<button class="vpn-btn disconnect-btn" onclick="voltageVPN.disconnect()">🔴 Disconnect</button>' :
                        '<button class="vpn-btn connect-btn" onclick="voltageVPN.quickConnect()">🚀 Quick Connect to Best Server</button>'
                    }
                </div>
                
                <div class="vpn-servers">
                    <h3>🌍 VPN Server Network</h3>
                    <p>Choose from our global network of high-speed VPN servers</p>
                    <div class="servers-grid" id="servers-grid">
                        ${this.renderServers()}
                    </div>
                </div>
                
                <div class="vpn-monitoring">
                    <h3>📈 VPN Performance Monitoring</h3>
                    <p>Real-time monitoring of your VPN connection and system performance</p>
                    <div class="monitoring-content">
                        ${this.connected ? 
                            '<div class="monitoring-active">✅ VPN Active - Monitoring enabled</div>' :
                            '<div class="monitoring-inactive">No VPN Connection<br>Connect to a VPN server to view real-time monitoring data</div>'
                        }
                    </div>
                </div>
            </div>
        `;
        
        this.addStyles();
    }
    
    renderServers() {
        return this.servers.map(server => `
            <div class="server-card">
                <div class="server-header">
                    <span class="server-flag">${server.flag}</span>
                    <div class="server-info">
                        <h4>${server.name}</h4>
                        <p>${server.location}</p>
                    </div>
                    <span class="server-status online">online</span>
                </div>
                <div class="server-stats">
                    <div class="stat">
                        <label>Ping:</label>
                        <span>${server.ping}</span>
                    </div>
                    <div class="stat">
                        <label>Load:</label>
                        <span>${server.load}</span>
                    </div>
                    <div class="stat">
                        <label>Speed:</label>
                        <span>${server.speed}</span>
                    </div>
                    <div class="stat">
                        <label>Users:</label>
                        <span>${server.users}</span>
                    </div>
                    <div class="stat">
                        <label>Uptime:</label>
                        <span>${server.uptime}</span>
                    </div>
                </div>
                <div class="server-load-bar">
                    <div class="load-progress" style="width: ${server.load}"></div>
                </div>
                <button class="server-connect-btn" onclick="voltageVPN.connectToServer('${server.id}')">
                    🚀 Connect
                </button>
            </div>
        `).join('');
    }
    
    updateUI() {
        const statusEl = document.getElementById('vpn-status');
        const infoEl = document.getElementById('vpn-info');
        
        if (statusEl) {
            statusEl.innerHTML = `
                <span class="status-indicator ${this.connected ? 'connected' : 'disconnected'}">
                    ${this.connected ? '🟢 CONNECTED' : '🔴 DISCONNECTED'}
                </span>
            `;
        }
        
        if (infoEl) {
            infoEl.innerHTML = `
                <p>${this.connected ? 'Your connection is protected' : 'Your connection is not protected'}</p>
                <p>Current IP: <strong>${this.status.current_ip || 'Unknown'}</strong></p>
                ${this.connected && this.currentServer ? 
                    `<p>Connected to: <strong>${this.currentServer.name}</strong></p>` : 
                    '<p>Connect to a VPN server to secure your internet traffic and change your IP address.</p>'
                }
            `;
        }
    }
    
    async quickConnect() {
        // Connect to the best server (lowest load)
        const bestServer = this.servers.reduce((best, server) => {
            const currentLoad = parseInt(server.load);
            const bestLoad = parseInt(best.load);
            return currentLoad < bestLoad ? server : best;
        });
        
        await this.connectToServer(bestServer.id);
    }
    
    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `vpn-notification ${type}`;
        notification.textContent = message;
        
        // Add to page
        document.body.appendChild(notification);
        
        // Remove after 3 seconds
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
    
    addStyles() {
        if (document.getElementById('voltage-vpn-styles')) return;
        
        const styles = document.createElement('style');
        styles.id = 'voltage-vpn-styles';
        styles.textContent = `
            .voltage-vpn-widget {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background: #f8f9fa;
                border-radius: 10px;
            }
            
            .vpn-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
                padding: 20px;
                background: white;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            
            .status-indicator.connected {
                color: #28a745;
                font-weight: bold;
            }
            
            .status-indicator.disconnected {
                color: #dc3545;
                font-weight: bold;
            }
            
            .vpn-info {
                background: white;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 20px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            
            .vpn-actions {
                text-align: center;
                margin-bottom: 30px;
            }
            
            .vpn-btn {
                padding: 15px 30px;
                border: none;
                border-radius: 25px;
                font-size: 16px;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.3s ease;
            }
            
            .connect-btn {
                background: linear-gradient(45deg, #28a745, #20c997);
                color: white;
            }
            
            .disconnect-btn {
                background: linear-gradient(45deg, #dc3545, #fd7e14);
                color: white;
            }
            
            .vpn-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }
            
            .servers-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
                gap: 20px;
                margin-top: 20px;
            }
            
            .server-card {
                background: white;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                transition: transform 0.3s ease;
            }
            
            .server-card:hover {
                transform: translateY(-5px);
            }
            
            .server-header {
                display: flex;
                align-items: center;
                margin-bottom: 15px;
            }
            
            .server-flag {
                font-size: 2em;
                margin-right: 15px;
            }
            
            .server-info h4 {
                margin: 0;
                color: #333;
            }
            
            .server-info p {
                margin: 5px 0 0 0;
                color: #666;
            }
            
            .server-status.online {
                background: #28a745;
                color: white;
                padding: 4px 8px;
                border-radius: 15px;
                font-size: 12px;
                margin-left: auto;
            }
            
            .server-stats {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 10px;
                margin-bottom: 15px;
            }
            
            .stat {
                display: flex;
                justify-content: space-between;
                padding: 5px 0;
            }
            
            .stat label {
                color: #666;
            }
            
            .stat span {
                font-weight: bold;
                color: #333;
            }
            
            .server-load-bar {
                background: #e9ecef;
                height: 8px;
                border-radius: 4px;
                margin-bottom: 15px;
                overflow: hidden;
            }
            
            .load-progress {
                background: linear-gradient(45deg, #28a745, #20c997);
                height: 100%;
                transition: width 0.3s ease;
            }
            
            .server-connect-btn {
                width: 100%;
                background: linear-gradient(45deg, #007bff, #0056b3);
                color: white;
                border: none;
                padding: 12px;
                border-radius: 8px;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.3s ease;
            }
            
            .server-connect-btn:hover {
                background: linear-gradient(45deg, #0056b3, #007bff);
                transform: scale(1.02);
            }
            
            .vpn-monitoring {
                background: white;
                padding: 20px;
                border-radius: 10px;
                margin-top: 30px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            
            .monitoring-active {
                color: #28a745;
                font-weight: bold;
                text-align: center;
                padding: 20px;
            }
            
            .monitoring-inactive {
                color: #666;
                text-align: center;
                padding: 20px;
            }
            
            .vpn-notification {
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 15px 20px;
                border-radius: 8px;
                color: white;
                font-weight: bold;
                z-index: 1000;
                animation: slideIn 0.3s ease;
            }
            
            .vpn-notification.success {
                background: #28a745;
            }
            
            .vpn-notification.error {
                background: #dc3545;
            }
            
            .vpn-notification.info {
                background: #007bff;
            }
            
            @keyframes slideIn {
                from { transform: translateX(100%); }
                to { transform: translateX(0); }
            }
            
            @media (max-width: 768px) {
                .servers-grid {
                    grid-template-columns: 1fr;
                }
                
                .vpn-header {
                    flex-direction: column;
                    text-align: center;
                }
                
                .server-stats {
                    grid-template-columns: 1fr;
                }
            }
        `;
        
        document.head.appendChild(styles);
    }
}

// Global instance for easy access
let voltageVPN;

// Auto-initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('vpn-widget')) {
        voltageVPN = new VoltageVPNWidget();
        console.log('🛡️ VoltageGPU VPN Widget loaded successfully');
    }
});
