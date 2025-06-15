#!/bin/bash

# =============================================================================
# Secure Certificate Manager for VPN
# Enhanced security with encrypted storage and key rotation
# =============================================================================

set -euo pipefail

# Configuration
CERT_DIR="../certificates"
SECURE_DIR="../secure-storage"
BACKUP_DIR="../cert-backups"
LOG_FILE="../logs/cert-manager.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Create secure directories
create_directories() {
    mkdir -p "$CERT_DIR" "$SECURE_DIR" "$BACKUP_DIR" "$(dirname "$LOG_FILE")"
    
    # Set secure permissions
    chmod 700 "$SECURE_DIR"
    chmod 755 "$CERT_DIR" "$BACKUP_DIR"
    
    log "Secure directories created with proper permissions"
}

# Generate secure random password
generate_password() {
    openssl rand -base64 32 | tr -d "=+/" | cut -c1-25
}

# Encrypt private key with password
encrypt_private_key() {
    local key_file="$1"
    local password="$2"
    local encrypted_file="${key_file}.enc"
    
    openssl rsa -in "$key_file" -aes256 -out "$encrypted_file" -passout pass:"$password"
    
    # Remove unencrypted key
    shred -vfz -n 3 "$key_file" 2>/dev/null || rm -f "$key_file"
    
    log "Private key encrypted: $encrypted_file"
}

# Create secure certificate authority
create_secure_ca() {
    echo -e "${BLUE}Creating Secure Certificate Authority...${NC}"
    
    cd "$CERT_DIR"
    
    # Generate CA password
    CA_PASSWORD=$(generate_password)
    echo "$CA_PASSWORD" > "$SECURE_DIR/ca_password.txt"
    chmod 600 "$SECURE_DIR/ca_password.txt"
    
    # Generate CA private key with encryption
    openssl genrsa -aes256 -out ca.key -passout pass:"$CA_PASSWORD" 4096
    
    # Generate CA certificate with enhanced security
    openssl req -new -x509 -days 3650 -key ca.key -out ca.crt \
        -passin pass:"$CA_PASSWORD" \
        -config <(cat <<EOF
[req]
distinguished_name = req_distinguished_name
x509_extensions = v3_ca
prompt = no

[req_distinguished_name]
C = CN
ST = Beijing
L = Beijing
O = Secure VPN CA
OU = Security Department
CN = Secure VPN Root CA
emailAddress = security@securevpn.local

[v3_ca]
basicConstraints = critical,CA:TRUE
keyUsage = critical,keyCertSign,cRLSign
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid:always,issuer:always
EOF
    )
    
    log "Secure CA created with encrypted private key"
}

# Generate server certificate with SAN
create_server_certificate() {
    local server_domain="$1"
    local server_ip="${2:-}"
    
    echo -e "${BLUE}Creating Server Certificate for $server_domain...${NC}"
    
    cd "$CERT_DIR"
    
    # Read CA password
    CA_PASSWORD=$(cat "$SECURE_DIR/ca_password.txt")
    
    # Generate server private key
    openssl genrsa -out server.key 4096
    
    # Create SAN configuration
    local san_config=""
    if [[ -n "$server_ip" ]]; then
        san_config="DNS:$server_domain,IP:$server_ip"
    else
        san_config="DNS:$server_domain"
    fi
    
    # Generate server certificate request
    openssl req -new -key server.key -out server.csr \
        -config <(cat <<EOF
[req]
distinguished_name = req_distinguished_name
req_extensions = v3_req
prompt = no

[req_distinguished_name]
C = CN
ST = Beijing
L = Beijing
O = Secure VPN
OU = Server Department
CN = $server_domain
emailAddress = server@securevpn.local

[v3_req]
basicConstraints = CA:FALSE
keyUsage = nonRepudiation,digitalSignature,keyEncipherment
subjectAltName = $san_config
EOF
    )
    
    # Sign server certificate
    openssl x509 -req -days 365 -in server.csr \
        -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt \
        -passin pass:"$CA_PASSWORD" \
        -extensions v3_req \
        -extfile <(cat <<EOF
[v3_req]
basicConstraints = CA:FALSE
keyUsage = nonRepudiation,digitalSignature,keyEncipherment
subjectAltName = $san_config
extendedKeyUsage = serverAuth
EOF
    )
    
    # Encrypt server private key
    SERVER_PASSWORD=$(generate_password)
    echo "$SERVER_PASSWORD" > "$SECURE_DIR/server_password.txt"
    chmod 600 "$SECURE_DIR/server_password.txt"
    
    encrypt_private_key "server.key" "$SERVER_PASSWORD"
    
    # Clean up CSR
    rm -f server.csr
    
    log "Server certificate created for $server_domain with SAN: $san_config"
}

# Generate client certificate
create_client_certificate() {
    local client_name="$1"
    
    echo -e "${BLUE}Creating Client Certificate for $client_name...${NC}"
    
    cd "$CERT_DIR"
    
    # Read CA password
    CA_PASSWORD=$(cat "$SECURE_DIR/ca_password.txt")
    
    # Generate client private key
    openssl genrsa -out "${client_name}.key" 4096
    
    # Generate client certificate request
    openssl req -new -key "${client_name}.key" -out "${client_name}.csr" \
        -config <(cat <<EOF
[req]
distinguished_name = req_distinguished_name
req_extensions = v3_req
prompt = no

[req_distinguished_name]
C = CN
ST = Beijing
L = Beijing
O = Secure VPN
OU = Client Department
CN = $client_name
emailAddress = client@securevpn.local

[v3_req]
basicConstraints = CA:FALSE
keyUsage = nonRepudiation,digitalSignature,keyEncipherment
extendedKeyUsage = clientAuth
EOF
    )
    
    # Sign client certificate
    openssl x509 -req -days 365 -in "${client_name}.csr" \
        -CA ca.crt -CAkey ca.key -CAcreateserial -out "${client_name}.crt" \
        -passin pass:"$CA_PASSWORD" \
        -extensions v3_req \
        -extfile <(cat <<EOF
[v3_req]
basicConstraints = CA:FALSE
keyUsage = nonRepudiation,digitalSignature,keyEncipherment
extendedKeyUsage = clientAuth
EOF
    )
    
    # Encrypt client private key
    CLIENT_PASSWORD=$(generate_password)
    echo "$CLIENT_PASSWORD" > "$SECURE_DIR/${client_name}_password.txt"
    chmod 600 "$SECURE_DIR/${client_name}_password.txt"
    
    encrypt_private_key "${client_name}.key" "$CLIENT_PASSWORD"
    
    # Clean up CSR
    rm -f "${client_name}.csr"
    
    log "Client certificate created for $client_name"
}

# Generate TLS auth key with enhanced security
create_tls_auth() {
    echo -e "${BLUE}Creating TLS Authentication Key...${NC}"
    
    cd "$CERT_DIR"
    
    # Generate TLS auth key
    openvpn --genkey --secret ta.key
    
    # Create backup
    cp ta.key "$BACKUP_DIR/ta.key.$(date +%Y%m%d_%H%M%S)"
    
    log "TLS authentication key created"
}

# Generate DH parameters with progress
create_dh_params() {
    local dh_size="${1:-4096}"
    
    echo -e "${BLUE}Generating Diffie-Hellman parameters ($dh_size bits)...${NC}"
    echo -e "${YELLOW}This may take several minutes...${NC}"
    
    cd "$CERT_DIR"
    
    # Generate DH parameters with progress
    openssl dhparam -out "dh${dh_size}.pem" "$dh_size"
    
    log "DH parameters ($dh_size bits) generated"
}

# Backup certificates
backup_certificates() {
    echo -e "${BLUE}Creating certificate backup...${NC}"
    
    local backup_file="$BACKUP_DIR/certificates_backup_$(date +%Y%m%d_%H%M%S).tar.gz"
    
    tar -czf "$backup_file" -C "$CERT_DIR" . -C "$SECURE_DIR" .
    
    # Encrypt backup
    BACKUP_PASSWORD=$(generate_password)
    echo "$BACKUP_PASSWORD" > "$SECURE_DIR/backup_password.txt"
    chmod 600 "$SECURE_DIR/backup_password.txt"
    
    gpg --symmetric --cipher-algo AES256 --compress-algo 1 \
        --s2k-mode 3 --s2k-digest-algo SHA512 --s2k-count 65011712 \
        --passphrase "$BACKUP_PASSWORD" --batch --yes \
        --output "${backup_file}.gpg" "$backup_file"
    
    # Remove unencrypted backup
    rm -f "$backup_file"
    
    log "Encrypted backup created: ${backup_file}.gpg"
}

# Verify certificate chain
verify_certificates() {
    echo -e "${BLUE}Verifying certificate chain...${NC}"
    
    cd "$CERT_DIR"
    
    # Verify CA certificate
    if openssl x509 -in ca.crt -text -noout > /dev/null 2>&1; then
        echo -e "${GREEN}✓ CA certificate is valid${NC}"
    else
        echo -e "${RED}✗ CA certificate is invalid${NC}"
        return 1
    fi
    
    # Verify server certificate
    if [[ -f server.crt ]]; then
        if openssl verify -CAfile ca.crt server.crt > /dev/null 2>&1; then
            echo -e "${GREEN}✓ Server certificate is valid${NC}"
        else
            echo -e "${RED}✗ Server certificate is invalid${NC}"
            return 1
        fi
    fi
    
    # Verify client certificates
    for cert in *.crt; do
        if [[ "$cert" != "ca.crt" && "$cert" != "server.crt" ]]; then
            if openssl verify -CAfile ca.crt "$cert" > /dev/null 2>&1; then
                echo -e "${GREEN}✓ Client certificate $cert is valid${NC}"
            else
                echo -e "${RED}✗ Client certificate $cert is invalid${NC}"
                return 1
            fi
        fi
    done
    
    log "Certificate verification completed successfully"
}

# Rotate certificates (renew before expiry)
rotate_certificates() {
    echo -e "${BLUE}Rotating certificates...${NC}"
    
    # Backup current certificates
    backup_certificates
    
    # Check certificate expiry
    cd "$CERT_DIR"
    
    for cert in *.crt; do
        if [[ -f "$cert" ]]; then
            expiry_date=$(openssl x509 -in "$cert" -noout -enddate | cut -d= -f2)
            expiry_epoch=$(date -d "$expiry_date" +%s)
            current_epoch=$(date +%s)
            days_until_expiry=$(( (expiry_epoch - current_epoch) / 86400 ))
            
            if [[ $days_until_expiry -lt 30 ]]; then
                echo -e "${YELLOW}Certificate $cert expires in $days_until_expiry days${NC}"
                # Here you would implement certificate renewal logic
            fi
        fi
    done
    
    log "Certificate rotation check completed"
}

# Display certificate information
show_certificate_info() {
    echo -e "${BLUE}Certificate Information:${NC}"
    
    cd "$CERT_DIR"
    
    for cert in *.crt; do
        if [[ -f "$cert" ]]; then
            echo -e "\n${YELLOW}=== $cert ===${NC}"
            openssl x509 -in "$cert" -noout -subject -issuer -dates -fingerprint
        fi
    done
}

# Main menu
show_menu() {
    echo -e "${BLUE}"
    echo "========================================"
    echo "    Secure Certificate Manager"
    echo "========================================"
    echo -e "${NC}"
    echo "1. Create new CA and certificates"
    echo "2. Create server certificate"
    echo "3. Create client certificate"
    echo "4. Create TLS auth key"
    echo "5. Generate DH parameters"
    echo "6. Backup certificates"
    echo "7. Verify certificates"
    echo "8. Rotate certificates"
    echo "9. Show certificate info"
    echo "0. Exit"
    echo
}

# Main execution
main() {
    create_directories
    
    if [[ $# -eq 0 ]]; then
        # Interactive mode
        while true; do
            show_menu
            read -p "Select option: " choice
            
            case $choice in
                1)
                    create_secure_ca
                    read -p "Server domain/IP: " server_domain
                    read -p "Server IP (optional): " server_ip
                    create_server_certificate "$server_domain" "$server_ip"
                    read -p "Client name: " client_name
                    create_client_certificate "$client_name"
                    create_tls_auth
                    create_dh_params
                    verify_certificates
                    echo -e "${GREEN}Complete certificate setup finished!${NC}"
                    ;;
                2)
                    read -p "Server domain: " server_domain
                    read -p "Server IP (optional): " server_ip
                    create_server_certificate "$server_domain" "$server_ip"
                    ;;
                3)
                    read -p "Client name: " client_name
                    create_client_certificate "$client_name"
                    ;;
                4)
                    create_tls_auth
                    ;;
                5)
                    read -p "DH key size (2048/4096): " dh_size
                    create_dh_params "${dh_size:-4096}"
                    ;;
                6)
                    backup_certificates
                    ;;
                7)
                    verify_certificates
                    ;;
                8)
                    rotate_certificates
                    ;;
                9)
                    show_certificate_info
                    ;;
                0)
                    echo -e "${GREEN}Goodbye!${NC}"
                    exit 0
                    ;;
                *)
                    echo -e "${RED}Invalid option${NC}"
                    ;;
            esac
            
            echo
            read -p "Press Enter to continue..."
        done
    else
        # Command line mode
        case "$1" in
            "create-all")
                create_secure_ca
                create_server_certificate "${2:-vpn.example.com}" "${3:-}"
                create_client_certificate "${4:-client}"
                create_tls_auth
                create_dh_params
                verify_certificates
                ;;
            "backup")
                backup_certificates
                ;;
            "verify")
                verify_certificates
                ;;
            *)
                echo "Usage: $0 [create-all domain [ip] [client_name] | backup | verify]"
                exit 1
                ;;
        esac
    fi
}

# Run main function
main "$@"
