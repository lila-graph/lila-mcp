# Comprehensive Lila MCP Server

A standalone, comprehensive implementation of the Lila psychological intelligence system as an MCP (Model Context Protocol) server.

## Overview

This is a **truly standalone** implementation that provides complete psychological intelligence capabilities without requiring the main Lila system. It includes:

- **Complete MCP Interface**: 8 tools, 3 prompts, 9 resources (2 direct + 7 templated)
- **Comprehensive Psychology**: Full PersonaAgent system, attachment theory, Big Five traits
- **Neo4j Integration**: Complete graph database operations with automatic connection
- **Autonomous Workflows**: PydanticAI-based decision making and strategy selection
- **Logfire Telemetry**: Native observability and monitoring
- **Self-Contained**: No dependencies on main Lila codebase

## Features

### Resources (9 total: 2 direct + 7 templated)
**Direct Resources:**
- `neo4j://personas/all` - All personas with complete psychological profiles
- `config://workflow-strategies` - Available autonomous workflow strategies

**Templated Resources:**
- `neo4j://personas/{persona_id}/relationships` - All relationships for a specific persona
- `neo4j://interactions/recent/{count}` - Recent interactions with psychological analysis
- `neo4j://relationships/{persona1_id}/{persona2_id}/current` - Current relationship state
- `neo4j://relationships/{persona1_id}/{persona2_id}/history` - Complete interaction history
- `telemetry://workflow-traces/{timerange}` - Telemetry traces from autonomous workflows
- `telemetry://conversation-quality/{persona_id}` - Conversation quality metrics
- `config://goal-templates/{scenario}` - Goal templates for relationship scenarios

### Tools (8 comprehensive psychological intelligence tools)
- `update_relationship_metrics` - Update trust, intimacy, and strength between personas
- `record_interaction` - Record interactions with psychological analysis
- `commit_relationship_state` - Explicitly persist relationship state (CQRS Command)
- `finalize_demo_session` - Finalize all relationship states at session end
- `analyze_persona_compatibility` - Assess relationship potential using attachment theory
- `autonomous_strategy_selection` - Select optimal strategy based on psychological modeling
- `assess_goal_progress` - Assess progress towards relationship goals
- `generate_contextual_response` - Generate psychologically authentic responses

### Prompts (3 comprehensive assessment prompts)
- `assess_attachment_style` - Determine persona's attachment style from behavioral observations
- `analyze_emotional_climate` - Evaluate conversation emotional dynamics and safety levels
- `generate_secure_response` - Create attachment-security-building responses for scenarios

## Quick Start

**Development Flow**: Test → Develop → Deploy

The recommended approach is to start with immediate visual testing (`fastmcp dev`), then move to production deployment (`fastmcp run`) once everything works.

### Step 1: Start the Server

The Lila MCP Server is fully self-contained with auto-configuration:

```bash
# Start the server with Inspector (auto-detects fastmcp.json)
fastmcp dev

# Or explicitly from virtual environment
/home/donbr/lila-graph/lila-mcp/.venv/bin/fastmcp dev

# ✅ No external dependencies required
# ✅ Auto-configured from fastmcp.json
# ✅ Complete psychological intelligence system
# ✅ All 8 tools, 3 prompts, 9 resources working
```

**Important Configuration Note**: The `fastmcp.json` file uses `"project": "."` configuration to avoid MCP Inspector bugs with version specifiers. See [Troubleshooting](#troubleshooting) section for details.

### Step 2: Test with MCP Inspector

**The server provides:**

```bash
# Inspector provides:
# ✅ Immediate web UI for testing (opens with auth token)
# ✅ Visual testing of all 8 tools, 3 prompts, resources
# ✅ Real-time protocol debugging
# ✅ STDIO transport (works immediately)
```

**What you'll see:**
- Inspector URL with token: `http://localhost:6274/?MCP_PROXY_AUTH_TOKEN=<token>`
- Click the URL to open the web interface
- Test resources like `neo4j://personas/all`
- Test tools like `analyze_persona_compatibility`
- Verify all functionality works before deployment

**Expected Components:**
- **Simplified Server**: 6 resources, 8 tools, 3 prompts (mock data)
- **Full Server**: 9 resources, 8 tools, 3 prompts (live Neo4j data)

### Step 2: Quick Capabilities Check

```bash
# Verify server capabilities without full Inspector
fastmcp inspect                 # Uses fastmcp.json auto-configuration

# Should show:
# Server: lila-psychological-relationships
# Components: Tools: 8, Prompts: 3, Resources: 2, Templates: 7
# Environment: FastMCP: 2.12.3, MCP: 1.14.0
# ✅ Successfully connected to Neo4j GraphDB
```

### Step 3: Production HTTP Deployment

Once testing confirms everything works, deploy with HTTP transport for production:

```bash
# HTTP transport for production deployment
fastmcp run                     # Uses fastmcp.json (port 8765)
fastmcp run --port 9000         # Override port if needed

# This provides:
# 🚀 Production-ready HTTP transport
# 🌐 Network accessible (can migrate to external server)
# 📡 Compatible with MCP clients (Claude Desktop, Cursor, etc.)
# 🔄 Scalable for multiple concurrent connections
```

**Important**: HTTP endpoint serves MCP JSON-RPC protocol, not REST API. See [MCP Client Testing](#mcp-client-testing) section for proper testing methods.

### Alternative: Docker Deployment

```bash
# Full stack deployment (Neo4j + Redis + MinIO + MCP server + Nginx)
docker compose up -d

# Or minimal deployment (MCP server only, requires Neo4j separately)
docker compose up -d neo4j mcp-server
```

### Server Selection: Mock vs Neo4j Data

The project includes two server implementations:

**`simple_lila_mcp_server.py`** (Default in fastmcp.json)
- In-memory mock data (Lila and Don personas)
- No Neo4j required
- Fast startup, ideal for development
- Graceful fallback if Neo4j unavailable

**`lila_mcp_server.py`** (Production)
- Full Neo4j database integration
- Real graph data queries
- Requires Neo4j running

To switch servers, edit `fastmcp.json` line 6:
```json
"path": "simple_lila_mcp_server.py"  // or "lila_mcp_server.py"
```

### Configuration

**Environment Configuration** (`.env` file):
All settings are configured in `.env` - no manual environment variables needed:
- `NEO4J_URI=bolt://localhost:7687`
- `NEO4J_USER=neo4j`
- `NEO4J_PASSWORD=passw0rd`
- `ENABLE_LOGFIRE_TELEMETRY=true`
- `LOGFIRE_PROJECT_NAME=lila-autonomous-agents`

**Critical Requirements**:
- **Neo4j Running** (if using `lila_mcp_server.py`): `docker compose up -d neo4j`
- **Configuration**: Uses `fastmcp.json` with `"project": "."` (avoids Inspector bugs)
- **Transport**: Inspector uses STDIO transport automatically (not HTTP)

**Recommended uv-Native Workflow** (avoids VIRTUAL_ENV conflicts):
```bash
# BEST: Use fastmcp.json auto-configuration
fastmcp dev                     # Auto-detects everything from fastmcp.json
fastmcp run                     # HTTP transport with auto-configuration
fastmcp inspect                 # View capabilities with auto-configuration

# FALLBACK: Explicit dependencies (if auto-detection fails)
fastmcp dev simple_lila_mcp_server.py --with fastmcp --with neo4j --with pydantic --with python-dotenv
```

**Inspector URL**: `http://localhost:6274/?MCP_PROXY_AUTH_TOKEN=<token>`
- Token is displayed in console output when server starts
- Use "Connect" button in Inspector interface
- Transport dropdown should show "STDIO" selected

### Quick Inspection

Verify the MCP server capabilities before starting development:

```bash
# Quick capabilities check using fastmcp.json - SIMPLEST!
fastmcp inspect

# Should show:
# Server: lila-psychological-relationships
# Components: Tools: 8, Prompts: 3, Resources: 2, Templates: 7
# Environment: FastMCP: 2.12.3, MCP: 1.14.0
# ✅ Successfully connected to Neo4j GraphDB

# For detailed JSON output:
fastmcp inspect --format fastmcp     # FastMCP-specific format
fastmcp inspect --format mcp         # Standard MCP protocol format
```

## Understanding MCP Transports

**Why does the Quick Start prioritize `fastmcp dev` (Inspector) over `fastmcp run` (HTTP)?**

The Model Context Protocol (MCP) supports multiple transport mechanisms, each optimized for different use cases:

### STDIO Transport (`fastmcp dev`)

**Use for**: Development, testing, immediate feedback

```bash
fastmcp dev                    # Creates Inspector web UI
```

**Benefits:**
- ✅ **Immediate visual testing** - Opens web UI with auth token automatically
- ✅ **Interactive debugging** - Click to test resources, tools, prompts in real-time
- ✅ **Protocol inspection** - View JSON-RPC messages in developer tools
- ✅ **Works immediately** - No client library configuration required
- ✅ **Zero setup** - Just one command to start testing

**How it works:**
- FastMCP creates a proxy server that bridges STDIO ↔ HTTP for the web Inspector
- Inspector connects via STDIO (standard input/output) to the MCP server
- Developer gets web UI for interactive testing without HTTP complexity

### HTTP Transport (`fastmcp run`)

**Use for**: Production deployment, client integration

```bash
fastmcp run                    # Serves MCP over HTTP JSON-RPC
```

**Benefits:**
- ✅ **Production ready** - Network accessible, scalable, SSL-capable
- ✅ **Client compatible** - Works with Claude Desktop, Cursor, custom clients
- ✅ **Multiple connections** - Supports concurrent client connections
- ✅ **Deployable** - Can be containerized, load-balanced, monitored

**How it works:**
- Serves MCP protocol as JSON-RPC over HTTP
- Clients send POST requests with MCP protocol messages
- **Not a REST API** - requires MCP-aware clients, not simple curl/browser access

### Development vs Production Flow

**Recommended workflow:**

1. **Development**: `fastmcp dev` → Visual testing in Inspector
2. **Validation**: `fastmcp inspect` → Verify capabilities
3. **Production**: `fastmcp run` → Deploy with HTTP for clients

**Why this order works:**
- Inspector provides immediate feedback on whether server works
- Once verified with Inspector, HTTP deployment "just works"
- Avoids confusion from HTTP testing complexity during development

### Transport Comparison

| Aspect | STDIO (`fastmcp dev`) | HTTP (`fastmcp run`) |
|--------|----------------------|---------------------|
| **Primary use** | Development testing | Production deployment |
| **Testing method** | Inspector web UI | MCP client libraries |
| **Setup complexity** | One command | Requires client configuration |
| **Debugging** | Interactive web UI | Client library + logs |
| **Accessibility** | Local only | Network accessible |
| **Concurrency** | Single session | Multiple clients |
| **Browser testing** | ✅ Yes (Inspector UI) | ❌ No (needs MCP client) |

## MCP Client Integration

### JSON Configuration Generation (FastMCP V2)

Generate MCP client configuration files for different applications:

```bash
# Auto-configuration using fastmcp.json (Recommended)
fastmcp install claude-desktop       # Uses fastmcp.json dependencies
fastmcp install cursor               # Uses fastmcp.json dependencies
fastmcp install mcp-json             # Generic MCP JSON configuration

# Explicit dependencies (fallback if auto-detection fails)
fastmcp install claude-desktop simple_lila_mcp_server.py --with neo4j --with pydantic --with python-dotenv
fastmcp install cursor simple_lila_mcp_server.py --with neo4j --with pydantic --with python-dotenv
fastmcp install mcp-json simple_lila_mcp_server.py --with neo4j --with pydantic --with python-dotenv
```

### Manual Client Configuration

#### HTTP Transport Configuration (Recommended)

For HTTP-based MCP clients (production ready):

```json
{
  "mcpServers": {
    "lila-psychology": {
      "url": "http://localhost:8765/mcp/",
      "transport": "http"
    }
  }
}
```

**Benefits of HTTP Transport:**
- ✅ **Network accessible** - can deploy to external servers
- ✅ **MCP client compatible** - works with Claude Desktop, Cursor, MCP libraries
- ✅ **Production ready** - supports load balancing, SSL termination
- ✅ **Scalable** - works with container orchestration

## MCP Client Testing

**Important**: MCP HTTP serves JSON-RPC protocol, not REST API. Use MCP-aware clients for testing:

```bash
# ✅ CORRECT: Test with FastMCP client library
python -c "
from fastmcp import Client
import asyncio

async def test():
    client = Client('http://localhost:8765/mcp/')
    async with client:
        # Test resource access
        personas = await client.get_resource('neo4j://personas/all')
        print('✅ Resources work:', len(personas) if personas else 'No data')

        # Test tool execution
        result = await client.call_tool('analyze_persona_compatibility', {
            'persona_a_id': 'lila',
            'persona_b_id': 'alex'
        })
        print('✅ Tools work:', bool(result))

asyncio.run(test())
"

# ❌ INCORRECT: Don't use simple HTTP tools
# curl http://localhost:8765/mcp/  # Returns 406 Not Acceptable
# Browser access also won't work - MCP needs proper JSON-RPC requests
```

#### Claude Desktop Configuration (STDIO - Development Only)

For local development with STDIO transport:

```json
{
  "mcpServers": {
    "lila-psychology": {
      "command": "fastmcp",
      "args": ["run", "/path/to/docker/mcp-standalone/simple_lila_mcp_server.py", "--transport", "stdio"],
      "env": {
        "NEO4J_URI": "bolt://localhost:7687",
        "NEO4J_USER": "neo4j",
        "NEO4J_PASSWORD": "passw0rd",
        "ENABLE_LOGFIRE_TELEMETRY": "true"
      }
    }
  }
}
```

#### Cursor Configuration (STDIO - Development Only)

For local development with STDIO transport:

```json
{
  "mcpServers": {
    "lila-psychology": {
      "command": "fastmcp",
      "args": ["run", "/path/to/docker/mcp-standalone/simple_lila_mcp_server.py", "--transport", "stdio"],
      "env": {
        "NEO4J_URI": "bolt://localhost:7687",
        "NEO4J_USER": "neo4j",
        "NEO4J_PASSWORD": "passw0rd"
      }
    }
  }
}
```

### Inspector Testing Workflow

1. **Start Inspector (Recommended - Auto-Configuration)**:
   ```bash
   # BEST: Uses fastmcp.json auto-configuration
   fastmcp dev                     # Automatically detects all dependencies and configuration

   # Custom Inspector port if needed:
   fastmcp dev --server-port 6350  # Avoids port conflicts

   # FALLBACK: Explicit dependencies (if auto-detection fails)
   fastmcp dev simple_lila_mcp_server.py --with fastmcp --with neo4j --with pydantic --with python-dotenv
   ```

2. **Access Web Interface**:
   - Copy URL with token from console output
   - Open in browser: `http://localhost:6274/?MCP_PROXY_AUTH_TOKEN=<your-token>`

3. **Test Resources**:
   - Click **Resources** tab
   - Test `neo4j://personas/all` - should return sample personas (Lila, Alex)
   - Test `neo4j://personas/lila` - should return detailed Lila profile
   - Test `neo4j://interactions/recent/5` - should return interaction history

4. **Test Tools**:
   - Click **Tools** tab
   - Test `analyze_persona_compatibility`:
     ```json
     {
       "persona_a_id": "lila",
       "persona_b_id": "alex"
     }
     ```
   - Test `query_relationship_metrics` with same parameters
   - Test `get_attachment_style_insights`:
     ```json
     {
       "persona_id": "lila"
     }
     ```

5. **Test Prompts**:
   - Click **Prompts** tab
   - Test `assess_attachment_style`:
     ```json
     {
       "behavior_description": "Shows consistent emotional availability and comfort with both intimacy and independence"
     }
     ```
   - Test `analyze_emotional_climate` with interaction history
   - Test `suggest_relationship_interventions` with relationship challenges

6. **Monitor Protocol**:
   - View real-time MCP JSON requests/responses
   - Check for any errors in console logs
   - Verify all capabilities are properly exposed

**FastMCP V2 Configuration Methods**:

```bash
# Option 1: Using fastmcp.json (Recommended - auto-detects everything)
fastmcp dev  # Automatically uses fastmcp.json in current directory

# Option 2: Explicit dependency management (fallback)
fastmcp dev simple_lila_mcp_server.py --with fastmcp --with neo4j --with pydantic --with python-dotenv

# Option 3: Project-based configuration
fastmcp project prepare fastmcp.json --output-dir ./env
fastmcp dev --project ./env

# Option 4: Requirements file (alternative)
fastmcp dev simple_lila_mcp_server.py --with-requirements requirements.txt
```

The Inspector provides:
- **Protocol Debugging**: Real-time MCP message inspection
- **Resource Testing**: Interactive resource querying with live data
- **Tool Execution**: Test psychological analysis tools with sample data
- **Prompt Testing**: Validate psychological assessment prompts
- **Schema Validation**: Verify tool/prompt schemas are correct

### Local Development (Alternative)

```bash
cd docker/mcp-standalone

# Install dependencies manually
pip install -r requirements.txt

# Run the server directly
python main.py
```

## Configuration

Environment variables:

```bash
# Database (optional - uses fallback if unavailable)
NEO4J_URI=bolt://neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=mcp_standalone_password_2025

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# MCP Server
MCP_HOST=0.0.0.0
MCP_PORT=8765
```

## Testing

### Unit Tests

```bash
# Test the implementation
python test_minimal.py

# Should output:
# 🎉 All tests passed! Minimal MCP server is ready.
```

### Interactive Testing with MCP Inspector

The **MCP Inspector** provides the best testing experience:

```bash
# Make sure you're in the docker/mcp-standalone/ directory
cd docker/mcp-standalone

# Start development server with Inspector
fastmcp dev main.py --with neo4j --with pydantic --with python-dotenv

# Or test HTTP server manually
fastmcp run main.py --transport http --port 8765
# Then open Inspector: https://github.com/modelcontextprotocol/inspector
```

**Inspector Testing Workflow**:

1. **Connect**: Select "STDIO" transport in Inspector (for `fastmcp dev`)
2. **Resources**: Test `neo4j://personas/all` - should return sample personas
3. **Tools**: Try `analyze_persona_compatibility` with `{"persona_a_id": "lila", "persona_b_id": "alex"}`
4. **Prompts**: Test `assess_attachment_style` with behavior descriptions
5. **Debug**: View JSON protocol messages, validate schemas

### HTTP Endpoint Testing

**Note**: This section is for validating HTTP deployment. For development, use Inspector (`fastmcp dev`) instead.

```bash
# ✅ CORRECT: Test with MCP client library
python -c "
from fastmcp import Client
import asyncio

async def test():
    print('Testing MCP HTTP endpoint...')
    client = Client('http://localhost:8765/mcp/')
    async with client:
        # Test server capabilities
        print('✅ Server connected')

        # Test resource access
        personas = await client.get_resource('neo4j://personas/all')
        print(f'✅ Resources: {len(personas) if personas else 0} personas loaded')

        # Test tool execution
        result = await client.call_tool('analyze_persona_compatibility', {
            'persona_a_id': 'lila',
            'persona_b_id': 'alex'
        })
        print(f'✅ Tools: compatibility analysis {"succeeded" if result else "failed"}')

asyncio.run(test())
"

# ❌ INCORRECT: Simple HTTP tools don't work with MCP
# curl http://localhost:8765/mcp/  # Returns 406 Not Acceptable
# Browser access also won't work - MCP requires JSON-RPC protocol
```

## Architecture

### Minimal Components

- **`minimal_models.py`** - Simple data models (Persona, Relationship, Interaction)
- **`minimal_neo4j.py`** - Neo4j interface with fallback database
- **`minimal_mcp_server.py`** - FastMCP server with resources, tools, and prompts
- **`main.py`** - Server entry point with configuration

### Size Comparison

- **Full Lila System**: 1.3MB+ with complex dependencies
- **Minimal MCP Server**: ~100KB with only essential components

### Dependencies

```
fastmcp>=2.12.3    # MCP server framework with HTTP transport
neo4j>=5.15.0      # Database driver
pydantic>=2.6.0    # Data validation
python-dotenv      # Environment configuration
```

### Transport Protocol

This server uses **HTTP transport** (FastMCP 2.0 standard):
- Runs as a web service accessible via URL
- Supports concurrent client connections
- Full bidirectional communication over HTTP
- Ideal for Docker deployment and network access

**Not STDIO transport** (which is for client-launched subprocesses)

## Sample Data

The system includes sample personas for demonstration:

- **Lila**: AI Research Assistant (Secure attachment)
- **Alex**: Software Engineer (Secure attachment)

These can be queried through the MCP resources to test functionality.

## Integration

Use this MCP server with MCP-compatible clients via HTTP transport:

```json
{
  "mcpServers": {
    "lila-psychology": {
      "url": "http://localhost:8765/mcp/",
      "transport": "http"
    }
  }
}
```

For FastMCP clients:

```python
from fastmcp import Client

# Connect to HTTP MCP server
client = Client("http://localhost:8765/mcp/")

async with client:
    # Query personas
    personas = await client.get_resource("neo4j://personas/all")

    # Analyze compatibility
    result = await client.call_tool("analyze_persona_compatibility", {
        "persona_a_id": "lila",
        "persona_b_id": "alex"
    })
```

## Development

### Development Workflow

**1. Start with MCP Inspector (Recommended - uv-Native)**:
```bash
# BEST: Auto-configuration with fastmcp.json (uv-native)
fastmcp dev                     # Automatically detects all dependencies

# Custom port if needed:
fastmcp dev --server-port 6350  # Avoids port conflicts

# FALLBACK: Explicit dependencies (if auto-detection fails)
fastmcp dev simple_lila_mcp_server.py --with fastmcp --with neo4j --with pydantic --with python-dotenv
```

**2. Test Production HTTP Deployment**:
```bash
# BEST: Auto-configuration HTTP transport (uv-native)
fastmcp run                     # Uses fastmcp.json auto-configuration

# Custom port if needed:
fastmcp run --port 9000         # Override port

# Docker deployment (for full production testing)
docker compose up -d
```

**3. Client Integration Testing**:
```bash
# BEST: Auto-configuration for MCP clients (uv-native)
fastmcp install claude-desktop  # Uses fastmcp.json auto-configuration
fastmcp install cursor          # Uses fastmcp.json auto-configuration
fastmcp install mcp-json        # Generic MCP JSON config

# FALLBACK: Explicit dependencies (if auto-detection fails)
fastmcp install claude-desktop simple_lila_mcp_server.py --with neo4j --with pydantic --with python-dotenv
fastmcp install cursor simple_lila_mcp_server.py --with neo4j --with pydantic --with python-dotenv
```

### Development Features

The minimal implementation is designed for:

- **Fast startup** - No complex initialization
- **Low resource usage** - Minimal memory footprint
- **Inspector Integration** - Built-in development and testing tools
- **Simple deployment** - Single container with few dependencies
- **Easy maintenance** - Clear, focused codebase

### FastMCP CLI Commands (V2)

```bash
# Development with Inspector (fastmcp.json - Recommended)
fastmcp dev                               # Uses fastmcp.json auto-configuration
fastmcp dev --server-port 6300           # Custom Inspector port

# Development with explicit dependencies (fallback)
fastmcp dev simple_lila_mcp_server.py --with fastmcp --with neo4j --with pydantic --with python-dotenv

# Run with different transports (HTTP recommended for production)
fastmcp run --transport http             # HTTP transport (production ready)
fastmcp run --transport http --port 8765 # HTTP with custom port
fastmcp run --transport stdio            # STDIO for Inspector development only

# Explicit transport configuration
fastmcp run simple_lila_mcp_server.py --transport http --port 8765 --with fastmcp --with neo4j --with pydantic
fastmcp run simple_lila_mcp_server.py --transport stdio --with fastmcp --with neo4j --with pydantic  # Dev only

# Install in MCP clients (uses fastmcp.json automatically)
fastmcp install claude-desktop           # Auto-configuration
fastmcp install cursor                   # Auto-configuration
fastmcp install mcp-json                 # Generic MCP JSON config

# Explicit client installation
fastmcp install claude-desktop simple_lila_mcp_server.py --with neo4j --with pydantic --with python-dotenv
fastmcp install cursor simple_lila_mcp_server.py --with neo4j --with pydantic --with python-dotenv

# Inspect server capabilities
fastmcp inspect                          # Uses fastmcp.json (Recommended)
fastmcp inspect --format fastmcp         # Detailed FastMCP info
fastmcp inspect --format mcp             # Standard MCP protocol info
fastmcp inspect simple_lila_mcp_server.py       # Explicit entrypoint (fallback)
```

For full Lila system capabilities, use the main system at the repository root.

## Troubleshooting

### MCP Inspector Connection Issues

#### `ERR_CONNECTION_REFUSED` or `[object Object]` Error - CRITICAL

**Problem**: Inspector UI loads but clicking "Connect" shows:
- `ERR_CONNECTION_REFUSED` on port 6277, OR
- `error: Failed to spawn: '[object Object]'` in console

**Root Cause**: MCP Inspector's JavaScript argument parser incorrectly handles `>=` operators in dependency version strings. When `fastmcp.json` contains:
```json
"dependencies": ["fastmcp>=2.12.3", "neo4j>=5.15.0"]
```

The Inspector splits `neo4j>=5.15.0` into: `neo4j`, `[object Object]`, `=5.15.0`, causing `uv` to fail.

**Solution** (Already Configured): Use `"project": "."` in `fastmcp.json`:
```json
{
  "environment": {
    "type": "uv",
    "python": "3.12",
    "project": "."  // ✓ Uses pyproject.toml, avoids bug
  }
}
```

**DO NOT USE** explicit dependencies with `>=` operators in `fastmcp.json` - they will break the Inspector.

#### Port Already in Use - PORT IS IN USE at port 6277

**Problem**: `fastmcp dev` fails with "PORT IS IN USE at port 6277"

**Root Cause**: `fastmcp dev` spawns multiple background processes (Python, node, npm, mcp-inspector) that must ALL be killed.

**Solution**:
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
fastmcp dev
```

**Check Running Processes**:
```bash
# See all MCP-related processes
ps aux | grep -E "fastmcp|mcp-inspector" | grep -v grep

# Check port usage
ss -tulpn | grep -E "6274|6277"
```

#### Inspector Proxy Shows "Error Connecting"

**Problem**: Inspector web UI loads but shows connection error

**Solution**: Ensure you're using the default server configuration in `fastmcp.json`:
- Default: `simple_lila_mcp_server.py` (mock data, works without Neo4j)
- Production: `lila_mcp_server.py` (requires Neo4j running)

**Validation**:
```bash
# Test server capabilities
python test_mcp_validation.py

# Expected output:
# ✅ Resources found: 6-9
# ✅ Tools found: 8
# ✅ Prompts found: 3
```

### Virtual Environment Issues

#### Understanding VIRTUAL_ENV Mismatch Warnings

**Warning: "VIRTUAL_ENV does not match the project environment path"**
```bash
warning: `VIRTUAL_ENV=/home/donbr/midlife/lila-pydanticai-phase1/.venv` does not match the project environment path `.venv` and will be ignored; use `--active` to target the active environment instead
```

**Root Cause Analysis:**

This warning occurs due to **uv's strict virtual environment path resolution logic**:

1. **uv Project Environment Detection**: When uv operates in a project directory, it expects to find or create a virtual environment at `.venv` (the default project environment path)

2. **VIRTUAL_ENV Environment Variable**: This variable points to an active virtual environment, often set by:
   - Manual `source .venv/bin/activate`
   - IDE integrations (VS Code, PyCharm)
   - Container environments
   - Previous virtualenv/conda activations

3. **Path Mismatch Logic**: uv compares `$VIRTUAL_ENV` against the expected project environment path:
   ```
   VIRTUAL_ENV=/app/.venv (from Docker container)
   Project expects: /home/donbr/midlife/lila-pydanticai-phase1/docker/mcp-standalone/.venv
   Result: MISMATCH → Warning + Ignore VIRTUAL_ENV
   ```

**When This Warning Appears:**
- **Container Development**: Docker containers set `VIRTUAL_ENV=/app/.venv` but host expects different path
- **IDE Environment Conflicts**: VS Code or other IDEs activate environments with different paths
- **Cross-Platform Development**: Windows/Linux path differences
- **Manual Environment Activation**: Using `source .venv/bin/activate` when uv expects different path

**Why It's Usually Harmless:**

**The warning is informational, not an error**:
- uv **ignores** the conflicting `VIRTUAL_ENV` and uses its project environment logic
- uv **creates or uses** the correct `.venv` directory regardless
- **Functionality is preserved** - packages install to the right location
- **No data loss** occurs

**When It Could Be Problematic:**
1. **Multiple environments exist** with different dependency versions
2. **Shared development** where team members expect consistent paths
3. **CI/CD pipelines** that rely on specific environment variables
4. **Automated scripts** that depend on `VIRTUAL_ENV` accuracy

**Solutions:**
```bash
# Option 1: Do nothing (recommended)
# Commands work correctly despite the warning

# Option 2: Clear environment variable before running
unset VIRTUAL_ENV
fastmcp run

# Option 3: Use UV_PROJECT_ENVIRONMENT to override default path
export UV_PROJECT_ENVIRONMENT=/path/to/desired/venv
fastmcp run

# Option 4: Use --quiet flag to suppress warnings
fastmcp run --quiet

# Option 5: Deactivate parent environment first
deactivate  # If in activated environment
cd docker/mcp-standalone
fastmcp run

# Option 6: Use environment-specific commands
# For development (avoids manual activation)
fastmcp dev  # Uses uv's environment management automatically

# For production (Docker handles environments)
docker compose up -d
```

#### Environment Validation Commands

**Verify your environment is set up correctly:**
```bash
# 1. Check current environment status
echo "VIRTUAL_ENV: $VIRTUAL_ENV"
echo "Current directory: $(pwd)"

# 2. Test uv environment detection
fastmcp inspect  # Should work regardless of VIRTUAL_ENV warning

# 3. Verify FastMCP can create isolated environment
fastmcp dev --server-port 6350  # Creates isolated environment

# 4. Check if dependencies are available
python -c "import fastmcp, neo4j, pydantic; print('Dependencies OK')"

# 5. Validate .env file loading
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
print('Neo4j URI:', os.getenv('NEO4J_URI', 'Not found'))
print('Logfire enabled:', os.getenv('ENABLE_LOGFIRE_TELEMETRY', 'Not found'))
"
```

#### Development Workflow Best Practices

**Recommended Patterns (avoid VIRTUAL_ENV conflicts):**
```bash
# GOOD: Use uv-native commands (automatic environment management)
fastmcp dev     # Auto-detects and manages environment
fastmcp run     # Uses project environment correctly
fastmcp inspect # Works regardless of active environment

# GOOD: Use .env files instead of manual activation
# All environment variables loaded automatically from .env

# AVOID: Manual virtual environment activation before fastmcp
source .venv/bin/activate  # Can cause path conflicts
fastmcp dev                # May show VIRTUAL_ENV warning

# BETTER: Let fastmcp handle environment management
fastmcp dev  # Creates isolated environment automatically
```

**IDE Integration Tips:**
```bash
# VS Code: Use Python interpreter selection instead of manual activation
# 1. Open Command Palette (Ctrl+Shift+P)
# 2. "Python: Select Interpreter"
# 3. Choose the correct .venv/bin/python
# 4. VS Code will handle environment automatically

# PyCharm: Configure Project Interpreter
# File → Settings → Project → Python Interpreter
# Add interpreter from .venv directory
```

**Container Development:**
```bash
# Host development (recommended for FastMCP)
cd docker/mcp-standalone
fastmcp dev  # Uses host environment management

# Container development (for production testing)
docker compose up -d
# Environment handled by Docker automatically
```

### FastMCP CLI Issues

**Error: "No server object found"**
```bash
# Make sure you're in the correct directory
cd docker/mcp-standalone

# Use explicit entrypoint syntax if auto-detection fails
fastmcp dev simple_lila_mcp_server.py:mcp --with fastmcp --with neo4j --with pydantic --with python-dotenv
fastmcp inspect simple_lila_mcp_server.py:mcp
```

**Error: "Could not load module" or Import Failures**
Modern fastmcp.json configuration should work automatically:
```bash
# WORKING: Auto-detection with fastmcp.json
fastmcp dev                     # Uses fastmcp.json automatically
fastmcp run                     # Uses fastmcp.json automatically
fastmcp inspect                 # Uses fastmcp.json automatically

# FALLBACK: Use explicit dependencies if auto-detection fails
fastmcp dev simple_lila_mcp_server.py --with fastmcp --with neo4j --with pydantic --with python-dotenv
```

**Inspector Port Conflicts**
```bash
# Error: "PORT IS IN USE at port 6277"
# Solution: Specify different server port
fastmcp dev main.py --with fastmcp --with neo4j --with pydantic --with python-dotenv --server-port 6280
```

**Missing `--with fastmcp` Dependency**
Always include `--with fastmcp` in dependency list:
```bash
# CORRECT: Include fastmcp dependency
fastmcp dev main.py --with fastmcp --with neo4j --with pydantic --with python-dotenv

# WRONG: Missing fastmcp dependency
fastmcp dev main.py --with neo4j --with pydantic --with python-dotenv  # May fail
```

### Transport and Connection Issues

**Inspector Transport Selection**
- Inspector automatically uses STDIO transport (correct)
- Do NOT manually select HTTP transport in Inspector UI
- STDIO transport is required for Inspector proxy communication

**Neo4j Connection Warnings**
- Neo4j warnings are normal when running locally without Docker
- Server automatically falls back to in-memory database with sample data
- For full Neo4j features, use `docker compose up -d neo4j` first

**HTTP vs STDIO Transport Confusion**
- **STDIO**: For Inspector testing and client integration (`fastmcp dev`)
- **HTTP**: For Docker deployment and network access (`docker compose up -d`)
- **SSE**: Deprecated, avoid using

### Dependency Management Issues

**Missing Dependencies**
```bash
# Install FastMCP globally if missing
pip install fastmcp

# Or use uv
uv add fastmcp

# Verify installation
fastmcp --version
```

**Python Version Compatibility**
```bash
# Specify Python version if needed
fastmcp dev main.py --python 3.11 --with fastmcp --with neo4j --with pydantic --with python-dotenv
```

**uv Environment Issues**
```bash
# If uv is not available, install it first
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or use pip
pip install uv
```

### Testing and Validation

**Verify Server Functionality**
```bash
# 1. Test basic server inspection
fastmcp inspect main.py

# 2. Test Inspector integration
fastmcp dev main.py --with fastmcp --with neo4j --with pydantic --with python-dotenv

# 3. Test HTTP deployment
fastmcp run main.py --transport http --port 8765

# 4. Test Docker deployment + MCP client validation
docker compose up -d
python -c "
from fastmcp import Client
import asyncio

async def test():
    client = Client('http://localhost:8765/mcp/')
    async with client:
        personas = await client.get_resource('neo4j://personas/all')
        print(f'✅ Docker deployment working: {len(personas) if personas else 0} personas')

asyncio.run(test())
"
```

**Common Testing Workflow**
1. Start with `fastmcp inspect main.py` to verify basic functionality
2. Use `fastmcp dev` for interactive testing with Inspector
3. Test HTTP transport for production deployment scenarios
4. Use Docker for full stack testing with Neo4j database

**Expected Inspector Behavior**
- Console shows: "Starting MCP inspector..."
- Proxy server starts on specified port (default 6277, custom with `--server-port`)
- Inspector URL with token is displayed
- Web interface should connect successfully via STDIO transport
- All resources, tools, and prompts should be visible and testable

## License

Same as main Lila project.