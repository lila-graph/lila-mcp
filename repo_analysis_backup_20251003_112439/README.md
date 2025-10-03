# Repository Architecture Documentation

## Overview

The **Lila MCP** (Model Context Protocol) system is a production-ready psychological intelligence server that provides AI-powered relationship modeling and analysis through the MCP protocol. Built on Neo4j graph database and FastMCP framework, it exposes psychological relationship data, tools for relationship management, and LLM-ready prompts for attachment theory-based assessments.

**Key Capabilities:**
- **Psychological Intelligence**: Attachment theory modeling with Big Five personality traits
- **Graph-Based Relationships**: Neo4j database for complex relationship networks
- **MCP Protocol**: Full Model Context Protocol implementation via FastMCP
- **Dual Architecture**: Production server with Neo4j + development server with mock data
- **Comprehensive API**: 5-9 resources, 6-8 tools, and 3 psychological assessment prompts

**Repository Location**: `/home/donbr/lila-graph/lila-mcp`

**Key Statistics**:
- **6 Python modules** (779-830 lines each for servers)
- **2 server implementations** (production + development)
- **8 MCP tools** for psychological operations
- **3 MCP prompts** for LLM-based assessments
- **9 MCP resources** (2 direct + 7 templated)
- **Neo4j integration** with connection pooling and retry logic
- **FastMCP framework** for MCP protocol compliance

---

## Quick Start

### For Different Audiences

**Developers New to the Project:**
1. Start with this README for overall architecture
2. Read [Component Inventory](docs/01_component_inventory.md) for detailed module breakdown
3. Review [Architecture Diagrams](diagrams/02_architecture_diagrams.md) for visual system design
4. Study [Data Flows](docs/03_data_flows.md) for understanding request/response cycles

**API Users:**
1. Jump to [API Reference](docs/04_api_reference.md) for complete endpoint documentation
2. Review code examples in API Reference for usage patterns
3. Check [Data Flows](docs/03_data_flows.md) for understanding tool invocation patterns

**DevOps/Infrastructure:**
1. Review [Architecture Diagrams](diagrams/02_architecture_diagrams.md) for deployment topology
2. Check `.env.example` for configuration requirements
3. Read `init_mcp_database.sh` for database initialization workflow
4. Review Docker Compose configuration for container orchestration

**Researchers/Psychological Modelers:**
1. Start with [API Reference](docs/04_api_reference.md) prompts section
2. Review attachment theory implementation in component inventory
3. Examine Big Five personality trait mappings
4. Study compatibility analysis algorithms

---

## Architecture Summary

### Layered Architecture

The Lila MCP system implements a **clean layered architecture** with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────┐
│  Presentation Layer: MCP Protocol (FastMCP Framework)  │
│  - HTTP/SSE Transport                                   │
│  - Resources, Tools, Prompts                            │
│  - Health Check Endpoint                                │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  Business Logic Layer: Application Servers              │
│  - LilaMCPServer (Production)        779 lines          │
│  - SimpleLilaMCPServer (Development) 830 lines          │
│  - Psychological Analysis Logic                         │
│  - Attachment Theory Algorithms                         │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  Data Access Layer: Database Interface                  │
│  - Neo4j Driver with Connection Pooling                 │
│  - Parameterized Cypher Queries                         │
│  - Session Management                                   │
│  - Mock Data Alternative (SimpleLilaMCPServer)          │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  External Systems                                       │
│  - Neo4j Graph Database                                 │
│  - Environment Configuration (.env)                     │
└─────────────────────────────────────────────────────────┘
```

### Key Architectural Patterns

**1. Dual-Implementation Architecture**
- **Production Path**: Full Neo4j integration for real-time data
- **Development Path**: In-memory mock data for testing without infrastructure
- **Shared Interface**: Both servers expose identical MCP endpoints
- **Benefits**: Easy testing, flexible deployment, rapid development

**2. Composition Over Inheritance**
- No class hierarchies - all classes are flat and independent
- Dependency injection for FastMCP and Neo4j driver
- Single responsibility principle throughout
- Easy to test, maintain, and extend

**3. Decorator-Based Endpoint Registration**
```python
@self.app.resource("neo4j://personas/all")
def get_all_personas() -> str:
    # Resource handler implementation
    pass

@self.app.tool()
async def update_relationship_metrics(...) -> str:
    # Tool handler implementation
    pass

@self.app.prompt()
def assess_attachment_style(...) -> str:
    # Prompt template generation
    pass
```

**4. Psychological Intelligence Integration**
- **Attachment Theory**: Secure, anxious, avoidant, exploratory styles
- **Big Five Personality**: OCEAN model (Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism)
- **Relationship Metrics**: Trust (0-10), intimacy (0-10), strength (0-10)
- **Emotional Analysis**: Valence tracking (-1 to +1), interaction recording

**5. Graph Database for Relationship Modeling**
- PersonaAgent nodes with psychological profiles
- RELATIONSHIP edges with bidirectional metrics
- Memory nodes for interaction history
- Goal nodes for relationship objectives

---

## Component Overview

### Dual-Server Architecture

| Component | Type | Lines | Database | Resources | Tools | Prompts | Use Case |
|-----------|------|-------|----------|-----------|-------|---------|----------|
| **LilaMCPServer** | Production | 779 | Neo4j | 5 | 6 | 3 | Production deployments |
| **SimpleLilaMCPServer** | Development | 830 | Mock data | 9 | 8 | 3 | Testing, development |

**Key Differences:**

**LilaMCPServer** (`lila_mcp_server.py`):
- Connects to Neo4j database with retry logic
- Real-time psychological intelligence queries
- Health check endpoint for container orchestration
- Production-ready error handling
- Requires Neo4j infrastructure

**SimpleLilaMCPServer** (`simple_lila_mcp_server.py`):
- In-memory mock data (Lila + Don personas)
- Enhanced debug logging
- Additional demo resources (emotional climate, trends, goals)
- Additional demo tools (commit state, finalize session)
- No database dependency - immediate startup

### MCP Protocol Components

**Resources** (Read-only data access):
1. `neo4j://personas/all` - All personas with psychological profiles
2. `neo4j://personas/{id}` - Specific persona by ID
3. `neo4j://relationships/all` - All relationships with metrics
4. `neo4j://relationships/{id1}/{id2}` - Specific relationship
5. `neo4j://interactions/recent/{count}` - Recent interactions
6. `neo4j://emotional_climate/current` - Current climate (SimpleLilaMCPServer only)
7. `neo4j://attachment_styles/analysis` - Compatibility matrix (SimpleLilaMCPServer only)
8. `neo4j://goals/active` - Active goals (SimpleLilaMCPServer only)
9. `neo4j://psychological_insights/trends` - Trends (SimpleLilaMCPServer only)

**Tools** (State-modifying operations):
1. `update_relationship_metrics` - Modify trust/intimacy/strength with bounds checking
2. `record_interaction` - Log persona interactions with emotional valence
3. `analyze_persona_compatibility` - Attachment style compatibility analysis
4. `autonomous_strategy_selection` - AI-driven strategy based on attachment theory
5. `assess_goal_progress` - Track progress toward relationship goals
6. `generate_contextual_response` - Generate psychologically authentic responses
7. `commit_relationship_state` - Explicit state commit (SimpleLilaMCPServer only)
8. `finalize_demo_session` - Batch finalization (SimpleLilaMCPServer only)

**Prompts** (LLM-ready templates):
1. `assess_attachment_style` - Attachment theory-based assessment framework
2. `analyze_emotional_climate` - Emotional safety and dynamics evaluation
3. `generate_secure_response` - Security-building response generation

### Data Management Utilities

**Neo4jDataImporter** (`import_data.py`, 466 lines):
- Database initialization with retry logic (30 attempts)
- Schema creation: constraints and indexes
- DISC to Big Five personality trait mapping
- Seed data import from Cypher scripts or JSON
- Default persona creation (Lila + Alex)
- Import verification with node/relationship counts

**Neo4jDataExporter** (`export_data.py`, 295 lines):
- Export personas, relationships, memories, goals
- Generate portable Cypher scripts
- Data serialization with proper escaping
- CLI interface with argparse

### Testing and Validation

**test_mcp_validation.py** (172 lines):
- Direct connection test (in-memory with FastMCP Client)
- Inspector connection test (HTTP to localhost:6274)
- Comprehensive endpoint validation
- Summary reporting with pass/fail status

**architecture.py** (363 lines):
- Claude Agent SDK for automated documentation
- 5-phase analysis pipeline
- Specialized agents (analyzer, doc-writer)
- Progress visibility with tool usage display

---

## Data Flows

### Key Flow Patterns

**Pattern 1: Resource Query Flow**
```
Client Request
    ↓
FastMCP Protocol Routing
    ↓
Resource Handler (get_all_personas)
    ↓
Neo4j Session Created
    ↓
Parameterized Cypher Query Executed
    ↓
Results Processed & Formatted
    ↓
JSON String Response Wrapped
    ↓
MCP Response to Client
```

**Performance**: Sub-100ms for simple queries (local Neo4j)

**Pattern 2: Tool Invocation Flow**
```
Client Tool Call
    ↓
FastMCP Parameter Validation
    ↓
Tool Handler (async function)
    ↓
Neo4j Transaction Started
    ↓
Bounds-Checked Update Query
    ↓
Results Verified & Formatted
    ↓
Transaction Auto-Committed
    ↓
JSON String Response
    ↓
MCP Response to Client
```

**Performance**: 100-500ms depending on operation complexity

**Pattern 3: Prompt Generation Flow**
```
Client Prompt Request
    ↓
Prompt Handler (sync function)
    ↓
Template Formatted with Parameters
    ↓
Psychological Framework Injected
    ↓
Formatted Prompt String
    ↓
MCP Response to Client
    ↓
Client Sends to LLM
```

**Performance**: <50ms (no database access)

### Request/Response Cycle Details

**Initialize Sequence:**
1. Client sends `initialize` with protocol version
2. Server returns capabilities (resources, tools, prompts)
3. Client sends `initialized` acknowledgment
4. Session established, ready for requests

**Resource Access:**
1. `resources/list` → Server returns resource descriptors
2. `resources/read` with URI → Server executes handler, returns content

**Tool Invocation:**
1. `tools/list` → Server returns tool schemas with JSON schemas
2. `tools/call` with name and args → Server executes, returns result

**Prompt Usage:**
1. `prompts/list` → Server returns available prompts
2. `prompts/get` with name and args → Server returns formatted template
3. Client uses template in LLM request

### Session Management

- **Stateless Request/Response**: No session persistence between calls
- **Connection Pooling**: Neo4j driver maintains connection pool (default: 100 max)
- **Transactional Isolation**: Each request creates new database session
- **Automatic Cleanup**: Context managers ensure session closure
- **No Explicit Commits**: Sessions auto-commit on success, rollback on exception

---

## API Highlights

### Most Important Resources

**1. Get All Personas** (`neo4j://personas/all`)
```json
{
  "personas": [
    {
      "id": "lila",
      "name": "Lila",
      "age": 28,
      "attachment_style": "secure",
      "personality": {
        "openness": 0.85,
        "conscientiousness": 0.80,
        "extraversion": 0.65,
        "agreeableness": 0.90,
        "neuroticism": 0.25
      }
    }
  ],
  "count": 2
}
```

**2. Get Relationship** (`neo4j://relationships/{id1}/{id2}`)
```json
{
  "relationship": {
    "persona1_id": "lila",
    "persona2_id": "alex",
    "trust_level": 7.5,
    "intimacy_level": 6.8,
    "relationship_strength": 7.2,
    "interaction_count": 15,
    "emotional_valence": 0.75
  }
}
```

### Most Important Tools

**1. Update Relationship Metrics**
```python
async with Client(mcp_server) as client:
    result = await client.call_tool("update_relationship_metrics", {
        "persona1_id": "lila",
        "persona2_id": "alex",
        "trust_delta": 0.5,
        "intimacy_delta": 0.3,
        "strength_delta": 0.4
    })
    # Returns updated metrics with bounds checking (0-10 scale)
```

**2. Analyze Compatibility**
```python
async with Client(mcp_server) as client:
    compatibility = await client.call_tool("analyze_persona_compatibility", {
        "persona1_id": "lila",
        "persona2_id": "alex",
        "relationship_type": "romantic"
    })
    # Returns: "High|Good|Moderate|Challenging|Difficult|Low"
    # With analysis and recommendations based on attachment theory
```

**3. Record Interaction**
```python
async with Client(mcp_server) as client:
    interaction = await client.call_tool("record_interaction", {
        "sender_id": "lila",
        "recipient_id": "alex",
        "content": "Thank you for your support today!",
        "emotional_valence": 0.8,
        "relationship_impact": 0.3
    })
    # Updates interaction count, last_interaction timestamp, rolling avg emotional_valence
```

### Attachment Compatibility Matrix

| Style 1 | Style 2 | Compatibility | Rationale |
|---------|---------|---------------|-----------|
| Secure | Secure | High | Both provide stability and emotional availability |
| Secure | Anxious | Good | Secure partner provides reassurance |
| Secure | Avoidant | Moderate | Secure partner helps avoidant open up gradually |
| Anxious | Anxious | Challenging | Both may escalate emotional intensity |
| Anxious | Avoidant | Difficult | Classic pursue-withdraw dynamic |
| Avoidant | Avoidant | Low | Both avoid emotional intimacy |

### Most Important Prompts

**1. Assess Attachment Style**
```python
async with Client(mcp_server) as client:
    prompt = await client.get_prompt("assess_attachment_style", {
        "persona_id": "alex",
        "observation_period": "past 6 months",
        "behavioral_examples": "Withdraws during conflict, prefers independence"
    })
    # Returns comprehensive framework for LLM analysis
    # Includes: Attachment styles, analysis dimensions, therapeutic implications
```

**Framework Includes:**
- 4 attachment styles (secure, anxious, avoidant, exploratory)
- 5 analysis dimensions (emotional regulation, intimacy comfort, patterns, communication, partner distress response)
- Expected output format with confidence levels
- Therapeutic implications and recommendations

---

## Key Technologies

### Core Stack

**Python 3.12+**
- Modern async/await support
- Type hints and annotations
- Pathlib for cross-platform paths

**FastMCP 2.12.3+**
- Complete MCP protocol implementation
- Decorator-based endpoint registration
- HTTP/SSE/STDIO transport support
- Automatic JSON schema generation from type hints

**Neo4j 5.15.0+**
- Graph database for relationship networks
- Cypher query language
- Connection pooling and retry logic
- ACID transactions

**Docker Compose**
- Container orchestration
- Service networking
- Health checks
- Volume management

### Key Libraries

**Database Integration:**
- `neo4j` (5.15.0+): Python driver for Neo4j
- Connection pooling, session management, parameterized queries

**Data Validation:**
- `pydantic` (2.6.0+): Data validation (declared but not actively used yet)
- `pydantic-settings` (2.2.0+): Settings management

**Configuration:**
- `python-dotenv` (1.0.0+): Environment variable loading from .env
- Environment-based configuration for deployment flexibility

**LLM Integration (Future-Ready):**
- `openai` (1.30.0+): OpenAI API client
- `anthropic` (0.25.0+): Anthropic API client
- `httpx` (0.27.0+): Modern async HTTP client
- `aiohttp` (3.9.0+): Async HTTP client/server

**Observability:**
- `logfire` (0.28.0+): Telemetry and monitoring (declared, ready for use)
- Structured logging throughout
- Health check endpoints

**Development Tools:**
- `pytest` (8.0.0+): Testing framework
- `pytest-asyncio` (0.23.0+): Async test support
- `black` (24.0.0+): Code formatter
- `ruff` (0.3.0+): Fast Python linter
- `claude-agent-sdk` (0.1.0+): Automated documentation generation

### Technology Decisions

**Why FastMCP?**
- Native MCP protocol support
- Decorator-based API is clean and intuitive
- Automatic schema generation from Python type hints
- Built-in transport layer (HTTP, SSE, STDIO)
- Active development and community

**Why Neo4j?**
- Graph database ideal for relationship networks
- Cypher query language is powerful and expressive
- Bidirectional relationship queries are native
- ACID transactions for data integrity
- Excellent Python driver support

**Why Dual Server Architecture?**
- Development without infrastructure (SimpleLilaMCPServer)
- Testing with predictable mock data
- Production with real-time database (LilaMCPServer)
- Identical interface for easy switching
- Faster iteration cycles

---

## Documentation Map

### Core Documentation

| Document | Purpose | Audience | Key Content |
|----------|---------|----------|-------------|
| **[Component Inventory](docs/01_component_inventory.md)** | Detailed module breakdown | Developers | Classes, methods, parameters, line numbers |
| **[Architecture Diagrams](diagrams/02_architecture_diagrams.md)** | Visual system design | All audiences | Mermaid diagrams, component relationships |
| **[Data Flows](docs/03_data_flows.md)** | Request/response cycles | Developers, API users | Sequence diagrams, message routing |
| **[API Reference](docs/04_api_reference.md)** | Complete API documentation | API users | Endpoints, parameters, examples |
| **This README** | Entry point overview | All audiences | Architecture, quick start, synthesis |

### Documentation Coverage

**Component Inventory** (Lines: 1560):
- Public API: All server classes, data management utilities
- MCP Resources: 9 resources with Cypher queries
- MCP Tools: 8 tools with parameters and returns
- MCP Prompts: 3 prompts with frameworks
- Internal Implementation: Configuration files, infrastructure scripts
- Entry Points: All execution modes
- Dependencies: External and standard library imports
- File statistics and code distribution

**Architecture Diagrams** (Lines: 1395):
- System architecture (layered view)
- Component relationships (dual-implementation)
- Class hierarchies (composition over inheritance)
- Module dependencies (clean dependency graph)
- All diagrams in Mermaid format with detailed explanations

**Data Flows** (Lines: 1586):
- Query flow (resource access)
- Interactive session flow (tool invocation)
- Tool permission callback flow (not implemented, future)
- MCP server communication flow (initialization, runtime)
- Message parsing and routing (JSON-RPC 2.0)
- Performance considerations
- Security considerations
- Future enhancement opportunities

**API Reference** (Lines: 2541):
- Core classes (LilaMCPServer, SimpleLilaMCPServer)
- MCP Resources (9 endpoints with schemas)
- MCP Tools (8 tools with signatures)
- MCP Prompts (3 templates with frameworks)
- Data management APIs (import/export)
- Configuration (environment variables, files)
- Usage patterns and best practices
- Complete working examples

### Reading Paths

**Path 1: Quick API Usage**
1. This README (Overview + API Highlights)
2. API Reference (Specific endpoints you need)
3. Data Flows (Understanding request patterns)

**Path 2: Deep System Understanding**
1. This README (Architecture Summary)
2. Architecture Diagrams (Visual understanding)
3. Component Inventory (Detailed implementation)
4. Data Flows (Runtime behavior)
5. API Reference (Complete reference)

**Path 3: Deployment and Operations**
1. This README (Architecture + Technologies)
2. Architecture Diagrams (Deployment topology)
3. API Reference Configuration section
4. Component Inventory Infrastructure section

**Path 4: Extending the System**
1. This README (Component Overview)
2. Component Inventory (Implementation details)
3. Architecture Diagrams (Class hierarchies, dependencies)
4. Data Flows (Message routing, handlers)

---

## Getting Started

### Prerequisites

**Required:**
- Python 3.12+
- Docker and Docker Compose (for Neo4j)
- UV package manager (or pip)

**Optional:**
- OpenAI API key (for LLM integration)
- Anthropic API key (for Claude integration)
- Logfire account (for observability)

### Installation

**1. Clone Repository:**
```bash
cd /home/donbr/lila-graph/lila-mcp
```

**2. Install Dependencies:**
```bash
# Using UV (recommended)
uv sync

# Or using pip
pip install -e .
```

**3. Configure Environment:**
```bash
# Copy example configuration
cp .env.example .env

# Edit .env with your settings
# At minimum, set NEO4J_PASSWORD
```

**4. Initialize Database:**
```bash
# Start Neo4j and import data
./init_mcp_database.sh

# This script:
# - Starts Docker Compose
# - Waits for Neo4j readiness
# - Imports schema and seed data
# - Verifies import success
```

### Development Workflow

**Option 1: Development Server (No Database Required)**
```bash
# Start SimpleLilaMCPServer with FastMCP Inspector
fastmcp dev simple_lila_mcp_server.py

# Access Inspector at:
# http://localhost:6274/
# Uses mock data, no Neo4j required
```

**Option 2: Production Server (Requires Neo4j)**
```bash
# Ensure Neo4j is running
docker compose up -d

# Start LilaMCPServer with FastMCP Inspector
fastmcp dev lila_mcp_server.py

# Access Inspector at http://localhost:6274/
# Uses live Neo4j database
```

**Option 3: Direct Python Execution**
```bash
# Production server
python lila_mcp_server.py

# Development server
python simple_lila_mcp_server.py
```

### Validation

**Run Test Suite:**
```bash
python test_mcp_validation.py

# Tests:
# - Direct connection (in-memory)
# - Inspector connection (HTTP)
# - All resources, tools, and prompts
```

**Expected Output:**
```
=================================================
MCP Validation Test Suite
=================================================

Testing direct connection...
✓ Server is connected
✓ Server responds to ping
✓ Resources available: 9
✓ Tools available: 8
✓ Prompts available: 3
Direct connection test: PASSED

Testing Inspector connection...
✓ Inspector connection established
Inspector connection test: PASSED

Summary:
  Direct connection: PASSED
  Inspector connection: PASSED
  Resources: 9
  Tools: 8
  Prompts: 3
```

### Quick API Examples

**Example 1: Get All Personas**
```python
from fastmcp import Client
import asyncio
import json

async def main():
    async with Client("http://localhost:8766/") as client:
        personas_json = await client.read_resource("neo4j://personas/all")
        personas = json.loads(personas_json)

        for persona in personas['personas']:
            print(f"{persona['name']}: {persona['attachment_style']} attachment")

asyncio.run(main())
```

**Example 2: Update Relationship**
```python
from fastmcp import Client
import asyncio
import json

async def main():
    async with Client("http://localhost:8766/") as client:
        result = await client.call_tool("update_relationship_metrics", {
            "persona1_id": "lila",
            "persona2_id": "alex",
            "trust_delta": 0.5,
            "intimacy_delta": 0.3
        })

        data = json.loads(result.content[0].text)
        rel = data['updated_relationship']
        print(f"Trust: {rel['trust_level']:.2f}/10")
        print(f"Intimacy: {rel['intimacy_level']:.2f}/10")

asyncio.run(main())
```

**Example 3: Analyze Compatibility**
```python
from fastmcp import Client
import asyncio
import json

async def main():
    async with Client("http://localhost:8766/") as client:
        compat = await client.call_tool("analyze_persona_compatibility", {
            "persona1_id": "lila",
            "persona2_id": "alex",
            "relationship_type": "romantic"
        })

        data = json.loads(compat.content[0].text)
        analysis = data['compatibility_analysis']
        print(f"Compatibility: {analysis['compatibility_level']}")
        print(f"Analysis: {analysis['analysis']}")

asyncio.run(main())
```

### Data Management

**Import Data:**
```bash
python import_data.py \
  --schema graphs/lila-graph-schema-v8.json \
  --seed-data seed_data.cypher \
  --uri bolt://localhost:7687 \
  --user neo4j \
  --password your_password \
  --create-defaults
```

**Export Data:**
```bash
python export_data.py \
  --output seed_data.cypher \
  --uri bolt://localhost:7687 \
  --user neo4j \
  --password your_password
```

---

## Unique Features

### 1. Psychological Intelligence

**Attachment Theory Integration:**
- Four attachment styles: secure, anxious, avoidant, exploratory
- Compatibility matrix for relationship analysis
- Strategy selection based on attachment patterns
- Security-building response generation

**Big Five Personality Traits:**
- OCEAN model (Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism)
- DISC to Big Five mapping for behavioral styles
- Personality-driven interaction strategies
- Trait-based compatibility calculations

**Relationship Metrics:**
- Trust level (0-10 scale with bounds checking)
- Intimacy level (0-10 scale)
- Relationship strength (0-10 scale)
- Emotional valence (-1 to +1)
- Interaction count tracking
- Last interaction timestamps

### 2. Dual Architecture Design

**Flexibility:**
- Production server for real deployments
- Development server for testing
- Identical MCP interface
- Easy switching between modes

**Benefits:**
- No infrastructure for development
- Predictable mock data for testing
- Fast iteration cycles
- Same code paths in production

### 3. Graph Database Modeling

**Relationship Networks:**
- Bidirectional RELATIONSHIP edges
- PersonaAgent nodes with full profiles
- Memory nodes for interaction history
- Goal nodes for relationship objectives

**Cypher Queries:**
- Parameterized for security
- Bidirectional matching
- Bounds checking in database
- Atomic updates with transactions

### 4. MCP Protocol Native

**FastMCP Framework:**
- Decorator-based endpoint registration
- Automatic JSON schema generation
- Type-safe parameters
- Multiple transport options (HTTP, SSE, STDIO)

**Protocol Compliance:**
- Full MCP specification support
- Resources, tools, and prompts
- JSON-RPC 2.0 messaging
- Proper error handling

---

## Statistics and Metrics

### Codebase Distribution

| Category | Lines | Percentage |
|----------|-------|------------|
| MCP Servers | 1,609 | 48% |
| Data Management | 761 | 23% |
| Testing/Analysis | 535 | 16% |
| Configuration | 431 | 13% |
| **Total** | **3,336** | **100%** |

### Component Complexity

| File | Lines | Complexity | Purpose |
|------|-------|------------|---------|
| `lila_mcp_server.py` | 779 | High | Production MCP server |
| `simple_lila_mcp_server.py` | 830 | Medium | Development MCP server |
| `import_data.py` | 466 | Medium | Database initialization |
| `export_data.py` | 295 | Low | Data export utility |
| `test_mcp_validation.py` | 172 | Low | Validation suite |
| `architecture.py` | 363 | Medium | Documentation generator |
| `init_mcp_database.sh` | 203 | Medium | Infrastructure automation |

### API Surface Area

| Category | LilaMCPServer | SimpleLilaMCPServer |
|----------|---------------|---------------------|
| **Resources** | 5 | 9 |
| **Tools** | 6 | 8 |
| **Prompts** | 3 | 3 |
| **Total Endpoints** | **14** | **20** |

### Database Schema

| Entity Type | Properties | Indexes | Constraints |
|-------------|-----------|---------|-------------|
| PersonaAgent | 15+ | 1 (attachment_style) | 2 (persona_id, name) |
| RELATIONSHIP | 10+ | 1 (relationship_type) | 0 |
| Memory | 8+ | 1 (memory_type) | 1 (memory_id) |
| Goal | 9+ | 1 (goal_type) | 1 (goal_id) |

---

## References

### Detailed Documentation

1. **[Component Inventory](docs/01_component_inventory.md)** - Comprehensive module breakdown
   - Public API documentation with line numbers
   - All classes, methods, and parameters
   - Entry points and execution modes
   - Dependencies and imports
   - 1,560 lines of detailed technical reference

2. **[Architecture Diagrams](diagrams/02_architecture_diagrams.md)** - Visual system design
   - System architecture (layered view)
   - Component relationships (dual-implementation)
   - Class hierarchies (composition patterns)
   - Module dependencies (clean graphs)
   - 1,395 lines with Mermaid diagrams

3. **[Data Flows](docs/03_data_flows.md)** - Runtime behavior analysis
   - Query flow (resource access)
   - Interactive session flow (tool invocation)
   - MCP server communication flow
   - Message parsing and routing
   - 1,586 lines with sequence diagrams

4. **[API Reference](docs/04_api_reference.md)** - Complete API documentation
   - All resources, tools, and prompts
   - Parameters, returns, and schemas
   - Configuration options
   - Usage patterns and examples
   - 2,541 lines with working code

### Configuration Files

- **`.env.example`** - Complete environment variable reference
- **`fastmcp.json`** - FastMCP server configuration
- **`pyproject.toml`** - Python project dependencies and metadata
- **`.mcp.json`** - MCP client configuration for Claude Desktop

### Source Files

- **`lila_mcp_server.py`** - Production MCP server implementation
- **`simple_lila_mcp_server.py`** - Development MCP server with mock data
- **`import_data.py`** - Database initialization and schema loading
- **`export_data.py`** - Data export and Cypher script generation
- **`test_mcp_validation.py`** - Comprehensive validation test suite
- **`architecture.py`** - Automated documentation generation tool
- **`init_mcp_database.sh`** - Database initialization bash script

### External Resources

- **FastMCP Documentation**: https://gofastmcp.com/
- **MCP Protocol Specification**: https://modelcontextprotocol.io/
- **Neo4j Python Driver**: https://neo4j.com/docs/python-manual/current/
- **Claude Agent SDK**: https://github.com/anthropics/claude-agent-sdk

---

## Development Philosophy

### Design Principles

**1. Simplicity Over Complexity**
- Flat class hierarchies (no inheritance)
- Composition over inheritance
- Single responsibility principle
- Clear separation of concerns

**2. Testability First**
- Mock data for testing without infrastructure
- Direct connection testing (in-memory)
- Comprehensive validation suite
- Predictable behavior

**3. Developer Experience**
- Clear error messages
- Comprehensive documentation
- Working examples
- Type hints throughout

**4. Production Ready**
- Health check endpoints
- Connection pooling
- Retry logic
- Graceful degradation

**5. Psychological Intelligence**
- Attachment theory foundation
- Evidence-based compatibility
- Big Five personality integration
- Therapeutic framework awareness

### Architectural Strengths

1. **Clean layered architecture** with clear separation
2. **Dual implementation** for development/production
3. **Decorator-based routing** for maintainability
4. **Parameterized queries** for security
5. **Mock data testing** without infrastructure
6. **Container-first design** with Docker Compose
7. **Health check endpoints** for orchestration
8. **Configuration externalization** for flexibility
9. **Psychological intelligence** with proven models
10. **Repository analysis** with Claude Agent SDK

### Future Enhancement Opportunities

**Short-Term:**
1. Use Pydantic models for JSON serialization
2. Add Redis caching for frequently accessed data
3. Implement rate limiting middleware
4. Add observability with Logfire integration
5. Extract common server interface

**Medium-Term:**
1. Implement AuthProvider for authentication
2. Add tool-level permission decorators
3. Database migrations for schema versioning
4. Enhanced error handling with custom exceptions
5. API versioning for backward compatibility

**Long-Term:**
1. Full RBAC with user roles and permissions
2. GraphQL integration for flexible queries
3. Streaming responses for long operations
4. Subscription support for real-time updates
5. Multi-tenancy with row-level security

---

## Conclusion

The Lila MCP system provides a **production-ready, psychologically intelligent relationship modeling platform** through the Model Context Protocol. With its dual architecture design, comprehensive API, and attachment theory foundation, it offers both flexibility for development and robustness for production deployments.

**Key Takeaways:**

- **Comprehensive**: 14-20 MCP endpoints covering resources, tools, and prompts
- **Flexible**: Dual architecture for development and production
- **Intelligent**: Attachment theory and Big Five personality integration
- **Well-Documented**: 7,000+ lines of documentation with diagrams and examples
- **Production-Ready**: Health checks, retry logic, connection pooling, Docker support
- **Developer-Friendly**: Mock data, FastMCP Inspector, comprehensive testing

**Get Started:**
1. Review this README for overall understanding
2. Run `./init_mcp_database.sh` to initialize infrastructure
3. Start `fastmcp dev simple_lila_mcp_server.py` for development
4. Explore the FastMCP Inspector at http://localhost:6274/
5. Read the API Reference for detailed endpoint documentation

**For Support:**
- Review detailed documentation in `repo_analysis/docs/`
- Check diagrams in `repo_analysis/diagrams/`
- Run validation tests with `test_mcp_validation.py`
- Consult external resources (FastMCP, MCP Protocol, Neo4j)

**Repository Location**: `/home/donbr/lila-graph/lila-mcp`

---

*Documentation generated on 2025-10-03 using Claude Agent SDK*
