#!/usr/bin/env python3
"""
Script de déconnexion d'urgence pour FREE VPN
Restaure la connexion internet normale
"""

import sys
import subprocess
import winreg

def disable_windows_proxy():
    """Désactive le proxy Windows"""
    try:
        print("🔄 Désactivation du proxy Windows...")
        
        # Ouvrir la clé de registre
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                           r"Software\Microsoft\Windows\CurrentVersion\Internet Settings", 
                           0, winreg.KEY_SET_VALUE)
        
        # Désactiver le proxy
        winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 0)
        winreg.SetValueEx(key, "ProxyServer", 0, winreg.REG_SZ, "")
        
        winreg.CloseKey(key)
        
        # Actualiser les paramètres Internet Explorer
        subprocess.run(['rundll32.exe', 'wininet.dll,InternetSetOption'], 
                      capture_output=True, timeout=10)
        
        print("✅ Proxy Windows désactivé avec succès!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la désactivation du proxy: {e}")
        return False

def kill_vpn_processes():
    """Arrête tous les processus VPN"""
    try:
        print("🔄 Arrêt des processus VPN...")
        
        # Arrêter les processus Python VPN
        subprocess.run(['taskkill', '/F', '/IM', 'python.exe'], 
                      capture_output=True)
        
        print("✅ Processus VPN arrêtés!")
        return True
        
    except Exception as e:
        print(f"⚠️ Erreur lors de l'arrêt des processus: {e}")
        return False

def flush_dns():
    """Vide le cache DNS"""
    try:
        print("🔄 Vidage du cache DNS...")
        subprocess.run(['ipconfig', '/flushdns'], capture_output=True)
        print("✅ Cache DNS vidé!")
        return True
    except Exception as e:
        print(f"⚠️ Erreur lors du vidage DNS: {e}")
        return False

def main():
    print("🚨 FREE VPN - Déconnexion d'urgence")
    print("=" * 50)
    
    # Désactiver le proxy
    proxy_disabled = disable_windows_proxy()
    
    # Arrêter les processus VPN
    processes_killed = kill_vpn_processes()
    
    # Vider le cache DNS
    dns_flushed = flush_dns()
    
    print("\n📊 Résultats:")
    print(f"🔧 Proxy désactivé: {'✅' if proxy_disabled else '❌'}")
    print(f"🛑 Processus arrêtés: {'✅' if processes_killed else '❌'}")
    print(f"🌐 DNS vidé: {'✅' if dns_flushed else '❌'}")
    
    if proxy_disabled:
        print("\n✅ CONNEXION INTERNET RESTAURÉE!")
        print("🌐 Vous pouvez maintenant accéder à Google et autres sites")
        print("🔄 Redémarrez votre navigateur si nécessaire")
    else:
        print("\n❌ Problème lors de la restauration")
        print("🔧 Essayez de redémarrer votre ordinateur")
    
    print("\n💡 Pour éviter ce problème à l'avenir:")
    print("   - Utilisez toujours le bouton 'Disconnect' dans l'interface VPN")
    print("   - Ou lancez ce script en cas d'urgence")
    
    input("\nAppuyez sur Entrée pour fermer...")

if __name__ == "__main__":
    main()
