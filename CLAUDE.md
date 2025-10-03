# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**lila-mcp** is a standalone MCP (Model Context Protocol) server that provides psychological relationship intelligence using Neo4j graph database. It exposes personas, psychological profiles, relationship metrics, and interaction histories through the MCP protocol.

The system implements:
- **8 MCP Tools** for psychological analysis and relationship modeling
- **3 MCP Prompts** for attachment theory assessments
- **9 MCP Resources** (2 direct + 7 templated) for querying psychological data
- **Neo4j graph database** for storing persona relationships and interactions
- **FastMCP framework** for MCP server implementation

### Key Technologies
- **Python 3.12** - Required version
- **FastMCP 2.12.3+** - MCP server framework
- **Neo4j 5.15.0+** - Graph database (with APOC plugin)
- **uv** - Package and virtual environment manager
- **Docker Compose** - Multi-service orchestration

## Development Commands

### Environment Setup
```bash
# Start Neo4j database
docker compose up -d neo4j

# Start all infrastructure services (Neo4j, Redis, MinIO)
docker compose up -d
```

### Running the MCP Server

**Development with Inspector (Recommended):**
```bash
# Auto-configuration using fastmcp.json (uses simple_lila_mcp_server.py by default)
fastmcp dev

# Or explicitly from venv (if fastmcp not in PATH)
/home/donbr/lila-graph/lila-mcp/.venv/bin/fastmcp dev

# With custom Inspector ports
fastmcp dev --ui-port 6274 --server-port 6277

# IMPORTANT: fastmcp.json uses "project": "." to avoid MCP Inspector argument parsing bugs
# Do NOT use explicit --with dependencies as >= operators break the Inspector's JavaScript parser
```

**Production HTTP Deployment:**
```bash
# Auto-configuration
fastmcp run

# Custom port
fastmcp run --port 9000

# Explicit configuration
fastmcp run lila_mcp_server.py --transport http --port 8765
```

### Testing

```bash
# Validate MCP server capabilities
fastmcp inspect

# Run validation tests
python test_mcp_validation.py

# Expected test output:
# ✅ Resources found: 6-9 (depending on simple vs full server)
# ✅ Tools found: 8
# ✅ Prompts found: 3
# Test validates MCP protocol compliance and endpoint registration

# Initialize database with seed data
./init_mcp_database.sh
```

### Database Operations

```bash
# Import seed data into Neo4j
python import_data.py --seed-data seed_data.cypher --schema graphs2/lila-graph-schema-v8.json

# Export data from Neo4j
python export_data.py

# Check Neo4j connection and data
docker compose exec neo4j cypher-shell -u neo4j -p $NEO4J_PASSWORD "MATCH (p:PersonaAgent) RETURN count(p)"
```

### MCP Client Configuration

```bash
# Generate Claude Desktop config
fastmcp install claude-desktop

# Generate Cursor config
fastmcp install cursor

# Generic MCP JSON config
fastmcp install mcp-json
```

## Architecture

### Core Server Files

- **`lila_mcp_server.py`** - Full-featured MCP server with complete Neo4j integration and all psychological intelligence features (production)
- **`simple_lila_mcp_server.py`** - Simplified MCP server with debug logging enabled and mock data fallback (development default)
- **`fastmcp.json`** - FastMCP configuration defining server entrypoint (`"path": "lila_mcp_server.py"` on line 6), dependencies via `"project": "."`, and deployment settings
- **`test_mcp_validation.py`** - Validates MCP protocol compliance, endpoint registration, and resource/tool/prompt counts

### Data Management

- **`import_data.py`** - Neo4j data importer with retry logic for container startup
- **`export_data.py`** - Neo4j data exporter for backup and migration
- **`init_mcp_database.sh`** - Automated database initialization script

### Infrastructure

- **`docker-compose.yml`** - Defines Neo4j, Redis, MinIO, mcp-server, and nginx proxy with service dependencies and health checks
- **`Dockerfile`** - Multi-stage container image using Python 3.12-slim with uv package manager
- **`nginx.conf`** - Nginx reverse proxy on port 8080 proxying to mcp-server:8766, includes `/health` endpoint

### Configuration

- **`.env`** - Environment variables for Neo4j connection, Logfire telemetry, service credentials
- **`.env.example`** - Template for environment configuration
- **`pyproject.toml`** - Python project dependencies and build configuration

### Graph Schemas

- **`graphs2/lila-graph-schema-v8.json`** - Neo4j graph schema defining PersonaAgent nodes, relationship types, and constraints
- **Note**: Use `graphs2/` directory for schema files (see Directory Permissions Issue below)

### Directory Permissions Issue

**Problem**: The `graphs/` directory has restrictive permissions and is inaccessible to the host user.

**Root Cause**:
- The `graphs/` directory is owned by UID:GID 7474:7474 (Neo4j container user)
- Permissions are 700 (drwx------), making it readable only by the Neo4j container
- This occurred when Docker Compose mounted Neo4j volumes and the container changed ownership

**Workaround**:
- Use the `graphs2/` directory instead (owned by host user, permissions 755)
- `graphs2/` contains a copy of the schema file and is fully accessible
- Created on Oct 3, 2025 as part of the "initial fastmcp cleanup"

**To Fix Permanently** (if you need to restore `graphs/` access):

```bash
# Stop Neo4j container first
docker compose stop neo4j

# Change ownership back to host user
sudo chown -R $(id -u):$(id -g) /home/donbr/lila-graph/lila-mcp/graphs/

# Fix permissions
sudo chmod 755 /home/donbr/lila-graph/lila-mcp/graphs/

# Restart Neo4j
docker compose up -d neo4j
```

**Why This Happens**:
- Docker containers run with specific UIDs (Neo4j uses 7474)
- When containers write to bind mounts, they use their internal UID
- Host system may not have that UID mapped to a user
- Results in "UNKNOWN" user ownership on host

## Key Architectural Concepts

### MCP Server Pattern

The server uses FastMCP decorators to expose functionality:
```python
@self.app.resource("neo4j://personas/all")
def get_all_personas() -> str:
    # Returns JSON string of all personas

@self.app.tool()
def analyze_persona_compatibility(persona_a_id: str, persona_b_id: str) -> str:
    # Tool implementation

@self.app.prompt()
def assess_attachment_style(behavior_description: str) -> str:
    # Prompt implementation
```

### MCP Endpoints Overview

**Resources** (read-only data access):
- `neo4j://personas/all` - All personas with psychological profiles
- `neo4j://personas/{persona_id}` - Specific persona by ID
- `neo4j://relationships/all` - All relationships with metrics
- `neo4j://relationships/{persona1_id}/{persona2_id}` - Specific relationship
- `neo4j://interactions/recent/{count}` - Recent interaction history

**Tools** (actions and analysis):
- `update_relationship_metrics` - Modify trust/intimacy/strength
- `record_interaction` - Log interactions with emotional analysis
- `analyze_persona_compatibility` - Assess relationship potential using attachment theory
- `autonomous_strategy_selection` - AI-driven strategy selection based on attachment style
- `assess_goal_progress` - Evaluate progress towards relationship goals
- `generate_contextual_response` - Create psychologically authentic responses
- Plus 2 additional tools for demo sessions and relationship state management

**Prompts** (LLM-ready assessment frameworks):
- `assess_attachment_style` - Determine attachment style from behavioral observations
- `analyze_emotional_climate` - Evaluate conversation dynamics and safety
- `generate_secure_response` - Create attachment-security-building responses

### Database Connection Strategy

- **Primary**: Neo4j connection via environment variables (`NEO4J_URI`, `NEO4J_USER`, `NEO4J_PASSWORD`)
- **Fallback**: In-memory database with sample data if Neo4j unavailable
- **Retry Logic**: `import_data.py` implements connection retry (30 attempts, 2s intervals) for container startup

### Transport Modes

- **STDIO** (`fastmcp dev`) - For development with Inspector web UI
- **HTTP** (`fastmcp run`) - For production deployment and client integration
- FastMCP automatically handles transport selection based on command

### Environment Variables

Required in `.env`:
```
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=passw0rd
ENABLE_LOGFIRE_TELEMETRY=true
LOGFIRE_PROJECT_NAME=lila-autonomous-agents
```

## Docker Infrastructure

The system uses a multi-service Docker Compose architecture:

### Service Dependencies
```
neo4j, redis, minio (infrastructure)
  ↓ (depends_on with condition: service_healthy)
mcp-server (FastMCP server on port 8766)
  ↓ (depends_on)
proxy (nginx on port 8080)
```

### Service Ports
- **Neo4j**: 7474 (Browser), 7687 (Bolt)
- **Redis**: 6379
- **MinIO**: 9000 (API), 9001 (Console)
- **MCP Server**: 8766 (Streamable-HTTP transport)
- **Nginx Proxy**: 8080 (External access point)

### Key Configuration Details
- **MCP Server Command**: `uvx fastmcp run /app/fastmcp.json` (uses uv to run FastMCP in container)
- **Neo4j Auth**: Uses `NEO4J_AUTH: "neo4j/${NEO4J_PASSWORD}"` format
- **Neo4j Plugins**: APOC plugin enabled via `NEO4J_PLUGINS: '["apoc"]'`
- **Network**: All services communicate via `lila-network` Docker network
- **Volumes**: Persistent data for Neo4j (data, logs, import, plugins), Redis, and MinIO

### Health Check Strategy
- **Neo4j**: Uses cypher-shell to verify bolt connection accepts authentication
- **Redis**: Simple `redis-cli ping`
- **MinIO**: HTTP health endpoint check
- **MCP Server**: Dockerfile-based healthcheck (not in docker-compose.yml) to avoid Streamable-HTTP protocol conflicts
- **Nginx Proxy**: No healthcheck (depends on mcp-server service)

## Development Workflow

1. **Start Infrastructure**: `docker compose up -d` (starts all services with proper dependencies)
2. **Initialize Database**: `./init_mcp_database.sh` (first time only)
3. **Develop with Inspector**: `fastmcp dev` (opens web UI for testing)
4. **Test Changes**: `python test_mcp_validation.py`
5. **Deploy**: Production deployment runs via Docker Compose (mcp-server container)

## Testing Strategy

**Direct Connection Testing** (preferred):
- Uses `Client(mcp_server)` for in-memory testing
- No network dependencies
- Fast iteration

**Inspector Testing** (interactive):
- Uses `fastmcp dev` to launch web UI
- Access at `http://localhost:6274/?MCP_PROXY_AUTH_TOKEN=<token>`
- Visual testing of resources, tools, prompts

**HTTP Client Testing** (production):
```python
from fastmcp import Client
async with Client('http://localhost:8765/mcp/') as client:
    personas = await client.read_resource('neo4j://personas/all')
```

## Common Development Patterns

### Adding a New MCP Resource

```python
@self.app.resource("neo4j://custom/resource")
def get_custom_resource() -> str:
    """Resource description."""
    if not self.driver:
        return '{"error": "Neo4j database not available"}'

    with self.driver.session() as session:
        result = session.run("MATCH (n) RETURN n")
        # Process and return JSON string
```

### Adding a New MCP Tool

```python
@self.app.tool()
def custom_tool(param1: str, param2: int) -> str:
    """Tool description with parameter details."""
    # Implementation
    return json.dumps({"result": "value"})
```

### Database Query Pattern

```python
with self.driver.session() as session:
    result = session.run("""
        MATCH (p:PersonaAgent)-[r:KNOWS]->(other)
        WHERE p.persona_id = $persona_id
        RETURN other
    """, persona_id=persona_id)

    records = [record.data() for record in result]
```

## Important Notes

### Server Selection
- **`simple_lila_mcp_server.py`** - Use for development (has debug logging, mock data fallback)
  - Default personas: "lila" and "don" with predefined psychological profiles
  - Works without Neo4j running
  - Enables FastMCP debug logging
- **`lila_mcp_server.py`** - Use for production (requires Neo4j, full database integration)
  - Connects to live Neo4j database
  - No mock data fallback
  - Includes health check endpoint
- Default configuration in `fastmcp.json` uses `lila_mcp_server.py` (line 6)

### FastMCP Configuration
- **CRITICAL**: `fastmcp.json` must use `"project": "."` in environment config
- **DO NOT** use explicit `dependencies` array with `>=` operators - breaks MCP Inspector
- FastMCP automatically manages virtual environments via `uv`
- The `"project": "."` configuration uses `pyproject.toml` for dependencies

### MCP Protocol
- MCP resources must return strings (typically JSON)
- Tools receive JSON-serializable parameters and return JSON strings
- Prompts return formatted text suitable for LLM consumption

### Infrastructure
- Environment variables loaded from `.env` via `python-dotenv`
- Neo4j connection failures are graceful (fallback to mock data in `simple_lila_mcp_server.py`)
- The mcp-server container runs on port 8766 with Streamable-HTTP transport
- Nginx proxy exposes the service on port 8080 with proper SSE/streaming support
- **Health checks**: The mcp-server healthcheck is defined in the Dockerfile (not docker-compose.yml) to avoid protocol compatibility issues with FastMCP's Streamable-HTTP transport

### Testing and Documentation Reference
- **Test Validation**: `test_mcp_validation.py` validates MCP protocol compliance
  - Tests direct connection (in-memory, no network)
  - Tests Inspector connection (requires `fastmcp dev` running)
  - Expected counts: 6-9 resources, 8 tools, 3 prompts
- **Component Documentation**: `repo_analysis/docs/01_component_inventory.md` contains detailed API reference for all MCP resources, tools, and prompts
- **Data Flow Documentation**: `repo_analysis/docs/03_data_flows.md` contains sequence diagrams showing request routing and database query patterns
- **Two Server Implementations**: `simple_lila_mcp_server.py` (mock data) vs `lila_mcp_server.py` (Neo4j data)

## Troubleshooting

### MCP Inspector Connection Issues

**Problem:** `ERR_CONNECTION_REFUSED` when clicking "Connect" in Inspector, or `error: Failed to spawn: '[object Object]'`

**Root Cause:** MCP Inspector's JavaScript argument parser incorrectly splits `>=` operators in dependency version strings (e.g., `fastmcp>=2.12.3` becomes `fastmcp`, `[object Object]`, `=2.12.3`)

**Solution:** Use `"project": "."` in `fastmcp.json` environment configuration instead of listing individual dependencies. This is already configured correctly in the repository.

**Verify Configuration:**
```json
{
  "environment": {
    "type": "uv",
    "python": "3.12",
    "project": "."  // ✓ Correct - uses pyproject.toml
  }
}
```

**Wrong Configuration (DO NOT USE):**
```json
{
  "environment": {
    "dependencies": [
      "fastmcp>=2.12.3",  // ✗ Breaks Inspector
      "neo4j>=5.15.0"     // ✗ Breaks Inspector
    ]
  }
}
```

### Killing and Restarting FastMCP Dev

**Problem:** `PORT IS IN USE at port 6277` when restarting

**Root Cause:** `fastmcp dev` spawns multiple background processes (Python, node, npm, mcp-inspector) that must ALL be killed

**Solution:**
```bash
# Kill all related processes
pkill -f "fastmcp dev" && pkill -f "mcp-inspector"

# Wait for processes to terminate
sleep 2

# Verify ports are free
ss -tulpn | grep -E "6274|6277"

# If ports still occupied, force kill by port
lsof -ti :6277 | xargs -r kill
lsof -ti :6274 | xargs -r kill

# Restart
/home/donbr/lila-graph/lila-mcp/.venv/bin/fastmcp dev
```

**Check Running Processes:**
```bash
# See all MCP-related processes
ps aux | grep -E "fastmcp|mcp-inspector" | grep -v grep

# Check port usage
ss -tulpn | grep -E "6274|6277"
```

### Directory Permission Issues

**Problem:** "Permission denied" when accessing `graphs/` directory or reading schema files

**Symptoms:**

```bash
ls: cannot open directory 'graphs/': Permission denied
# or
Permission denied: 'graphs/lila-graph-schema-v8.json'
```

**Root Cause:** The `graphs/` directory is owned by the Neo4j Docker container user (UID 7474) with restrictive 700 permissions.

**Solutions:**

1. **Use the workaround** (Recommended):

   ```bash
   # Use graphs2/ directory instead
   python import_data.py --schema graphs2/lila-graph-schema-v8.json
   ```

2. **Fix permissions permanently**:

   ```bash
   # Stop Neo4j first
   docker compose stop neo4j

   # Fix ownership and permissions
   sudo chown -R $(id -u):$(id -g) graphs/
   sudo chmod 755 graphs/

   # Restart Neo4j
   docker compose up -d neo4j
   ```

3. **Prevent the issue** (for new deployments):

   ```bash
   # Before first docker compose up, ensure correct ownership
   chown -R $(id -u):$(id -g) graphs/
   chmod 755 graphs/
   ```

**Understanding Docker UID Mapping:**

- Docker containers run with specific UIDs (Neo4j = 7474)
- When containers modify bind-mounted directories, they use their internal UID
- Host may not have that UID, resulting in "UNKNOWN" ownership
- Use named volumes instead of bind mounts to avoid this, or manage permissions carefully

### Other Issues

**"Error Connecting to MCP Inspector Proxy"**: Use `simple_lila_mcp_server.py` instead of `lila_mcp_server.py` (this is the default in `fastmcp.json`)

**Neo4j connection issues**: Verify Neo4j is running with `docker compose ps neo4j`, check `.env` credentials

**Port conflicts**: Use `--ui-port` and `--server-port` flags to change Inspector ports

**Import failures**: Ensure you're in the repository root and `.env` file exists

**MCP server healthcheck failures (406 Not Acceptable)**: This occurs when docker-compose healthchecks try to make simple HTTP requests to FastMCP's Streamable-HTTP transport, which requires specific MCP protocol headers. The healthcheck should be defined in the Dockerfile or removed from docker-compose.yml entirely. Do not use `curl -X POST http://localhost:8766/mcp` for healthchecks - it will return 406.

## Quick Reference: Common Tasks

### Switching Between Server Implementations

```bash
# Edit fastmcp.json line 6 to change server
# For development (mock data):
"path": "simple_lila_mcp_server.py"

# For production (Neo4j required):
"path": "lila_mcp_server.py"

# Restart the server after changing
pkill -f "fastmcp dev" && fastmcp dev
```

### Debugging Connection Issues

```bash
# 1. Check Neo4j is running
docker compose ps neo4j

# 2. Test Neo4j connection
python -c "from neo4j import GraphDatabase; driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'passw0rd')); driver.verify_connectivity(); print('✅ Connected')"

# 3. Verify environment variables
cat .env | grep NEO4J

# 4. Run validation tests
python test_mcp_validation.py
```

### Fixing Directory Permissions

```bash
# Check current permissions
ls -la | grep graphs

# Fix graphs/ directory ownership (if needed)
sudo chown -R $(id -u):$(id -g) graphs/
sudo chmod 755 graphs/

# Or use the graphs2/ workaround
python import_data.py --schema graphs2/lila-graph-schema-v8.json
```

### Working with Docker Services

```bash
# Start only Neo4j
docker compose up -d neo4j

# View logs for specific service
docker compose logs -f mcp-server

# Restart a service
docker compose restart mcp-server

# Clean up and start fresh
docker compose down -v && docker compose up -d
```

### Accessing Services

- **Neo4j Browser**: <http://localhost:7474> (user: neo4j, password from .env)
- **MCP Inspector**: <http://localhost:6274/?MCP_PROXY_AUTH_TOKEN=TOKEN> (run `fastmcp dev` first)
- **Nginx Proxy**: <http://localhost:8080> (production MCP endpoint)
- **MCP Server Direct**: <http://localhost:8766> (Streamable-HTTP, requires MCP client)
