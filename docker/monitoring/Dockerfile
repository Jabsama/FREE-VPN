# =============================================================================
# VPN Monitoring Dashboard - Docker Image
# Advanced monitoring with real-time statistics and alerts
# =============================================================================

FROM python:3.11-alpine

# Install system dependencies
RUN apk add --no-cache \
    gcc \
    musl-dev \
    linux-headers \
    curl \
    bash \
    && rm -rf /var/cache/apk/*

# Set working directory
WORKDIR /opt/monitoring

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create necessary directories
RUN mkdir -p data templates static logs

# Set permissions
RUN chmod +x *.py

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:3000/health || exit 1

# Run application
CMD ["python3", "app.py"]
