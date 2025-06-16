/**
 * VoltageGPU.com VPN Dashboard Integration
 * Connects your website to VoltageVPN API for real VPN functionality
 */

class VoltageGPUVPN {
    constructor(apiUrl = 'http://localhost:8080') {
        this.apiUrl = apiUrl;
        this.connected = false;
        this.currentServer = null;
        this.statusCheckInterval = null;
        
        // Initialize dashboard
        this.init();
    }
    
    /**
     * Initialize VPN integration on voltagegpu.com
     */
    async init() {
        console.log('🌐 VoltageGPU VPN Dashboard initializing...');
        
        // Check if VoltageVPN server is running
        const serverAvailable = await this.checkServerAvailability();
        
        if (serverAvailable) {
            console.log('✅ VoltageVPN server connected');
            this.startStatusMonitoring();
            await this.loadDashboard();
        } else {
            console.log('❌ VoltageVPN server not available');
            this.showServerNotAvailable();
        }
    }
    
    /**
     * Check if VoltageVPN server is running
     */
    async checkServerAvailability() {
        try {
            const response = await fetch(`${this.apiUrl}/api/status`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
                timeout: 5000
            });
            
            return response.ok;
        } catch (error) {
            console.log('VoltageVPN server not reachable:', error.message);
            return false;
        }
    }
    
    /**
     * Get current VPN status
     */
    async getStatus() {
        try {
            const response = await fetch(`${this.apiUrl}/api/status`);
            const data = await response.json();
            
            this.connected = data.connected;
            this.currentServer = data.current_server;
            
            return data;
        } catch (error) {
            console.error('Failed to get VPN status:', error);
            return null;
        }
    }
    
    /**
     * Get available VPN servers
     */
    async getServers() {
        try {
            const response = await fetch(`${this.apiUrl}/api/servers`);
            const data = await response.json();
            return data.servers;
        } catch (error) {
            console.error('Failed to get servers:', error);
            return {};
        }
    }
    
    /**
     * Connect to VPN server
     */
    async connect(serverKey) {
        try {
            console.log(`🔄 Connecting to ${serverKey}...`);
            
            const response = await fetch(`${this.apiUrl}/api/connect/${serverKey}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            const result = await response.json();
            
            if (result.success) {
                console.log('✅ VPN Connected:', result.message);
                this.connected = true;
                this.currentServer = serverKey;
                
                // Show success notification on voltagegpu.com
                this.showNotification('success', `✅ Connected to ${result.server.name}! Your IP is now changed on ALL websites.`);
                
                // Update dashboard
                await this.updateDashboard();
                
                return true;
            } else {
                console.error('❌ Connection failed:', result.message);
                this.showNotification('error', `❌ Connection failed: ${result.message}`);
                return false;
            }
        } catch (error) {
            console.error('Connection error:', error);
            this.showNotification('error', `❌ Connection error: ${error.message}`);
            return false;
        }
    }
    
    /**
     * Disconnect from VPN
     */
    async disconnect() {
        try {
            console.log('🔄 Disconnecting VPN...');
            
            const response = await fetch(`${this.apiUrl}/api/disconnect`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            const result = await response.json();
            
            if (result.success) {
                console.log('✅ VPN Disconnected:', result.message);
                this.connected = false;
                this.currentServer = null;
                
                this.showNotification('success', '✅ VPN disconnected successfully. Your IP is back to normal.');
                await this.updateDashboard();
                
                return true;
            } else {
                console.error('❌ Disconnection failed:', result.message);
                this.showNotification('error', `❌ Disconnection failed: ${result.message}`);
                return false;
            }
        } catch (error) {
            console.error('Disconnection error:', error);
            this.showNotification('error', `❌ Disconnection error: ${error.message}`);
            return false;
        }
    }
    
    /**
     * Start monitoring VPN status
     */
    startStatusMonitoring() {
        // Check status every 30 seconds
        this.statusCheckInterval = setInterval(async () => {
            await this.updateDashboard();
        }, 30000);
    }
    
    /**
     * Stop monitoring VPN status
     */
    stopStatusMonitoring() {
        if (this.statusCheckInterval) {
            clearInterval(this.statusCheckInterval);
            this.statusCheckInterval = null;
        }
    }
    
    /**
     * Load VPN dashboard into voltagegpu.com
     */
    async loadDashboard() {
        const dashboardContainer = document.getElementById('vpn-dashboard');
        if (!dashboardContainer) {
            console.error('VPN dashboard container not found. Add <div id="vpn-dashboard"></div> to your page.');
            return;
        }
        
        const status = await this.getStatus();
        const servers = await this.getServers();
        
        dashboardContainer.innerHTML = this.generateDashboardHTML(status, servers);
        this.attachEventListeners();
    }
    
    /**
     * Update dashboard display
     */
    async updateDashboard() {
        const status = await this.getStatus();
        const servers = await this.getServers();
        
        // Update status display
        const statusElement = document.getElementById('vpn-status-display');
        if (statusElement) {
            statusElement.innerHTML = this.generateStatusHTML(status);
        }
        
        // Update server buttons
        this.updateServerButtons(status);
    }
    
    /**
     * Generate dashboard HTML for voltagegpu.com
     */
    generateDashboardHTML(status, servers) {
        return `
            <div class="voltagegpu-vpn-dashboard">
                <div class="vpn-header">
                    <h2>⚡ VoltageVPN Dashboard</h2>
                    <p>Professional VPN integrated with VoltageGPU.com</p>
                </div>
                
                <div id="vpn-status-display" class="vpn-status">
                    ${this.generateStatusHTML(status)}
                </div>
                
                <div class="vpn-servers">
                    <h3>🌍 Available VPN Servers</h3>
                    <div class="servers-grid">
                        ${Object.entries(servers).map(([key, server]) => `
                            <div class="server-card" data-server="${key}">
                                <div class="server-info">
                                    <span class="server-flag">${server.flag}</span>
                                    <div class="server-details">
                                        <h4>${server.name}</h4>
                                        <p>${server.location}</p>
                                        <small>Speed: ${server.speed} | Load: ${server.load}</small>
                                    </div>
                                </div>
                                <button class="connect-btn" data-server="${key}" ${status?.connected ? 'disabled' : ''}>
                                    ${status?.connected && status?.current_server === key ? 'Connected' : 'Connect'}
                                </button>
                            </div>
                        `).join('')}
                    </div>
                </div>
                
                <div class="vpn-controls">
                    <button id="disconnect-btn" class="disconnect-btn" ${!status?.connected ? 'disabled' : ''}>
                        🔌 Disconnect VPN
                    </button>
                    <button id="refresh-btn" class="refresh-btn">
                        🔄 Refresh Status
                    </button>
                </div>
            </div>
            
            <style>
                .voltagegpu-vpn-dashboard {
                    max-width: 1000px;
                    margin: 20px auto;
                    padding: 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border-radius: 15px;
                    color: white;
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                }
                
                .vpn-header {
                    text-align: center;
                    margin-bottom: 30px;
                }
                
                .vpn-status {
                    background: rgba(255,255,255,0.15);
                    border-radius: 10px;
                    padding: 20px;
                    margin: 20px 0;
                    text-align: center;
                }
                
                .servers-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                    gap: 15px;
                    margin: 20px 0;
                }
                
                .server-card {
                    background: rgba(255,255,255,0.1);
                    border-radius: 10px;
                    padding: 15px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }
                
                .server-info {
                    display: flex;
                    align-items: center;
                }
                
                .server-flag {
                    font-size: 2em;
                    margin-right: 15px;
                }
                
                .connect-btn, .disconnect-btn, .refresh-btn {
                    background: #4CAF50;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 20px;
                    cursor: pointer;
                    font-weight: bold;
                    transition: all 0.3s;
                }
                
                .connect-btn:hover, .refresh-btn:hover {
                    background: #45a049;
                    transform: translateY(-2px);
                }
                
                .disconnect-btn {
                    background: #f44336;
                }
                
                .disconnect-btn:hover {
                    background: #d32f2f;
                }
                
                .connect-btn:disabled, .disconnect-btn:disabled {
                    background: #666;
                    cursor: not-allowed;
                    transform: none;
                }
                
                .vpn-controls {
                    text-align: center;
                    margin-top: 30px;
                }
                
                .vpn-controls button {
                    margin: 0 10px;
                }
                
                .status-connected {
                    color: #4CAF50;
                    font-weight: bold;
                }
                
                .status-disconnected {
                    color: #f44336;
                    font-weight: bold;
                }
            </style>
        `;
    }
    
    /**
     * Generate status HTML
     */
    generateStatusHTML(status) {
        if (!status) {
            return '<p class="status-disconnected">❌ Unable to connect to VPN server</p>';
        }
        
        if (status.connected) {
            return `
                <p class="status-connected">✅ VPN Connected</p>
                <p><strong>Current IP:</strong> ${status.current_ip}</p>
                <p><strong>Original IP:</strong> ${status.original_ip}</p>
                <p><strong>IP Changed:</strong> ${status.ip_changed ? '✅ YES' : '❌ NO'}</p>
                <p><strong>Works on ALL websites:</strong> ✅ YES</p>
            `;
        } else {
            return `
                <p class="status-disconnected">❌ VPN Disconnected</p>
                <p><strong>Your IP:</strong> ${status.current_ip}</p>
                <p><em>Connect to a server to change your IP on ALL websites</em></p>
            `;
        }
    }
    
    /**
     * Update server buttons based on status
     */
    updateServerButtons(status) {
        const buttons = document.querySelectorAll('.connect-btn');
        const disconnectBtn = document.getElementById('disconnect-btn');
        
        buttons.forEach(btn => {
            const serverKey = btn.getAttribute('data-server');
            
            if (status?.connected) {
                btn.disabled = true;
                if (status.current_server === serverKey) {
                    btn.textContent = 'Connected';
                    btn.style.background = '#4CAF50';
                } else {
                    btn.textContent = 'Connect';
                    btn.style.background = '#666';
                }
            } else {
                btn.disabled = false;
                btn.textContent = 'Connect';
                btn.style.background = '#4CAF50';
            }
        });
        
        if (disconnectBtn) {
            disconnectBtn.disabled = !status?.connected;
        }
    }
    
    /**
     * Attach event listeners
     */
    attachEventListeners() {
        // Connect buttons
        document.querySelectorAll('.connect-btn').forEach(btn => {
            btn.addEventListener('click', async (e) => {
                const serverKey = e.target.getAttribute('data-server');
                await this.connect(serverKey);
            });
        });
        
        // Disconnect button
        const disconnectBtn = document.getElementById('disconnect-btn');
        if (disconnectBtn) {
            disconnectBtn.addEventListener('click', async () => {
                await this.disconnect();
            });
        }
        
        // Refresh button
        const refreshBtn = document.getElementById('refresh-btn');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', async () => {
                await this.updateDashboard();
            });
        }
    }
    
    /**
     * Show notification on voltagegpu.com
     */
    showNotification(type, message) {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `vpn-notification vpn-notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <span>${message}</span>
                <button class="notification-close">&times;</button>
            </div>
        `;
        
        // Add styles
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'success' ? '#4CAF50' : '#f44336'};
            color: white;
            padding: 15px 20px;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            z-index: 10000;
            max-width: 400px;
            animation: slideIn 0.3s ease-out;
        `;
        
        // Add animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
        `;
        document.head.appendChild(style);
        
        // Add to page
        document.body.appendChild(notification);
        
        // Close button
        notification.querySelector('.notification-close').addEventListener('click', () => {
            notification.remove();
        });
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }
    
    /**
     * Show server not available message
     */
    showServerNotAvailable() {
        const dashboardContainer = document.getElementById('vpn-dashboard');
        if (dashboardContainer) {
            dashboardContainer.innerHTML = `
                <div class="vpn-server-unavailable">
                    <h3>⚠️ VoltageVPN Server Not Available</h3>
                    <p>To use the VPN dashboard on voltagegpu.com, you need to:</p>
                    <ol>
                        <li>Download VoltageVPN from GitHub</li>
                        <li>Run: <code>python voltagevpn.py</code></li>
                        <li>Refresh this page</li>
                    </ol>
                    <a href="https://github.com/Jabsama/FREE-VPN" target="_blank" class="download-btn">
                        📥 Download VoltageVPN
                    </a>
                </div>
                
                <style>
                    .vpn-server-unavailable {
                        text-align: center;
                        padding: 40px;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        border-radius: 15px;
                        color: white;
                        margin: 20px 0;
                    }
                    
                    .vpn-server-unavailable ol {
                        text-align: left;
                        display: inline-block;
                        margin: 20px 0;
                    }
                    
                    .download-btn {
                        display: inline-block;
                        background: #4CAF50;
                        color: white;
                        padding: 15px 30px;
                        text-decoration: none;
                        border-radius: 25px;
                        font-weight: bold;
                        margin-top: 20px;
                        transition: all 0.3s;
                    }
                    
                    .download-btn:hover {
                        background: #45a049;
                        transform: translateY(-2px);
                    }
                </style>
            `;
        }
    }
    
    /**
     * Cleanup when leaving page
     */
    destroy() {
        this.stopStatusMonitoring();
    }
}

// Auto-initialize when page loads
document.addEventListener('DOMContentLoaded', () => {
    // Check if we're on voltagegpu.com VPN dashboard page
    if (document.getElementById('vpn-dashboard')) {
        window.voltageGPUVPN = new VoltageGPUVPN();
        
        // Cleanup on page unload
        window.addEventListener('beforeunload', () => {
            if (window.voltageGPUVPN) {
                window.voltageGPUVPN.destroy();
            }
        });
    }
});

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = VoltageGPUVPN;
}
