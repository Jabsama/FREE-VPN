#!/usr/bin/env python3
"""
VoltageVPN Quick Start Script
One-click launcher for VoltageVPN
"""

import subprocess
import sys
import os
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    missing = []
    
    try:
        import flask
    except ImportError:
        missing.append('flask')
    
    try:
        import flask_cors
    except ImportError:
        missing.append('flask-cors')
    
    try:
        import requests
    except ImportError:
        missing.append('requests')
    
    return missing

def install_dependencies(missing):
    """Install missing dependencies"""
    print("📦 Installing missing dependencies...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing)
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def check_openvpn():
    """Check if OpenVPN is available"""
    try:
        subprocess.run(['openvpn', '--version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def main():
    print("⚡ VoltageVPN Quick Start")
    print("=" * 40)
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ required")
        print("   Current version:", sys.version)
        return
    
    print("✅ Python version OK")
    
    # Check dependencies
    missing = check_dependencies()
    if missing:
        print(f"📦 Missing dependencies: {', '.join(missing)}")
        if not install_dependencies(missing):
            return
    else:
        print("✅ All dependencies available")
    
    # Check OpenVPN
    if check_openvpn():
        print("✅ OpenVPN found - Real VPN possible")
        vpn_mode = "REAL VPN (changes IP on ALL websites)"
    else:
        print("⚠️  OpenVPN not found - Install for real VPN")
        print("   Windows: winget install OpenVPN.OpenVPN")
        print("   Linux: sudo apt install openvpn")
        print("   macOS: brew install openvpn")
        vpn_mode = "Browser proxy mode"
    
    print()
    print("🚀 Starting VoltageVPN...")
    print(f"🎯 Mode: {vpn_mode}")
    print("🌐 Dashboard will open at: http://localhost:8080")
    print()
    print("Press Ctrl+C to stop VoltageVPN")
    print("=" * 40)
    
    # Start VoltageVPN
    try:
        if Path('voltagevpn.py').exists():
            subprocess.run([sys.executable, 'voltagevpn.py'])
        else:
            print("❌ voltagevpn.py not found!")
            print("   Make sure you're in the VoltageVPN directory")
    except KeyboardInterrupt:
        print("\n👋 VoltageVPN stopped by user")
    except Exception as e:
        print(f"❌ Error starting VoltageVPN: {e}")

if __name__ == '__main__':
    main()
