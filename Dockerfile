# syntax=docker/dockerfile:1.7
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates \
 && rm -rf /var/lib/apt/lists/* \
 && curl -LsSf https://astral.sh/uv/install.sh | env UV_NO_MODIFY_PATH=1 UV_INSTALL_DIR=/usr/local/bin sh \
 && uv --version

# deps only
COPY pyproject.toml uv.lock* ./
RUN uv sync --frozen --no-dev --no-install-project

# then project files
COPY . .
RUN uv pip install -e .

# non-root runtime
RUN useradd -m -u 10001 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8766
ENV MCP_HOST=0.0.0.0 MCP_PORT=8766

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD curl -fsS http://127.0.0.1:8766/mcp/capabilities || exit 1

CMD ["uv", "run", "python", "lila_mcp_server.py"]
