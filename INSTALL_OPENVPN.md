# 🔧 OpenVPN Installation Guide

Pour que le VPN fonctionne réellement et permette de naviguer sur internet, OpenVPN doit être installé sur votre système.

## 🪟 Windows

### Option 1: Installation automatique
```bash
# Télécharger et installer OpenVPN
winget install OpenVPN.OpenVPN
```

### Option 2: Installation manuelle
1. Téléchargez OpenVPN depuis: https://openvpn.net/community-downloads/
2. Exécutez l'installateur en tant qu'administrateur
3. Redémarrez votre ordinateur

### Option 3: Chocolatey
```bash
choco install openvpn
```

## 🐧 Linux (Ubuntu/Debian)

```bash
# Mettre à jour les paquets
sudo apt update

# Installer OpenVPN
sudo apt install openvpn

# Vérifier l'installation
openvpn --version
```

## 🐧 Linux (CentOS/RHEL/Fedora)

```bash
# CentOS/RHEL
sudo yum install openvpn

# Fedora
sudo dnf install openvpn

# Vérifier l'installation
openvpn --version
```

## 🍎 macOS

### Option 1: Homebrew
```bash
# Installer Homebrew si pas déjà fait
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Installer OpenVPN
brew install openvpn
```

### Option 2: Installation manuelle
1. Téléchargez Tunnelblick: https://tunnelblick.net/
2. Installez Tunnelblick (inclut OpenVPN)

## ✅ Vérification de l'installation

Après installation, vérifiez qu'OpenVPN fonctionne :

```bash
openvpn --version
```

Vous devriez voir quelque chose comme :
```
OpenVPN 2.5.x x86_64-pc-linux-gnu
```

## 🚀 Lancement du VPN réel

Une fois OpenVPN installé :

```bash
# Lancer le serveur VPN réel
python real_vpn_api.py
```

## 🌐 Fonctionnalités du VPN réel

- ✅ **Navigation internet réelle** - Tout le trafic passe par le VPN
- ✅ **Changement d'IP vérifié** - Votre IP change vraiment
- ✅ **Serveurs gratuits** - Utilise ProtonVPN gratuit
- ✅ **Interface web** - Contrôle via navigateur
- ✅ **API REST** - Intégration programmatique

## 🔒 Sécurité

- Chiffrement AES-256-CBC
- Authentification SHA256
- DNS sécurisé (8.8.8.8, 8.8.4.4)
- Vérification des certificats serveur

## ⚠️ Notes importantes

1. **Privilèges administrateur** : OpenVPN peut nécessiter des privilèges élevés
2. **Pare-feu** : Assurez-vous que le port 1194 UDP n'est pas bloqué
3. **Antivirus** : Certains antivirus peuvent bloquer OpenVPN
4. **Performance** : Les serveurs gratuits peuvent être plus lents

## 🆘 Dépannage

### Erreur "OpenVPN not found"
- Vérifiez que OpenVPN est dans le PATH
- Redémarrez votre terminal/invite de commande
- Réinstallez OpenVPN

### Erreur de connexion
- Vérifiez votre connexion internet
- Essayez un autre serveur
- Vérifiez les logs dans la console

### Privilèges insuffisants
- Lancez en tant qu'administrateur (Windows)
- Utilisez sudo (Linux/macOS)

---

**Une fois OpenVPN installé, le VPN permettra vraiment de naviguer sur internet avec une IP différente !**
