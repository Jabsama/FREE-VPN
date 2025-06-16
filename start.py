#!/usr/bin/env python3
"""
VPN Browser API - Simple Startup Script
Quick launcher for the VPN Browser API server
"""

import subprocess
import sys
import os

def main():
    """Start the VPN Browser API server"""
    print("🚀 VPN Browser API - Starting Server...")
    print("=" * 50)
    
    # Check if the main script exists
    if not os.path.exists('vpn_browser_api.py'):
        print("❌ Error: vpn_browser_api.py not found!")
        print("Make sure you're in the correct directory.")
        sys.exit(1)
    
    try:
        # Start the main server
        subprocess.run([sys.executable, 'vpn_browser_api.py'], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
