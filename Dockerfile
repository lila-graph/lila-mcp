# Standalone Lila MCP Server
# Optimized for minimal dependencies and fast startup

FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy MCP-specific dependencies
COPY docker/mcp-standalone/requirements.txt ./

# Install minimal dependencies for MCP server
RUN pip install -r requirements.txt

# Create non-root user
RUN groupadd -r mcp && useradd -r -g mcp mcp

# Copy minimal standalone MCP server files
COPY --chown=mcp:mcp docker/mcp-standalone/main.py ./
COPY --chown=mcp:mcp docker/mcp-standalone/minimal_models.py ./
COPY --chown=mcp:mcp docker/mcp-standalone/minimal_neo4j.py ./
COPY --chown=mcp:mcp docker/mcp-standalone/minimal_mcp_server.py ./
COPY --chown=mcp:mcp docker/mcp-standalone/__init__.py ./

# Set environment variables
ENV PYTHONPATH=/app
ENV ENV=production
ENV LOG_LEVEL=INFO

# Switch to non-root user
USER mcp

# No health check in minimal implementation (removed to avoid AsyncIO conflicts)

# Expose MCP server port
EXPOSE 8765

# Start MCP server
CMD ["python", "main.py"]