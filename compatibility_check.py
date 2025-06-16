#!/usr/bin/env python3
"""
Production Compatibility Check for VPN Integration
Helps AI systems determine the best VPN mode for production deployment
"""

import sys
import subprocess
import importlib
import platform
import socket
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    return {
        'compatible': version >= (3, 7),
        'version': f"{version.major}.{version.minor}.{version.micro}",
        'required': '3.7+',
        'status': 'OK' if version >= (3, 7) else 'UPGRADE_NEEDED'
    }

def check_dependencies():
    """Check if required Python packages are available"""
    dependencies = {
        'flask': {'required': True, 'available': False, 'version': None},
        'flask_cors': {'required': True, 'available': False, 'version': None},
        'requests': {'required': True, 'available': False, 'version': None},
        'subprocess': {'required': True, 'available': True, 'version': 'builtin'},
        'socket': {'required': True, 'available': True, 'version': 'builtin'}
    }
    
    for package, info in dependencies.items():
        if package in ['subprocess', 'socket']:
            continue
            
        try:
            if package == 'flask_cors':
                module = importlib.import_module('flask_cors')
            else:
                module = importlib.import_module(package)
            
            info['available'] = True
            info['version'] = getattr(module, '__version__', 'unknown')
        except ImportError:
            info['available'] = False
    
    return dependencies

def check_openvpn():
    """Check if OpenVPN is installed and accessible"""
    try:
        result = subprocess.run(['openvpn', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            version_line = result.stderr.split('\n')[0] if result.stderr else result.stdout.split('\n')[0]
            return {
                'available': True,
                'version': version_line.strip(),
                'status': 'INSTALLED'
            }
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
        pass
    
    return {
        'available': False,
        'version': None,
        'status': 'NOT_INSTALLED'
    }

def check_admin_privileges():
    """Check if running with administrator/root privileges"""
    try:
        if platform.system() == 'Windows':
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
            return {
                'has_admin': bool(is_admin),
                'method': 'Windows UAC',
                'status': 'ADMIN' if is_admin else 'USER'
            }
        else:
            is_root = os.geteuid() == 0
            return {
                'has_admin': is_root,
                'method': 'Unix UID',
                'status': 'ROOT' if is_root else 'USER'
            }
    except Exception:
        return {
            'has_admin': False,
            'method': 'unknown',
            'status': 'UNKNOWN'
        }

def check_network_connectivity():
    """Check internet connectivity and port availability"""
    connectivity = {
        'internet': False,
        'port_8080_available': False,
        'dns_resolution': False
    }
    
    # Test internet connectivity
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        connectivity['internet'] = True
    except OSError:
        pass
    
    # Test DNS resolution
    try:
        socket.gethostbyname('google.com')
        connectivity['dns_resolution'] = True
    except socket.gaierror:
        pass
    
    # Test port 8080 availability
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('localhost', 8080))
        sock.close()
        connectivity['port_8080_available'] = True
    except OSError:
        pass
    
    return connectivity

def determine_best_vpn_mode(checks):
    """Determine the best VPN mode based on system capabilities"""
    python_ok = checks['python']['compatible']
    deps_ok = all(dep['available'] for dep in checks['dependencies'].values() if dep['required'])
    openvpn_ok = checks['openvpn']['available']
    admin_ok = checks['admin']['has_admin']
    network_ok = checks['network']['internet']
    
    if python_ok and deps_ok and openvpn_ok and admin_ok and network_ok:
        return {
            'mode': 'real',
            'description': 'Real VPN with actual IP changing',
            'capabilities': ['change_server_ip', 'route_all_traffic', 'full_vpn'],
            'limitations': [],
            'confidence': 'high'
        }
    elif python_ok and deps_ok and network_ok:
        return {
            'mode': 'zero',
            'description': 'Zero Install browser proxy',
            'capabilities': ['proxy_requests', 'browser_routing'],
            'limitations': ['no_server_ip_change', 'proxy_only'],
            'confidence': 'medium'
        }
    elif python_ok and network_ok:
        return {
            'mode': 'demo',
            'description': 'Demo mode for testing',
            'capabilities': ['simulation', 'testing'],
            'limitations': ['no_real_vpn', 'no_ip_change'],
            'confidence': 'low'
        }
    else:
        return {
            'mode': 'none',
            'description': 'System not compatible',
            'capabilities': [],
            'limitations': ['missing_requirements'],
            'confidence': 'none'
        }

def generate_installation_commands(checks, recommended_mode):
    """Generate installation commands based on system and mode"""
    commands = []
    
    # Python dependencies
    missing_deps = [name for name, info in checks['dependencies'].items() 
                   if info['required'] and not info['available']]
    
    if missing_deps:
        if platform.system() == 'Windows':
            commands.append(f"pip install {' '.join(missing_deps)}")
        else:
            commands.append(f"pip3 install {' '.join(missing_deps)}")
    
    # OpenVPN installation (if needed for real mode)
    if recommended_mode['mode'] == 'real' and not checks['openvpn']['available']:
        system = platform.system().lower()
        if system == 'linux':
            if Path('/etc/debian_version').exists():
                commands.append("sudo apt update && sudo apt install openvpn")
            elif Path('/etc/redhat-release').exists():
                commands.append("sudo yum install openvpn")
            else:
                commands.append("# Install OpenVPN using your distribution's package manager")
        elif system == 'darwin':  # macOS
            commands.append("brew install openvpn")
        elif system == 'windows':
            commands.append("winget install OpenVPN.OpenVPN")
    
    # Start command
    commands.append("python unified_vpn.py")
    
    return commands

def run_compatibility_check():
    """Run complete compatibility check"""
    print("🔍 Running VPN Production Compatibility Check...")
    print("=" * 60)
    
    checks = {
        'python': check_python_version(),
        'dependencies': check_dependencies(),
        'openvpn': check_openvpn(),
        'admin': check_admin_privileges(),
        'network': check_network_connectivity(),
        'system': {
            'platform': platform.system(),
            'architecture': platform.architecture()[0],
            'hostname': socket.gethostname()
        }
    }
    
    recommended_mode = determine_best_vpn_mode(checks)
    installation_commands = generate_installation_commands(checks, recommended_mode)
    
    # Print results
    print(f"🐍 Python: {checks['python']['version']} ({'✅' if checks['python']['compatible'] else '❌'})")
    print(f"🌐 Internet: {'✅' if checks['network']['internet'] else '❌'}")
    print(f"🔧 OpenVPN: {'✅' if checks['openvpn']['available'] else '❌'}")
    print(f"👑 Admin Rights: {'✅' if checks['admin']['has_admin'] else '❌'}")
    print(f"📦 Dependencies: {'✅' if all(d['available'] for d in checks['dependencies'].values() if d['required']) else '❌'}")
    
    print("\n📊 Dependency Status:")
    for name, info in checks['dependencies'].items():
        status = '✅' if info['available'] else '❌'
        version = f" (v{info['version']})" if info['version'] and info['version'] != 'builtin' else ''
        print(f"   {status} {name}{version}")
    
    print(f"\n🎯 Recommended VPN Mode: {recommended_mode['mode'].upper()}")
    print(f"📝 Description: {recommended_mode['description']}")
    print(f"🔧 Capabilities: {', '.join(recommended_mode['capabilities'])}")
    if recommended_mode['limitations']:
        print(f"⚠️  Limitations: {', '.join(recommended_mode['limitations'])}")
    
    print(f"\n🚀 Installation Commands:")
    for i, cmd in enumerate(installation_commands, 1):
        print(f"   {i}. {cmd}")
    
    print(f"\n📈 Confidence Level: {recommended_mode['confidence'].upper()}")
    
    # Return structured data for AI systems
    return {
        'compatibility_check': checks,
        'recommended_mode': recommended_mode,
        'installation_commands': installation_commands,
        'can_change_real_ip': recommended_mode['mode'] == 'real',
        'production_ready': recommended_mode['mode'] in ['real', 'zero'],
        'timestamp': __import__('datetime').datetime.now().isoformat()
    }

def main():
    """Main function for command line usage"""
    import json
    
    result = run_compatibility_check()
    
    # Save results to file for AI systems
    with open('compatibility_report.json', 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"\n💾 Detailed report saved to: compatibility_report.json")
    
    # Exit with appropriate code
    if result['production_ready']:
        print("✅ System is production ready!")
        sys.exit(0)
    else:
        print("❌ System needs setup before production use")
        sys.exit(1)

if __name__ == '__main__':
    main()
