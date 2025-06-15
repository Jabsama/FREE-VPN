# 🐳 Docker Deployment Guide

## Vue d'ensemble

Ce guide vous explique comment déployer rapidement le serveur VPN avec Docker, incluant toutes les améliorations de sécurité, monitoring et gestion automatisée.

## 🚀 Déploiement Rapide

### Windows
```cmd
# Exécuter en tant qu'administrateur
DOCKER-DEPLOY.bat
```

### Linux/macOS
```bash
# Rendre le script exécutable
chmod +x docker-deploy.sh

# Exécuter le script
./docker-deploy.sh
```

## 📋 Prérequis

- **Docker Desktop** (Windows/macOS) ou **Docker Engine** (Linux)
- **Docker Compose** v2.0+
- **8 GB RAM** minimum recommandé
- **Ports disponibles**: 80, 443, 1194, 3000, 8080, 8443

## 🏗️ Architecture Docker

### Services Déployés

| Service | Description | Port | Accès |
|---------|-------------|------|-------|
| **vpn-server** | Serveur OpenVPN principal | 1194/UDP | VPN |
| **vpn-monitor** | Dashboard de monitoring | 3000/TCP | http://localhost:3000 |
| **vpn-database** | Base PostgreSQL | 5432/TCP | Interne |
| **vpn-redis** | Cache Redis | 6379/TCP | Interne |
| **vpn-proxy** | Reverse proxy Nginx | 80,443/TCP | http://localhost |

### Volumes Persistants

- `vpn-config` - Configurations OpenVPN
- `vpn-certs` - Certificats et clés
- `vpn-secure` - Stockage sécurisé des mots de passe
- `vpn-logs` - Logs du serveur
- `monitoring-data` - Données de monitoring
- `postgres-data` - Base de données
- `redis-data` - Cache Redis

## 🔐 Sécurité Renforcée

### Gestion des Certificats

Le système utilise le **Secure Certificate Manager** avec :

- **Chiffrement AES-256** des clés privées
- **Stockage sécurisé** des mots de passe
- **Rotation automatique** des certificats
- **Sauvegarde chiffrée** avec GPG
- **Vérification** de la chaîne de certificats

### Fonctionnalités de Sécurité

```bash
# Accéder au gestionnaire de certificats
docker exec -it secure-vpn-server /opt/vpn-manager/secure-certificate-manager.sh

# Options disponibles :
# 1. Créer nouveaux certificats
# 2. Créer certificat serveur
# 3. Créer certificat client
# 4. Sauvegarder certificats
# 5. Vérifier certificats
# 6. Rotation des certificats
```

## 📊 Monitoring Avancé

### Dashboard de Monitoring

Accès : **http://localhost:3000**

**Fonctionnalités :**
- 📈 **Statistiques temps réel** (CPU, RAM, Disque, Réseau)
- 👥 **Clients connectés** avec détails de session
- 🚨 **Alertes automatiques** (seuils configurables)
- 📊 **Graphiques historiques** (24h, 7j, 30j)
- 📝 **Logs système** avec filtrage
- 🔔 **Notifications email** pour les alertes critiques

### Métriques Surveillées

- **Serveur** : CPU, Mémoire, Disque, Charge système
- **Réseau** : Bande passante, Paquets, Connexions actives
- **VPN** : Clients connectés, Trafic par utilisateur
- **Sécurité** : Tentatives de connexion, Erreurs d'authentification

### API de Monitoring

```bash
# Statistiques serveur
curl http://localhost:3000/api/stats

# Clients connectés
curl http://localhost:3000/api/clients

# Alertes récentes
curl http://localhost:3000/api/alerts

# Données historiques (24h)
curl http://localhost:3000/api/historical/24
```

## 🔧 Gestion et Maintenance

### Commandes Docker Compose

```bash
# Démarrer tous les services
docker compose up -d

# Voir les logs en temps réel
docker compose logs -f

# Redémarrer un service spécifique
docker compose restart vpn-server

# Arrêter tous les services
docker compose down

# Mise à jour des images
docker compose pull && docker compose up -d

# Nettoyer les volumes (ATTENTION: perte de données)
docker compose down -v
```

### Sauvegarde et Restauration

```bash
# Sauvegarde complète
docker exec secure-vpn-server /opt/vpn-manager/secure-certificate-manager.sh backup

# Sauvegarde des volumes
docker run --rm -v vpn-certs:/data -v $(pwd):/backup alpine tar czf /backup/vpn-backup.tar.gz /data

# Restauration
docker run --rm -v vpn-certs:/data -v $(pwd):/backup alpine tar xzf /backup/vpn-backup.tar.gz -C /
```

## ⚙️ Configuration Avancée

### Variables d'Environnement

Modifiez le fichier `docker-compose.yml` :

```yaml
environment:
  - VPN_SERVER_NAME=mon-vpn.example.com
  - VPN_SERVER_IP=10.8.0.1
  - VPN_CLIENT_NETWORK=10.8.0.0
  - VPN_CLIENT_NETMASK=255.255.255.0
  - VPN_DNS1=8.8.8.8
  - VPN_DNS2=1.1.1.1
  - WEB_ADMIN_USER=admin
  - WEB_ADMIN_PASS=MonMotDePasseSecurise!
  - MONITORING_ENABLED=true
  - LOG_LEVEL=INFO
```

### Configuration Personnalisée

Placez vos fichiers de configuration dans :
- `docker/custom-configs/` - Configurations personnalisées
- `docker/nginx/ssl/` - Certificats SSL pour Nginx

## 🚨 Dépannage

### Problèmes Courants

**1. Port 1194 déjà utilisé**
```bash
# Vérifier les ports utilisés
netstat -tulpn | grep 1194

# Changer le port dans docker-compose.yml
ports:
  - "1195:1194/udp"
```

**2. Certificats non générés**
```bash
# Régénérer manuellement
docker exec -it secure-vpn-server /opt/vpn-manager/secure-certificate-manager.sh create-all
```

**3. Monitoring inaccessible**
```bash
# Vérifier le statut du service
docker compose ps vpn-monitor

# Voir les logs
docker compose logs vpn-monitor
```

**4. Base de données corrompue**
```bash
# Réinitialiser la base
docker compose down
docker volume rm my-vpn_postgres-data
docker compose up -d
```

### Logs et Diagnostics

```bash
# Logs du serveur VPN
docker compose logs vpn-server

# Logs de monitoring
docker compose logs vpn-monitor

# Logs de la base de données
docker compose logs vpn-database

# Entrer dans un conteneur pour diagnostic
docker exec -it secure-vpn-server bash
```

## 🔒 Sécurité en Production

### Recommandations

1. **Changer les mots de passe par défaut**
2. **Utiliser des certificats SSL valides**
3. **Configurer un firewall**
4. **Activer les sauvegardes automatiques**
5. **Surveiller les logs de sécurité**
6. **Mettre à jour régulièrement**

### Configuration Firewall

```bash
# UFW (Ubuntu)
sudo ufw allow 1194/udp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 3000/tcp  # Monitoring (restreindre en production)

# iptables
iptables -A INPUT -p udp --dport 1194 -j ACCEPT
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT
```

## 📈 Performance et Optimisation

### Recommandations Matériel

| Utilisateurs | CPU | RAM | Disque | Bande Passante |
|--------------|-----|-----|--------|----------------|
| 1-10 | 1 vCPU | 2 GB | 20 GB | 100 Mbps |
| 10-50 | 2 vCPU | 4 GB | 50 GB | 500 Mbps |
| 50-100 | 4 vCPU | 8 GB | 100 GB | 1 Gbps |
| 100+ | 8+ vCPU | 16+ GB | 200+ GB | 10+ Gbps |

### Optimisations

```yaml
# Dans docker-compose.yml
services:
  vpn-server:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 4G
        reservations:
          cpus: '1.0'
          memory: 2G
```

## 🆘 Support

### Ressources

- **Documentation** : `docs/` dans le projet
- **Issues GitHub** : Pour signaler des bugs
- **Monitoring** : Dashboard temps réel à http://localhost:3000
- **Logs** : `docker compose logs -f`

### Contact

Pour un support professionnel ou des questions spécifiques, consultez la documentation du projet principal.

---

## 🎉 Félicitations !

Votre serveur VPN Docker est maintenant déployé avec :

✅ **Sécurité renforcée** - Certificats chiffrés et gestion sécurisée  
✅ **Monitoring complet** - Dashboard temps réel et alertes  
✅ **Déploiement automatisé** - Un clic pour tout installer  
✅ **Haute disponibilité** - Services redondants et health checks  
✅ **Facilité de maintenance** - Commandes simples et sauvegardes  

**Profitez de votre VPN sécurisé et professionnel !** 🚀
