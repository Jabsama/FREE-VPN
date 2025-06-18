#!/usr/bin/env python3
"""
VoltageVPN Configuration
Secure configuration management for VPN servers
"""

import os
from typing import Dict, Any

# VPN Server Configuration
# Note: These are public demo credentials for free VPN services
# Not actual sensitive credentials
VPN_DEMO_CREDENTIALS = {
    'demo_user': 'proton_free',
    'demo_pass': 'proton_free'
}

def get_server_config() -> Dict[str, Dict[str, Any]]:
    """
    Get VPN server configuration
    Uses environment variables if available, falls back to demo credentials
    """
    
    # Try to get credentials from environment variables first
    vpn_username = os.getenv('VPN_USERNAME', VPN_DEMO_CREDENTIALS['demo_user'])
    vpn_password = os.getenv('VPN_PASSWORD', VPN_DEMO_CREDENTIALS['demo_pass'])
    
    return {
        'voltage_usa_east': {
            'name': 'VoltageVPN USA East',
            'flag': '🇺🇸',
            'location': 'New York, USA',
            'host': 'us-free-01.protonvpn.net',
            'port': 1194,
            'protocol': 'udp',
            'username': vpn_username,
            'password': vpn_password,
            'speed': '100 Mbps',
            'load': '23%',
            'ping': '12ms',
            'status': 'online'
        },
        'voltage_usa_west': {
            'name': 'VoltageVPN USA West',
            'flag': '🇺🇸',
            'location': 'Los Angeles, USA',
            'host': 'us-free-02.protonvpn.net',
            'port': 1194,
            'protocol': 'udp',
            'username': vpn_username,
            'password': vpn_password,
            'speed': '100 Mbps',
            'load': '31%',
            'ping': '8ms',
            'status': 'online'
        },
        'voltage_uk': {
            'name': 'VoltageVPN United Kingdom',
            'flag': '🇬🇧',
            'location': 'London, UK',
            'host': 'uk-free-01.protonvpn.net',
            'port': 1194,
            'protocol': 'udp',
            'username': vpn_username,
            'password': vpn_password,
            'speed': '100 Mbps',
            'load': '18%',
            'ping': '15ms',
            'status': 'online'
        },
        'voltage_germany': {
            'name': 'VoltageVPN Germany',
            'flag': '🇩🇪',
            'location': 'Frankfurt, Germany',
            'host': 'de-free-01.protonvpn.net',
            'port': 1194,
            'protocol': 'udp',
            'username': vpn_username,
            'password': vpn_password,
            'speed': '100 Mbps',
            'load': '27%',
            'ping': '10ms',
            'status': 'online'
        },
        'voltage_netherlands': {
            'name': 'VoltageVPN Netherlands',
            'flag': '🇳🇱',
            'location': 'Amsterdam, Netherlands',
            'host': 'nl-free-01.protonvpn.net',
            'port': 1194,
            'protocol': 'udp',
            'username': vpn_username,
            'password': vpn_password,
            'speed': '100 Mbps',
            'load': '15%',
            'ping': '12ms',
            'status': 'online'
        },
        'voltage_japan': {
            'name': 'VoltageVPN Japan',
            'flag': '🇯🇵',
            'location': 'Tokyo, Japan',
            'host': 'jp-free-01.protonvpn.net',
            'port': 1194,
            'protocol': 'udp',
            'username': vpn_username,
            'password': vpn_password,
            'speed': '100 Mbps',
            'load': '22%',
            'ping': '25ms',
            'status': 'online'
        }
    }

def get_mobile_server_config() -> Dict[str, Dict[str, Any]]:
    """
    Get mobile-optimized VPN server configuration
    """
    
    # Try to get credentials from environment variables first
    vpn_username = os.getenv('VPN_USERNAME', VPN_DEMO_CREDENTIALS['demo_user'])
    vpn_password = os.getenv('VPN_PASSWORD', VPN_DEMO_CREDENTIALS['demo_pass'])
    
    return {
        'mobile_usa_east': {
            'name': 'VoltageVPN USA East',
            'flag': '🇺🇸',
            'location': 'New York, USA',
            'host': 'us-free-01.protonvpn.net',
            'port': 1194,
            'protocol': 'udp',
            'username': vpn_username,
            'password': vpn_password,
            'speed': '100 Mbps',
            'load': '23%',
            'ping': '12ms',
            'status': 'online',
            'mobile_optimized': True
        },
        'mobile_usa_west': {
            'name': 'VoltageVPN USA West',
            'flag': '🇺🇸',
            'location': 'Los Angeles, USA',
            'host': 'us-free-02.protonvpn.net',
            'port': 1194,
            'protocol': 'udp',
            'username': vpn_username,
            'password': vpn_password,
            'speed': '100 Mbps',
            'load': '31%',
            'ping': '8ms',
            'status': 'online',
            'mobile_optimized': True
        },
        'mobile_uk': {
            'name': 'VoltageVPN United Kingdom',
            'flag': '🇬🇧',
            'location': 'London, UK',
            'host': 'uk-free-01.protonvpn.net',
            'port': 1194,
            'protocol': 'udp',
            'username': vpn_username,
            'password': vpn_password,
            'speed': '100 Mbps',
            'load': '18%',
            'ping': '15ms',
            'status': 'online',
            'mobile_optimized': True
        },
        'mobile_germany': {
            'name': 'VoltageVPN Germany',
            'flag': '🇩🇪',
            'location': 'Frankfurt, Germany',
            'host': 'de-free-01.protonvpn.net',
            'port': 1194,
            'protocol': 'udp',
            'username': vpn_username,
            'password': vpn_password,
            'speed': '100 Mbps',
            'load': '27%',
            'ping': '10ms',
            'status': 'online',
            'mobile_optimized': True
        },
        'mobile_netherlands': {
            'name': 'VoltageVPN Netherlands',
            'flag': '🇳🇱',
            'location': 'Amsterdam, Netherlands',
            'host': 'nl-free-01.protonvpn.net',
            'port': 1194,
            'protocol': 'udp',
            'username': vpn_username,
            'password': vpn_password,
            'speed': '100 Mbps',
            'load': '15%',
            'ping': '12ms',
            'status': 'online',
            'mobile_optimized': True
        },
        'mobile_japan': {
            'name': 'VoltageVPN Japan',
            'flag': '🇯🇵',
            'location': 'Tokyo, Japan',
            'host': 'jp-free-01.protonvpn.net',
            'port': 1194,
            'protocol': 'udp',
            'username': vpn_username,
            'password': vpn_password,
            'speed': '100 Mbps',
            'load': '22%',
            'ping': '25ms',
            'status': 'online',
            'mobile_optimized': True
        }
    }
