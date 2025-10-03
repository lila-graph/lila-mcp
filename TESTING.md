# MCP Server Testing Guide

## Overview

This project provides two MCP server implementations for different testing and deployment scenarios:

1. **`simple_lila_mcp_server.py`** - Mock data server for rapid development and testing
2. **`lila_mcp_server.py`** - Full Neo4j-integrated server for production use

## Server Implementations

### Simple Mock Server (`simple_lila_mcp_server.py`)

**Purpose:** Rapid development and testing without database dependencies

**Data Source:** In-memory mock data defined in the `__init__` method:
- `self.mock_personas` - Hardcoded persona profiles (Lila, Don)
- `self.mock_relationships` - Predefined relationship metrics
- `self.mock_interactions` - Sample interaction history

**Use Cases:**
- Testing MCP Inspector functionality
- Developing new tools/resources without database setup
- Debugging MCP protocol issues
- Fast iteration during development

**Neo4j Connection:** Attempts connection but gracefully falls back to mock data if Neo4j unavailable

### Full Neo4j Server (`lila_mcp_server.py`)

**Purpose:** Production deployment with live Neo4j database

**Data Source:** Neo4j graph database queries:
- Queries `PersonaAgent` nodes for persona data
- Queries `RELATIONSHIP` edges for relationship metrics
- Stores interaction history in database
- Updates metrics in real-time

**Use Cases:**
- Production deployments
- Testing with real Neo4j data
- Integration testing
- Performance testing with large datasets

**Neo4j Connection:** Required - returns errors if database unavailable

## Testing with MCP Inspector

### Quick Start (Mock Data)

1. **Configure for mock data testing:**
```bash
# fastmcp.json is already configured for simple_lila_mcp_server.py
cat fastmcp.json
```

Expected configuration:
```json
{
  "source": {
    "type": "filesystem",
    "path": "simple_lila_mcp_server.py",
    "entrypoint": "mcp"
  },
  "environment": {
    "type": "uv",
    "python": "3.12",
    "project": "."
  }
}
```

2. **Start MCP Inspector:**
```bash
/home/donbr/lila-graph/lila-mcp/.venv/bin/fastmcp dev
```

3. **Access Inspector UI:**
- Open the URL displayed in terminal (includes auth token)
- Example: `http://localhost:6274/?MCP_PROXY_AUTH_TOKEN=<token>`

4. **Click "Connect"** - Server will use mock data from `simple_lila_mcp_server.py`

### Testing with Neo4j Data

1. **Ensure Neo4j is running:**
```bash
docker compose up -d neo4j
docker compose ps neo4j  # Verify it's healthy
```

2. **Load data into Neo4j (if needed):**
```bash
./init_mcp_database.sh
```

3. **Update `fastmcp.json` to use Neo4j server:**
```json
{
  "source": {
    "type": "filesystem",
    "path": "lila_mcp_server.py",
    "entrypoint": "mcp"
  },
  "environment": {
    "type": "uv",
    "python": "3.12",
    "project": "."
  }
}
```

4. **Restart MCP Inspector:**
```bash
# Kill existing server
pkill -f "fastmcp dev"

# Start with Neo4j-backed server
/home/donbr/lila-graph/lila-mcp/.venv/bin/fastmcp dev
```

5. **Access Inspector and test with real data**

## Configuration Fix for Inspector

### Problem: `[object Object]` Error

The MCP Inspector's argument parser has a bug when parsing `>=` operators in dependency version strings. When `fastmcp.json` contains:

```json
"dependencies": [
  "fastmcp>=2.12.3",
  "neo4j>=5.15.0"
]
```

The Inspector incorrectly splits `neo4j>=5.15.0` into `neo4j`, `[object Object]`, `=5.15.0`, causing `uv` to fail.

### Solution: Use Project Configuration

Instead of listing individual dependencies, point to the existing `pyproject.toml`:

```json
{
  "environment": {
    "type": "uv",
    "python": "3.12",
    "project": "."
  }
}
```

This uses the already-installed virtual environment and avoids the buggy argument parser.

## Testing Resources

### Available Resources (Both Servers)

- `neo4j://personas/all` - List all personas
- `neo4j://personas/{persona_id}` - Get specific persona
- `neo4j://relationships/all` - List all relationships
- `neo4j://relationships/{persona1_id}/{persona2_id}` - Get specific relationship
- `neo4j://interactions/recent/{count}` - Recent interactions
- Additional resources (varies by implementation)

### Available Tools (Both Servers)

- `update_relationship_metrics` - Update trust/intimacy/strength
- `record_interaction` - Log new interaction
- `analyze_persona_compatibility` - Compatibility analysis
- `autonomous_strategy_selection` - Select interaction strategy
- `assess_goal_progress` - Track relationship goals
- `generate_contextual_response` - Generate persona responses

### Available Prompts (Both Servers)

- `assess_attachment_style` - Determine attachment style
- `analyze_emotional_climate` - Evaluate emotional dynamics
- `generate_secure_response` - Create secure attachment responses

## Comparison Table

| Feature | `simple_lila_mcp_server.py` | `lila_mcp_server.py` |
|---------|----------------------------|---------------------|
| Data Source | In-memory mock data | Neo4j database |
| Neo4j Required | No (optional) | Yes |
| Debug Logging | Enabled | Standard logging |
| Startup Speed | Fast | Depends on Neo4j |
| Data Persistence | No (in-memory only) | Yes (database) |
| Use Case | Development/testing | Production/integration |
| Mock Personas | Lila, Don | Database-driven |

## Troubleshooting

### Inspector Connection Issues

**Problem:** `ERR_CONNECTION_REFUSED` on port 6277

**Solutions:**
1. Verify `fastmcp dev` is running: `ps aux | grep fastmcp`
2. Check correct port: should be 6274 for UI, 6277 for proxy
3. Use full URL with auth token from terminal output

**Problem:** `[object Object]` error when connecting

**Solution:** Ensure `fastmcp.json` uses `"project": "."` instead of listing dependencies

### Neo4j Connection Issues

**Problem:** "Neo4j database not available" errors

**Solutions:**
1. Start Neo4j: `docker compose up -d neo4j`
2. Check Neo4j health: `docker compose ps neo4j`
3. Verify `.env` has correct credentials
4. Test connection: `docker exec -it lila-mcp-neo4j-1 cypher-shell -u neo4j -p passw0rd`

### Port Conflicts

**Problem:** Port already in use

**Solutions:**
1. Kill existing processes: `pkill -f "fastmcp dev"`
2. Check what's using port: `lsof -i :6274` or `ss -tulpn | grep 6274`
3. Use custom port: `fastmcp dev --server-port 6350`

## Best Practices

1. **Use `simple_lila_mcp_server.py` for:**
   - Initial development of new tools/resources
   - Testing MCP protocol features
   - Debugging without database complexity

2. **Use `lila_mcp_server.py` for:**
   - Testing with actual graph data
   - Integration testing
   - Performance testing
   - Pre-production validation

3. **Always use `"project": "."` in `fastmcp.json`** to avoid Inspector parsing bugs

4. **Keep both servers synchronized** - When adding new tools/resources, update both implementations

5. **Use version control** - Before switching between servers, commit your `fastmcp.json` changes

## Command Reference

### FastMCP Development Server Commands

```bash
# Start MCP Inspector with auto-detected fastmcp.json (recommended)
fastmcp dev

# Start from virtual environment (if not in PATH)
/home/donbr/lila-graph/lila-mcp/.venv/bin/fastmcp dev

# Start with custom Inspector ports
fastmcp dev --ui-port 6274 --server-port 6277

# Start with specific Python version
fastmcp dev --python 3.12

# Start with additional packages
fastmcp dev --with pandas --with numpy

# Start in specific project directory
fastmcp dev --project /path/to/project
```

### Stopping FastMCP Server

**Problem:** `fastmcp dev` creates multiple background processes (node, npm, mcp-inspector) that must ALL be killed.

**Complete Kill Process:**

```bash
# Method 1: Kill by pattern (kills main process but may leave orphans)
pkill -f "fastmcp dev"

# Method 2: Kill ALL related processes (RECOMMENDED)
pkill -f "fastmcp dev" && pkill -f "mcp-inspector"

# Method 3: Manual kill by PID (if pkill doesn't work)
# First, find all related processes:
ps aux | grep -E "fastmcp|mcp-inspector|node.*6274|node.*6277" | grep -v grep

# Then kill by PID:
kill <PID1> <PID2> <PID3> ...

# Method 4: One-liner to kill all (nuclear option)
ps aux | grep -E "fastmcp|mcp-inspector|node.*627" | grep -v grep | awk '{print $2}' | xargs -r kill
```

**Verify ports are free before restarting:**
```bash
# Check if ports 6274 and 6277 are in use
ss -tulpn | grep -E "6274|6277"

# Or use lsof
lsof -i :6274
lsof -i :6277

# If ports still in use, find and kill the process
lsof -ti :6277 | xargs -r kill
lsof -ti :6274 | xargs -r kill
```

### Complete Kill and Restart Workflow

```bash
# 1. Kill all fastmcp and inspector processes
pkill -f "fastmcp dev"
pkill -f "mcp-inspector"

# 2. Wait for processes to terminate
sleep 2

# 3. Verify ports are free
ss -tulpn | grep -E "6274|6277"

# 4. If ports still occupied, force kill by port
lsof -ti :6277 | xargs -r kill
lsof -ti :6274 | xargs -r kill

# 5. Restart server
/home/donbr/lila-graph/lila-mcp/.venv/bin/fastmcp dev
```

### Checking Server Status

```bash
# Check if fastmcp dev is running
ps aux | grep "fastmcp dev" | grep -v grep

# Check all MCP-related processes
ps aux | grep -E "fastmcp|mcp-inspector" | grep -v grep

# Check what's using the Inspector ports
ss -tulpn | grep -E "6274|6277"

# Full process tree (shows parent-child relationships)
pstree -p | grep -A 5 fastmcp
```

### Neo4j Database Commands

```bash
# Start Neo4j
docker compose up -d neo4j

# Check Neo4j status
docker compose ps neo4j

# View Neo4j logs
docker compose logs neo4j

# Stop Neo4j
docker compose stop neo4j

# Initialize/seed database
./init_mcp_database.sh

# Test Neo4j connection
docker exec -it lila-mcp-neo4j-1 cypher-shell -u neo4j -p passw0rd
```

### FastMCP CLI Help

```bash
# Show all available commands
fastmcp --help

# Show dev command options
fastmcp dev --help

# Show version
fastmcp version
```
