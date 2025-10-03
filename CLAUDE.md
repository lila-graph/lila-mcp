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
# Auto-configuration using fastmcp.json
fastmcp dev

# With custom Inspector port
fastmcp dev --server-port 6350

# Fallback with explicit dependencies
fastmcp dev lila_mcp_server.py --with fastmcp --with neo4j --with pydantic --with python-dotenv
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

# Initialize database with seed data
./init_mcp_database.sh
```

### Database Operations

```bash
# Import seed data into Neo4j
python import_data.py --seed-data seed_data.cypher --schema graphs/lila-graph-schema-v8.json

# Export data from Neo4j
python export_data.py
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

- **`lila_mcp_server.py`** - Full-featured MCP server with complete Neo4j integration and all psychological intelligence features
- **`simple_lila_mcp_server.py`** - Simplified MCP server with debug logging enabled, recommended for development
- **`fastmcp.json`** - FastMCP configuration defining server entrypoint, dependencies, and deployment settings

### Data Management

- **`import_data.py`** - Neo4j data importer with retry logic for container startup
- **`export_data.py`** - Neo4j data exporter for backup and migration
- **`init_mcp_database.sh`** - Automated database initialization script

### Infrastructure

- **`docker-compose.yml`** - Defines Neo4j, Redis, and MinIO services with health checks
- **`Dockerfile`** - Container image for MCP server deployment
- **`nginx.conf`** - Nginx reverse proxy configuration

### Configuration

- **`.env`** - Environment variables for Neo4j connection, Logfire telemetry, service credentials
- **`.env.example`** - Template for environment configuration
- **`pyproject.toml`** - Python project dependencies and build configuration

### Graph Schemas

Located in `graphs/`:
- **`lila-graph-schema-v8.json`** - Current schema (default)
- **`lila-graph-schema-v9.json`** - Latest schema version
- **`lila-graph-schema-v7.json`** - Legacy schema

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

## Development Workflow

1. **Start Infrastructure**: `docker compose up -d neo4j`
2. **Initialize Database**: `./init_mcp_database.sh` (first time only)
3. **Develop with Inspector**: `fastmcp dev` (opens web UI for testing)
4. **Test Changes**: `python test_mcp_validation.py`
5. **Deploy**: `fastmcp run` (HTTP server on port 8765)

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

- Always use `simple_lila_mcp_server.py` for development (has debug logging)
- Use `lila_mcp_server.py` for production deployments
- MCP resources must return strings (typically JSON)
- Environment variables are loaded from `.env` via `python-dotenv`
- Neo4j connection failures are graceful (fallback to mock data)
- FastMCP automatically manages virtual environments when using `fastmcp.json`

## Troubleshooting

**"Error Connecting to MCP Inspector Proxy"**: Use `simple_lila_mcp_server.py` instead of `lila_mcp_server.py`

**Neo4j connection issues**: Verify Neo4j is running with `docker compose ps`, check `.env` credentials

**Port conflicts**: Use `--server-port 6350` with `fastmcp dev` to change Inspector port

**Import failures**: Ensure you're in the repository root and `.env` file exists
