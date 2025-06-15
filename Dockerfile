# =============================================================================
# Secure VPN Server - Docker Image
# Multi-stage build for optimized production image
# =============================================================================

# Build stage
FROM alpine:3.19 AS builder

# Install build dependencies
RUN apk add --no-cache \
    build-base \
    openssl-dev \
    lzo-dev \
    linux-pam-dev \
    net-tools \
    curl \
    git

# Download and compile OpenVPN from source for latest security patches
WORKDIR /tmp
RUN curl -L https://swupdate.openvpn.org/community/releases/openvpn-2.6.8.tar.gz | tar xz
WORKDIR /tmp/openvpn-2.6.8

RUN ./configure \
    --enable-iproute2 \
    --enable-plugins \
    --enable-port-share \
    --enable-crypto \
    --enable-lzo \
    --enable-lz4 \
    --disable-debug \
    --prefix=/usr/local

RUN make -j$(nproc) && make install

# Production stage
FROM alpine:3.19

# Install runtime dependencies
RUN apk add --no-cache \
    openssl \
    lzo \
    linux-pam \
    iptables \
    ip6tables \
    iproute2 \
    bash \
    curl \
    jq \
    python3 \
    py3-pip \
    supervisor \
    nginx \
    && rm -rf /var/cache/apk/*

# Copy OpenVPN from builder
COPY --from=builder /usr/local /usr/local

# Create VPN user and directories
RUN adduser -D -s /bin/bash vpnuser && \
    mkdir -p /etc/openvpn/server \
             /etc/openvpn/client \
             /var/log/openvpn \
             /var/lib/openvpn \
             /opt/vpn-manager \
             /opt/monitoring \
             /var/run/openvpn

# Set up directory permissions
RUN chown -R vpnuser:vpnuser /etc/openvpn /var/log/openvpn /var/lib/openvpn /opt/vpn-manager

# Copy VPN configuration files
COPY configs/server.conf /etc/openvpn/server/
COPY tools/secure-certificate-manager.sh /opt/vpn-manager/
COPY docker/scripts/ /opt/vpn-manager/scripts/

# Install Python dependencies for monitoring
RUN pip3 install --no-cache-dir flask psutil requests

# Copy monitoring application
COPY docker/monitoring/ /opt/monitoring/

# Copy supervisor configuration
COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Copy nginx configuration for web interface
COPY docker/nginx.conf /etc/nginx/nginx.conf

# Copy startup script
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh /opt/vpn-manager/secure-certificate-manager.sh

# Create health check script
RUN echo '#!/bin/bash' > /healthcheck.sh && \
    echo 'curl -f http://localhost:8080/health || exit 1' >> /healthcheck.sh && \
    echo 'pgrep openvpn > /dev/null || exit 1' >> /healthcheck.sh && \
    chmod +x /healthcheck.sh

# Expose ports
EXPOSE 1194/udp 8080/tcp 8443/tcp

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD /healthcheck.sh

# Set working directory
WORKDIR /opt/vpn-manager

# Use non-root user for security
USER vpnuser

# Entry point
ENTRYPOINT ["/entrypoint.sh"]
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
