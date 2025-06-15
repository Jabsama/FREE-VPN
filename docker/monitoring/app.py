#!/usr/bin/env python3
"""
Advanced VPN Monitoring Dashboard
Real-time monitoring with alerts, statistics, and user management
"""

from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash
import psutil
import subprocess
import json
import os
import re
import sqlite3
import redis
import smtplib
import schedule
import time
import threading
from datetime import datetime, timedelta
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
import requests
import pandas as pd
import plotly.graph_objs as go
import plotly.utils

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'vpn-monitoring-secret-key-2025')

# Configuration
VPN_SERVER_HOST = os.environ.get('VPN_SERVER_HOST', 'vpn-server')
VPN_SERVER_PORT = os.environ.get('VPN_SERVER_PORT', '8080')
REFRESH_INTERVAL = int(os.environ.get('REFRESH_INTERVAL', '10'))
ALERT_EMAIL = os.environ.get('ALERT_EMAIL', 'admin@example.com')

class VPNMonitor:
    def __init__(self):
        self.db_file = '/opt/monitoring/data/vpn_monitor.db'
        self.redis_client = None
        self.init_database()
        self.init_redis()
        
    def init_database(self):
        """Initialize SQLite database"""
        os.makedirs(os.path.dirname(self.db_file), exist_ok=True)
        
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Server statistics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS server_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                cpu_usage REAL,
                memory_usage REAL,
                disk_usage REAL,
                network_in INTEGER,
                network_out INTEGER,
                active_connections INTEGER,
                load_average TEXT,
                uptime INTEGER
            )
        ''')
        
        # Connection logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS connection_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                client_name TEXT,
                client_ip TEXT,
                virtual_ip TEXT,
                action TEXT,
                bytes_received INTEGER DEFAULT 0,
                bytes_sent INTEGER DEFAULT 0,
                duration INTEGER DEFAULT 0
            )
        ''')
        
        # User management table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vpn_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_login DATETIME,
                is_active BOOLEAN DEFAULT 1,
                total_bytes_sent INTEGER DEFAULT 0,
                total_bytes_received INTEGER DEFAULT 0,
                total_connections INTEGER DEFAULT 0
            )
        ''')
        
        # Alerts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                alert_type TEXT,
                severity TEXT,
                message TEXT,
                resolved BOOLEAN DEFAULT 0,
                resolved_at DATETIME
            )
        ''')
        
        # System events table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                event_type TEXT,
                description TEXT,
                details TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def init_redis(self):
        """Initialize Redis connection"""
        try:
            self.redis_client = redis.Redis(
                host='vpn-redis',
                port=6379,
                password='RedisVPN2025!',
                decode_responses=True
            )
            self.redis_client.ping()
        except Exception as e:
            print(f"Redis connection failed: {e}")
            self.redis_client = None
    
    def get_server_stats(self):
        """Get comprehensive server statistics"""
        try:
            # CPU and Memory
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            network = psutil.net_io_counters()
            
            # Load average
            try:
                load_avg = os.getloadavg()
                load_average = f"{load_avg[0]:.2f}, {load_avg[1]:.2f}, {load_avg[2]:.2f}"
            except:
                load_average = "N/A"
            
            # Uptime
            try:
                with open('/proc/uptime', 'r') as f:
                    uptime_seconds = int(float(f.readline().split()[0]))
            except:
                uptime_seconds = 0
            
            # Process information
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    if 'openvpn' in proc.info['name'].lower():
                        processes.append(proc.info)
                except:
                    continue
            
            stats = {
                'cpu_usage': cpu_percent,
                'memory_usage': memory.percent,
                'memory_total': memory.total,
                'memory_used': memory.used,
                'memory_available': memory.available,
                'disk_usage': disk.percent,
                'disk_total': disk.total,
                'disk_used': disk.used,
                'disk_free': disk.free,
                'network_bytes_sent': network.bytes_sent,
                'network_bytes_recv': network.bytes_recv,
                'network_packets_sent': network.packets_sent,
                'network_packets_recv': network.packets_recv,
                'load_average': load_average,
                'uptime': uptime_seconds,
                'processes': processes,
                'timestamp': datetime.now().isoformat()
            }
            
            # Cache in Redis
            if self.redis_client:
                self.redis_client.setex('server_stats', 30, json.dumps(stats))
            
            return stats
            
        except Exception as e:
            return {'error': str(e), 'timestamp': datetime.now().isoformat()}
    
    def get_vpn_status(self):
        """Get VPN server status from main container"""
        try:
            response = requests.get(f'http://{VPN_SERVER_HOST}:{VPN_SERVER_PORT}/api/status', timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                return {'error': f'HTTP {response.status_code}'}
        except Exception as e:
            return {'error': str(e)}
    
    def get_connected_clients(self):
        """Get list of connected VPN clients"""
        try:
            response = requests.get(f'http://{VPN_SERVER_HOST}:{VPN_SERVER_PORT}/api/clients', timeout=5)
            if response.status_code == 200:
                return response.json().get('clients', [])
            else:
                return []
        except Exception as e:
            print(f"Error getting clients: {e}")
            return []
    
    def save_stats(self):
        """Save current statistics to database"""
        stats = self.get_server_stats()
        clients = self.get_connected_clients()
        
        if 'error' not in stats:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO server_stats 
                (cpu_usage, memory_usage, disk_usage, network_in, network_out, 
                 active_connections, load_average, uptime)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                stats.get('cpu_usage', 0),
                stats.get('memory_usage', 0),
                stats.get('disk_usage', 0),
                stats.get('network_bytes_recv', 0),
                stats.get('network_bytes_sent', 0),
                len(clients),
                stats.get('load_average', ''),
                stats.get('uptime', 0)
            ))
            
            conn.commit()
            conn.close()
    
    def get_historical_stats(self, hours=24):
        """Get historical statistics for charts"""
        conn = sqlite3.connect(self.db_file)
        
        query = '''
            SELECT timestamp, cpu_usage, memory_usage, disk_usage, active_connections
            FROM server_stats 
            WHERE timestamp > datetime('now', '-{} hours')
            ORDER BY timestamp
        '''.format(hours)
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if not df.empty:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            return df.to_dict('records')
        return []
    
    def create_charts(self):
        """Create Plotly charts for dashboard"""
        data = self.get_historical_stats(24)
        
        if not data:
            return {}
        
        df = pd.DataFrame(data)
        
        # CPU Usage Chart
        cpu_chart = go.Scatter(
            x=df['timestamp'],
            y=df['cpu_usage'],
            mode='lines+markers',
            name='CPU Usage (%)',
            line=dict(color='#ff6b6b', width=2)
        )
        
        # Memory Usage Chart
        memory_chart = go.Scatter(
            x=df['timestamp'],
            y=df['memory_usage'],
            mode='lines+markers',
            name='Memory Usage (%)',
            line=dict(color='#4ecdc4', width=2)
        )
        
        # Active Connections Chart
        connections_chart = go.Scatter(
            x=df['timestamp'],
            y=df['active_connections'],
            mode='lines+markers',
            name='Active Connections',
            line=dict(color='#45b7d1', width=2)
        )
        
        return {
            'cpu_chart': json.dumps([cpu_chart], cls=plotly.utils.PlotlyJSONEncoder),
            'memory_chart': json.dumps([memory_chart], cls=plotly.utils.PlotlyJSONEncoder),
            'connections_chart': json.dumps([connections_chart], cls=plotly.utils.PlotlyJSONEncoder)
        }
    
    def check_alerts(self):
        """Check for system alerts"""
        stats = self.get_server_stats()
        alerts = []
        
        if 'error' not in stats:
            # CPU Alert
            if stats['cpu_usage'] > 80:
                alerts.append({
                    'type': 'cpu_high',
                    'severity': 'warning' if stats['cpu_usage'] < 90 else 'critical',
                    'message': f"High CPU usage: {stats['cpu_usage']:.1f}%"
                })
            
            # Memory Alert
            if stats['memory_usage'] > 85:
                alerts.append({
                    'type': 'memory_high',
                    'severity': 'warning' if stats['memory_usage'] < 95 else 'critical',
                    'message': f"High memory usage: {stats['memory_usage']:.1f}%"
                })
            
            # Disk Alert
            if stats['disk_usage'] > 90:
                alerts.append({
                    'type': 'disk_full',
                    'severity': 'critical',
                    'message': f"Disk space critical: {stats['disk_usage']:.1f}% used"
                })
        
        # Save alerts to database
        if alerts:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            for alert in alerts:
                cursor.execute('''
                    INSERT INTO alerts (alert_type, severity, message)
                    VALUES (?, ?, ?)
                ''', (alert['type'], alert['severity'], alert['message']))
            
            conn.commit()
            conn.close()
        
        return alerts
    
    def get_recent_alerts(self, limit=10):
        """Get recent alerts"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM alerts 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (limit,))
        
        alerts = cursor.fetchall()
        conn.close()
        
        return [dict(zip([col[0] for col in cursor.description], alert)) for alert in alerts]

# Initialize monitor
monitor = VPNMonitor()

# Background task for collecting stats
def background_stats_collector():
    """Background task to collect statistics"""
    while True:
        try:
            monitor.save_stats()
            monitor.check_alerts()
            time.sleep(REFRESH_INTERVAL)
        except Exception as e:
            print(f"Background task error: {e}")
            time.sleep(30)

# Start background thread
stats_thread = threading.Thread(target=background_stats_collector, daemon=True)
stats_thread.start()

# Routes
@app.route('/')
def dashboard():
    """Main monitoring dashboard"""
    stats = monitor.get_server_stats()
    clients = monitor.get_connected_clients()
    alerts = monitor.get_recent_alerts(5)
    charts = monitor.create_charts()
    
    return render_template('dashboard.html', 
                         stats=stats, 
                         clients=clients, 
                         alerts=alerts,
                         charts=charts,
                         refresh_interval=REFRESH_INTERVAL)

@app.route('/api/stats')
def api_stats():
    """API endpoint for real-time statistics"""
    stats = monitor.get_server_stats()
    clients = monitor.get_connected_clients()
    
    return jsonify({
        'server': stats,
        'clients': clients,
        'client_count': len(clients),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/charts')
def api_charts():
    """API endpoint for chart data"""
    charts = monitor.create_charts()
    return jsonify(charts)

@app.route('/api/alerts')
def api_alerts():
    """API endpoint for alerts"""
    alerts = monitor.get_recent_alerts(20)
    return jsonify({
        'alerts': alerts,
        'count': len(alerts),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/historical/<int:hours>')
def api_historical(hours):
    """API endpoint for historical data"""
    data = monitor.get_historical_stats(hours)
    return jsonify({
        'data': data,
        'count': len(data),
        'hours': hours,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/clients')
def clients_page():
    """Connected clients page"""
    clients = monitor.get_connected_clients()
    return render_template('clients.html', clients=clients)

@app.route('/logs')
def logs_page():
    """System logs page"""
    return render_template('logs.html')

@app.route('/alerts')
def alerts_page():
    """Alerts management page"""
    alerts = monitor.get_recent_alerts(50)
    return render_template('alerts.html', alerts=alerts)

@app.route('/settings')
def settings_page():
    """Settings page"""
    return render_template('settings.html')

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'vpn-monitoring',
        'version': '1.0.0'
    })

if __name__ == '__main__':
    print("🚀 Starting VPN Monitoring Dashboard...")
    print(f"📊 Dashboard: http://localhost:3000")
    print(f"🔄 Refresh interval: {REFRESH_INTERVAL}s")
    print(f"📡 VPN Server: {VPN_SERVER_HOST}:{VPN_SERVER_PORT}")
    
    app.run(host='0.0.0.0', port=3000, debug=False, threaded=True)
