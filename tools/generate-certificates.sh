#!/bin/bash

echo "========================================"
echo "China VPN Certificate Generator"
echo "========================================"
echo

# Create certificates directory
mkdir -p ../certificates
cd ../certificates

echo "Generating CA (Certificate Authority)..."

# Generate CA private key
openssl genrsa -out ca.key 4096

# Generate CA certificate
openssl req -new -x509 -days 3650 -key ca.key -out ca.crt -subj "/C=CN/ST=Beijing/L=Beijing/O=China VPN/OU=IT Department/CN=China VPN CA"

echo "Generating Server Certificate..."

# Generate server private key
openssl genrsa -out server.key 4096

# Generate server certificate request
openssl req -new -key server.key -out server.csr -subj "/C=CN/ST=Beijing/L=Beijing/O=China VPN/OU=IT Department/CN=china-vpn-server.example.com"

# Generate server certificate
openssl x509 -req -days 3650 -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt

echo "Generating Client Certificate..."

# Generate client private key
openssl genrsa -out client.key 4096

# Generate client certificate request
openssl req -new -key client.key -out client.csr -subj "/C=CN/ST=Beijing/L=Beijing/O=China VPN/OU=IT Department/CN=china-vpn-client"

# Generate client certificate
openssl x509 -req -days 3650 -in client.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out client.crt

echo "Generating TLS Auth Key..."

# Generate TLS auth key
openvpn --genkey --secret ta.key

echo "Generating Diffie-Hellman parameters..."

# Generate DH parameters (this may take a while)
openssl dhparam -out dh4096.pem 4096

echo
echo "========================================"
echo "Certificate Generation Complete!"
echo "========================================"
echo
echo "Generated files:"
echo "  ca.crt      - Certificate Authority certificate"
echo "  ca.key      - Certificate Authority private key"
echo "  server.crt  - Server certificate"
echo "  server.key  - Server private key"
echo "  client.crt  - Client certificate"
echo "  client.key  - Client private key"
echo "  ta.key      - TLS authentication key"
echo "  dh4096.pem  - Diffie-Hellman parameters"
echo
echo "Next steps:"
echo "1. Copy ca.crt, client.crt, client.key, and ta.key contents"
echo "2. Paste them into the china-vpn.ovpn configuration file"
echo "3. Set up your VPN server with server.crt, server.key, ca.crt, ta.key, and dh4096.pem"
echo

# Clean up certificate signing requests
rm -f server.csr client.csr ca.srl

echo "Certificate files are ready in the certificates/ directory"
