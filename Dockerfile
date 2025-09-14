# Multi-stage hardened Docker build für MCP Docassemble Server
# Security-optimized, production-ready container

# ============================================================================
# BUILD STAGE - Dependency compilation
# ============================================================================
FROM python:3.12-slim AS builder

# Security: Create non-root build user
RUN groupadd -r build && useradd -r -g build build

# Install build dependencies (minimal set)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc6-dev \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Set up build environment
WORKDIR /build
USER build

# Copy requirements with dependency locking
COPY requirements.txt .
COPY requirements.lock .

# Install Python dependencies to user directory
RUN pip install --user --no-cache-dir --require-hashes -r requirements.lock || \
    pip install --user --no-cache-dir -r requirements.txt

# ============================================================================
# PRODUCTION STAGE - Hardened runtime
# ============================================================================
FROM python:3.12-slim AS production

# Security metadata
LABEL maintainer="MCP Docassemble Team"
LABEL description="Hardened MCP Docassemble Server"
LABEL version="1.1.0"
LABEL security.scan="enabled"

# Security: Create dedicated runtime user
RUN groupadd -r mcp --gid=1000 && \
    useradd -r -g mcp --uid=1000 --home-dir=/app --shell=/bin/false mcp

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy Python dependencies from builder stage
COPY --from=builder /home/build/.local /home/mcp/.local

# Set up application directory
WORKDIR /app
COPY --chown=mcp:mcp src/ ./src/
COPY --chown=mcp:mcp mcp_docassemble/ ./mcp_docassemble/
COPY --chown=mcp:mcp pyproject.toml requirements.txt ./

# Create necessary directories with proper permissions
RUN mkdir -p /app/logs /app/tmp /tmp/mcp \
    && chown -R mcp:mcp /app /tmp/mcp \
    && chmod 755 /app \
    && chmod 750 /app/logs /app/tmp /tmp/mcp

# Security: Switch to non-root user
USER mcp

# Set up environment
ENV PATH="/home/mcp/.local/bin:$PATH"
ENV PYTHONPATH="/app/src:/app"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Application configuration
ENV MCP_HOST=0.0.0.0
ENV MCP_PORT=8080
ENV MCP_WORKERS=4
ENV LOG_LEVEL=INFO
ENV LOG_FORMAT=json

# Docassemble configuration
ENV DOCASSEMBLE_URL=""
ENV DOCASSEMBLE_API_KEY=""

# Security configuration
ENV SECURITY_HEADERS=true
ENV RATE_LIMITING=true
ENV MAX_REQUESTS_PER_MINUTE=60

# Health check configuration
ENV HEALTH_CHECK_INTERVAL=30
ENV HEALTH_CHECK_TIMEOUT=5
ENV HEALTH_CHECK_RETRIES=3

# Create health check script
RUN echo '#!/bin/bash\ncurl -f http://localhost:8080/health || exit 1' > /app/health_check.sh \
    && chmod +x /app/health_check.sh

# Health check
HEALTHCHECK --interval=30s \
            --timeout=5s \
            --start-period=10s \
            --retries=3 \
    CMD ["/app/health_check.sh"]

# Security: Read-only root filesystem (with exceptions)
VOLUME ["/app/logs", "/app/tmp", "/tmp/mcp"]

# Expose ports
EXPOSE 8080

# Add security labels
LABEL security.capabilities="NET_BIND_SERVICE"
LABEL security.no-new-privileges="true"
LABEL security.read-only-root-filesystem="true"

# Production startup with Gunicorn
CMD ["python", "-m", "gunicorn", \
     "--bind", "0.0.0.0:8080", \
     "--workers", "4", \
     "--worker-class", "sync", \
     "--worker-connections", "1000", \
     "--max-requests", "1000", \
     "--max-requests-jitter", "50", \
     "--timeout", "30", \
     "--keep-alive", "2", \
     "--user", "mcp", \
     "--group", "mcp", \
     "--access-logfile", "/app/logs/access.log", \
     "--error-logfile", "/app/logs/error.log", \
     "--log-level", "info", \
     "--capture-output", \
     "mcp_docassemble.server:app"]

# Alternative lightweight startup for development
# CMD ["python", "-m", "mcp_docassemble.server"]
