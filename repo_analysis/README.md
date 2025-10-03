# Repository Architecture Documentation

## Overview

**Lila MCP** is a sophisticated multi-domain agent orchestration system that combines psychological relationship modeling with advanced AI agent coordination. The project provides:

- **Psychological Intelligence MCP Servers**: FastMCP-based servers exposing relationship data, psychological analysis tools, and attachment theory prompts through the Model Context Protocol
- **Multi-Domain Orchestrators**: Framework for coordinating specialized AI agents across different domains (architecture analysis, UX design, etc.)
- **Tool Integration Layer**: Registry system for managing MCP servers, external tools, and graceful degradation
- **Neo4j Integration**: Graph database backend for modeling complex psychological relationships and persona interactions

### What Problem Does It Solve?

1. **Complex Workflow Orchestration**: Coordinates multiple AI agents across sequential phases with cost tracking, output verification, and error recovery
2. **Psychological Relationship Modeling**: Provides data structures and tools for modeling attachment styles, trust metrics, and relationship dynamics
3. **Extensible Agent Framework**: Base classes and patterns for creating domain-specific orchestrators with minimal boilerplate
4. **Tool Availability Management**: Graceful degradation when optional tools are unavailable, with fallback options and setup guidance

### Who Is It For?

- **AI Researchers**: Exploring multi-agent orchestration and psychological modeling
- **Software Architects**: Building complex agentic workflows with tool integration
- **UX/Product Teams**: Leveraging AI agents for comprehensive design workflows
- **Developers**: Creating custom orchestrators for specific domains or use cases

---

## Quick Start

### Understanding the Documentation

This documentation is organized into four main areas:

1. **[Component Inventory](docs/01_component_inventory.md)** - Complete catalog of all classes, methods, and entry points
2. **[Architecture Diagrams](diagrams/02_architecture_diagrams.md)** - Visual system architecture, dependencies, and data flows
3. **[Data Flows](docs/03_data_flows.md)** - Detailed sequence diagrams showing how information moves through the system
4. **[API Reference](docs/04_api_reference.md)** - Complete API documentation with examples and best practices

### Recommended Reading Order

**For New Developers:**
1. Start with this README for high-level understanding
2. Review [Architecture Diagrams](diagrams/02_architecture_diagrams.md) for visual system overview
3. Read [Component Inventory](docs/01_component_inventory.md) to understand available components
4. Consult [API Reference](docs/04_api_reference.md) when implementing

**For System Architects:**
1. Begin with [Architecture Diagrams](diagrams/02_architecture_diagrams.md) for design patterns
2. Study [Data Flows](docs/03_data_flows.md) for interaction patterns
3. Reference [Component Inventory](docs/01_component_inventory.md) for extension points

**For Integration Developers:**
1. Jump to [API Reference](docs/04_api_reference.md) for implementation details
2. Check [Data Flows](docs/03_data_flows.md) for integration patterns
3. Use [Component Inventory](docs/01_component_inventory.md) as reference

### How to Navigate

- All documentation includes source file references with line numbers
- Cross-references link between documents for deep dives
- Code examples are complete and runnable
- Diagrams use Mermaid for interactive visualization

---

## Architecture Summary

### Layered Architecture

The system follows a **6-layer architecture** with clear separation of concerns:

```
┌─────────────────────────────────────────┐
│     Presentation Layer                  │
│     - CLI Entry Points                  │
│     - HTTP Health Checks                │
└─────────────────────────────────────────┘
┌─────────────────────────────────────────┐
│     Orchestration Layer                 │
│     - BaseOrchestrator (abstract)       │
│     - Domain Orchestrators              │
│     - CrossOrchestrator Communication   │
└─────────────────────────────────────────┘
┌─────────────────────────────────────────┐
│     Agent Management Layer              │
│     - AgentRegistry                     │
│     - Agent Definitions (JSON)          │
└─────────────────────────────────────────┘
┌─────────────────────────────────────────┐
│     Tool Integration Layer              │
│     - MCPRegistry                       │
│     - FigmaIntegration                  │
│     - SDK Tools (Read, Write, etc.)     │
└─────────────────────────────────────────┘
┌─────────────────────────────────────────┐
│     MCP Server Layer                    │
│     - LilaMCPServer (Neo4j)             │
│     - SimpleLilaMCPServer (Mock)        │
└─────────────────────────────────────────┘
┌─────────────────────────────────────────┐
│     Data Layer                          │
│     - Neo4j Database                    │
│     - Import/Export Tools               │
└─────────────────────────────────────────┘
```

### Key Design Patterns

1. **Abstract Base Class Pattern**: `BaseOrchestrator` defines common workflow, subclasses implement domain logic
2. **Registry Pattern**: Centralized discovery and management (`AgentRegistry`, `MCPRegistry`)
3. **Template Method Pattern**: Orchestrators follow predefined execution flow with customizable phases
4. **Facade Pattern**: `SimpleLilaMCPServer` provides same interface as `LilaMCPServer` with mock data
5. **Mixin Pattern**: `CrossOrchestratorCommunication` adds optional cross-domain capabilities
6. **Strategy Pattern**: Multiple orchestrators implement different domain strategies with same base interface
7. **Dependency Injection**: Clients and options injected rather than constructed internally

### Design Principles

- **Modularity**: Each layer has specific responsibilities with minimal coupling
- **Extensibility**: New orchestrators extend `BaseOrchestrator`; new agents added via JSON
- **Testability**: Mock implementations (`SimpleLilaMCPServer`) support testing without dependencies
- **Graceful Degradation**: Fallback options when tools unavailable
- **Observable Workflows**: Real-time progress display and cost tracking
- **Single Responsibility**: Each class has focused, well-defined purpose
- **Open/Closed**: System open for extension, closed for modification

---

## Component Overview

### MCP Servers

#### 1. **LilaMCPServer** ([Source](../lila_mcp_server.py))
Production MCP server with comprehensive Neo4j integration:
- **Resources**: Personas, relationships, interactions (Neo4j-backed)
- **Tools**: Update metrics, record interactions, analyze compatibility
- **Prompts**: Attachment style assessment, emotional climate analysis
- **Health Check**: HTTP endpoint for container orchestration
- **Use Case**: Production deployment with graph database

#### 2. **SimpleLilaMCPServer** ([Source](../simple_lila_mcp_server.py))
Development/testing server with mock data fallback:
- **Resources**: Same interface as LilaMCPServer + additional mock resources
- **Tools**: Full psychological analysis toolkit with in-memory state
- **Prompts**: Attachment theory frameworks for LLM consumption
- **Use Case**: Development, testing, demos without database

### Orchestrators

#### 1. **BaseOrchestrator** ([Source](../orchestrators/base_orchestrator.py))
Abstract base providing orchestrator framework:
- Phase execution and management
- Agent lifecycle coordination
- Progress tracking with real-time display
- Cost tracking and reporting
- Output verification and checkpointing
- Error handling and recovery

**Key Methods**:
- `execute_phase()` - Run single workflow phase
- `run_with_client()` - Main execution with automatic setup/teardown
- `verify_outputs()` - Validate phase results
- `display_summary()` - Show cost and completion status

#### 2. **ArchitectureOrchestrator** ([Source](../orchestrators/architecture_orchestrator.py))
Comprehensive repository analysis workflow:
- **Phase 1**: Component inventory (all classes, methods, entry points)
- **Phase 2**: Architecture diagrams (system, class, dependency views)
- **Phase 3**: Data flow analysis (sequence diagrams, interaction patterns)
- **Phase 4**: API documentation (complete reference with examples)
- **Phase 5**: Synthesis (integrated README)
- **Agents**: Analyzer (code analysis), Doc-Writer (documentation)
- **Output**: `repo_analysis/` directory structure

#### 3. **UXOrchestrator** ([Source](../orchestrators/ux_orchestrator.py))
End-to-end UX/UI design workflow:
- **Phase 1**: UX research (personas, journeys, competitive analysis)
- **Phase 2**: Information architecture (sitemaps, wireframes)
- **Phase 3**: Visual design (mockups, design system)
- **Phase 4**: Interactive prototyping (flows, animations)
- **Phase 5**: API contract design (data models, endpoints)
- **Phase 6**: Design system documentation (component library)
- **Agents**: UX Researcher, IA Architect, UI Designer, Prototype Developer
- **Output**: `outputs/ux_design/` directory structure

### Tool Integration

#### **MCPRegistry** ([Source](../tools/mcp_registry.py))
Manages MCP server discovery and availability:
- Auto-discovers: Figma, V0, Sequential-Thinking, Playwright servers
- Validates tool availability across servers
- Provides fallback options when tools unavailable
- Returns configuration requirements and setup instructions
- **Use Case**: Check tool availability before orchestrator execution

#### **FigmaIntegration** ([Source](../tools/figma_integration.py))
Wrapper for Figma MCP and REST API:
- Get design context from Figma files
- Export components to code (React, Vue, etc.)
- Create components from specifications
- Provide setup instructions when unavailable
- **Use Case**: Bridge between design tools and orchestrators

### Data Management

#### **Neo4jDataImporter** ([Source](../import_data.py))
Import psychological intelligence data:
- Loads schema constraints and indexes
- Imports persona and relationship data
- Maps behavioral styles to Big Five traits
- Retry logic for container startup
- Verification and default persona creation
- **CLI**: `python import_data.py --schema graphs/lila-graph-schema-v8.json`

#### **Neo4jDataExporter** ([Source](../export_data.py))
Export data for seeding/backup:
- Exports personas, relationships, memories, goals
- Generates Cypher import scripts
- Preserves psychological profiles and metrics
- **CLI**: `python export_data.py --output seed_data.cypher`

### Entry Points

**MCP Servers**:
```bash
# Full server with Neo4j
python lila_mcp_server.py

# Simple server with mock data
fastmcp dev simple_lila_mcp_server.py
```

**Orchestrators**:
```bash
# Architecture analysis
python -m orchestrators.architecture_orchestrator

# UX design workflow
python -m orchestrators.ux_orchestrator "My Project"
```

**Data Management**:
```bash
# Import data
python import_data.py --schema graphs/lila-graph-schema-v8.json --create-defaults

# Export data
python export_data.py --output seed_data.cypher
```

**Testing**:
```bash
# Validate all components
python test_orchestrators.py
```

---

## Data Flows

### Key Flow Patterns

#### 1. **Orchestrator Execution Flow**
```
User → Orchestrator.run_with_client()
  → Create ClaudeAgentOptions (agents, tools, permission mode)
  → Open ClaudeSDKClient context
  → For each phase:
      → execute_phase(phase_name, agent_name, prompt)
      → Agent processes with tools (Read, Write, Grep, etc.)
      → Track cost, mark complete
  → Verify outputs
  → Display summary
```

**Key Characteristics**:
- Single client session across all phases (context maintained)
- Streaming message display (AssistantMessage → UserMessage → ResultMessage)
- Real-time cost tracking per phase
- Output verification before completion

#### 2. **MCP Resource Request Flow**
```
Client → MCP Server (HTTP/SSE)
  → FastMCP routes to resource handler
  → Resource handler queries Neo4j
  → Transform to JSON
  → Return to client
```

**Resource Types**:
- **Static**: Personas, relationships, interactions (direct Neo4j queries)
- **Dynamic**: Emotional climate, psychological trends (computed from data)

#### 3. **Tool Execution Flow**
```
Agent decides to use tool → ToolUseBlock
  → Check permission mode
  → If "acceptEdits": Auto-approve Read/Write/Grep/Glob
  → If "ask" or destructive: Request user approval
  → Execute tool → ToolResultBlock
  → Return to agent
```

**Permission Modes**:
- `acceptEdits` (default): Auto-approve safe operations, ask for destructive
- `ask`: Require approval for every tool use

#### 4. **Cross-Orchestrator Communication**
```
UXOrchestrator needs validation
  → invoke_orchestrator("architecture", "validate_design", context)
  → Architecture agent processes with context
  → Return validation results
  → UX continues with validated design
```

See [Data Flows Documentation](docs/03_data_flows.md) for detailed sequence diagrams.

---

## API Highlights

### Starting an MCP Server

```python
import asyncio
from lila_mcp_server import LilaMCPServer

async def main():
    server = LilaMCPServer()
    try:
        await server.run_server(host="0.0.0.0", port=8765)
    finally:
        server.close()

asyncio.run(main())
```

### Running an Orchestrator

```python
import asyncio
from orchestrators.architecture_orchestrator import ArchitectureOrchestrator

async def analyze():
    orchestrator = ArchitectureOrchestrator(
        output_base_dir=Path("repo_analysis"),
        show_tool_details=True
    )
    success = await orchestrator.run_with_client()
    return success

asyncio.run(analyze())
```

### Integrating Tools

```python
from tools.mcp_registry import MCPRegistry

registry = MCPRegistry()

if registry.is_server_available("figma"):
    tools = registry.get_server_tools("figma")
    print(f"Figma tools: {tools}")
else:
    fallbacks = registry.get_fallback_options("figma_get_file")
    config = registry.get_configuration_requirements("figma")
    print(f"Setup: {config['setup_instructions']}")
```

### Importing/Exporting Data

```python
from import_data import Neo4jDataImporter
from pathlib import Path

# Import
importer = Neo4jDataImporter(
    uri="bolt://localhost:7687",
    user="neo4j",
    password="passw0rd"
)
importer.load_schema(Path("graphs/lila-graph-schema-v8.json"))
importer.verify_import()
importer.close()

# Export
from export_data import Neo4jDataExporter

exporter = Neo4jDataExporter(uri="bolt://localhost:7687", user="neo4j", password="passw0rd")
personas = exporter.export_personas()
relationships = exporter.export_relationships()
script = exporter.generate_cypher_script(personas, relationships, [], [])
Path("seed_data.cypher").write_text(script)
exporter.close()
```

See [API Reference](docs/04_api_reference.md) for complete documentation with 52+ methods and 25+ examples.

---

## Configuration

### Environment Variables

**Neo4j Connection** (required for production MCP server):
```bash
export NEO4J_URI="bolt://localhost:7687"
export NEO4J_USER="neo4j"
export NEO4J_PASSWORD="passw0rd"
```

**Figma Integration** (optional):
```bash
export FIGMA_ACCESS_TOKEN="figd_xxx"
export FIGMA_FILE_ID="abc123def456"
```

**Vercel V0** (optional):
```bash
export V0_API_KEY="v0_xxx"
```

### Configuration Files

**.env File** (place in project root):
```bash
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=passw0rd
FIGMA_ACCESS_TOKEN=figd_xxx
```

**MCP Server Configuration** (for Claude Code):
```json
{
  "mcpServers": {
    "lila-psychological-relationships": {
      "command": "python",
      "args": ["-m", "simple_lila_mcp_server"],
      "env": {
        "NEO4J_URI": "bolt://localhost:7687",
        "NEO4J_USER": "neo4j",
        "NEO4J_PASSWORD": "passw0rd"
      }
    }
  }
}
```

---

## Key Design Decisions

### Why Dual MCP Servers?

**LilaMCPServer**: Production deployment with Neo4j
- Full graph database capabilities
- Complex relationship queries
- Persistent psychological state
- Health check for container orchestration

**SimpleLilaMCPServer**: Development and testing
- No database dependencies
- Instant startup with mock data
- Same interface for drop-in replacement
- Ideal for CI/CD and demos

**Rationale**: Enables development without infrastructure while maintaining production-ready interface.

### Why Phase-Based Orchestration?

**Sequential Phases** with agent switching:
- Each phase has specific deliverables
- Later phases build on earlier outputs
- Different agents specialized for different tasks
- Clear progress tracking and cost attribution

**Single Client Session**:
- Maintains context across phases
- Agents can reference previous outputs
- Reduced overhead vs. multiple sessions

**Rationale**: Complex workflows broken into manageable units with clear dependencies and measurable progress.

### Why Registry Pattern for Tools?

**AgentRegistry**:
- Centralizes agent discovery from JSON files
- Caching prevents redundant file I/O
- Domain-based organization
- Easy to add new agents without code changes

**MCPRegistry**:
- Auto-discovers available MCP servers
- Validates tool availability before execution
- Provides fallback options and setup guidance
- Decouples orchestrators from tool availability

**Rationale**: Dynamic discovery enables extensibility and graceful degradation without hardcoded dependencies.

### Graceful Degradation Strategy

**Tool Availability Checks**:
1. Query MCPRegistry for server availability
2. If unavailable, get configuration requirements
3. If still unavailable, get fallback options
4. Proceed with manual alternatives

**Example Flow**:
```python
if not registry.is_server_available("figma"):
    config = registry.get_configuration_requirements("figma")
    # Show setup instructions
    fallbacks = registry.get_fallback_options("figma_get_file")
    # Use markdown specifications instead
```

**Rationale**: System remains functional even when optional tools unavailable; users get clear guidance on enabling features.

---

## Getting Started

### Prerequisites

- Python 3.9+
- Neo4j 5.x (for production MCP server)
- Claude API key (for orchestrators)
- Optional: Figma access token, V0 API key

### Installation Steps

1. **Clone Repository**:
   ```bash
   git clone <repository-url>
   cd lila-mcp
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment** (create `.env`):
   ```bash
   NEO4J_URI=bolt://localhost:7687
   NEO4J_USER=neo4j
   NEO4J_PASSWORD=passw0rd
   ```

4. **Start Neo4j** (optional, for production server):
   ```bash
   docker run -d -p 7687:7687 -p 7474:7474 \
     -e NEO4J_AUTH=neo4j/passw0rd \
     neo4j:5-community
   ```

5. **Import Data** (optional):
   ```bash
   python import_data.py --schema graphs/lila-graph-schema-v8.json --create-defaults
   ```

### Running Your First Query

**Start Simple MCP Server**:
```bash
fastmcp dev simple_lila_mcp_server.py
```

**Connect from Claude Code**: Add to MCP settings and query resources like `neo4j://personas/all`

### Running Your First Orchestration

**Architecture Analysis**:
```bash
python -m orchestrators.architecture_orchestrator
```

**Results**: Check `repo_analysis/` directory for:
- Component inventory
- Architecture diagrams
- Data flow analysis
- API documentation
- Synthesis README

### Common Use Cases

**1. Analyze a Repository**:
```bash
python -m orchestrators.architecture_orchestrator
```

**2. Design a UX Workflow**:
```bash
python -m orchestrators.ux_orchestrator "My Dashboard Project"
```

**3. Create Custom Orchestrator**:
```python
from orchestrators.base_orchestrator import BaseOrchestrator

class MyOrchestrator(BaseOrchestrator):
    def __init__(self):
        super().__init__(domain_name="my_domain")

    def get_agent_definitions(self):
        return {"my-agent": AgentDefinition(...)}

    def get_allowed_tools(self):
        return ["Read", "Write"]

    async def run(self):
        await self.execute_phase("Phase 1", "my-agent", "prompt", self.client)
```

**4. Access Psychological Data**:
```python
from simple_lila_mcp_server import SimpleLilaMCPServer

server = SimpleLilaMCPServer()
# Query personas, relationships via MCP protocol
```

---

## References

### Detailed Documentation

- **[Component Inventory](docs/01_component_inventory.md)** - Complete catalog of 17 Python files, 11+ classes, 52+ methods, 8 entry points
- **[Architecture Diagrams](diagrams/02_architecture_diagrams.md)** - 8 Mermaid diagrams showing system layers, dependencies, class hierarchies
- **[Data Flows](docs/03_data_flows.md)** - 7 sequence diagrams with detailed message routing and permission flows
- **[API Reference](docs/04_api_reference.md)** - Complete API documentation with 25+ code examples

### Source Code Locations

**MCP Servers**:
- [lila_mcp_server.py](../lila_mcp_server.py) - Production server with Neo4j (779 lines)
- [simple_lila_mcp_server.py](../simple_lila_mcp_server.py) - Development server with mock data (830 lines)

**Orchestrators**:
- [orchestrators/base_orchestrator.py](../orchestrators/base_orchestrator.py) - Abstract base class (344 lines)
- [orchestrators/architecture_orchestrator.py](../orchestrators/architecture_orchestrator.py) - Repository analysis (313 lines)
- [orchestrators/ux_orchestrator.py](../orchestrators/ux_orchestrator.py) - UX/UI design workflow (619 lines)

**Tool Integration**:
- [tools/mcp_registry.py](../tools/mcp_registry.py) - MCP server management (153 lines)
- [tools/figma_integration.py](../tools/figma_integration.py) - Figma integration wrapper (157 lines)

**Agent Management**:
- [agents/registry.py](../agents/registry.py) - Agent discovery and loading (100 lines)

**Data Management**:
- [import_data.py](../import_data.py) - Neo4j data importer (465 lines)
- [export_data.py](../export_data.py) - Neo4j data exporter (294 lines)

**Testing**:
- [test_orchestrators.py](../test_orchestrators.py) - Validation tests (209 lines)

### External Dependencies

- **claude_agent_sdk**: Agent orchestration and SDK tools
- **fastmcp**: FastMCP server framework
- **neo4j**: Neo4j Python driver
- **starlette**: ASGI framework (used by FastMCP)
- **dotenv**: Environment variable management

---

## Contributing

### Documentation Maintenance

This documentation is **auto-generated** by the ArchitectureOrchestrator. To update:

1. **Modify Source Code**: Make changes to Python files
2. **Re-run Orchestrator**:
   ```bash
   python -m orchestrators.architecture_orchestrator
   ```
3. **Review Generated Docs**: Check `repo_analysis/` for updates
4. **Commit Changes**: Include both source and documentation

### Adding New Components

**New Orchestrator**:
1. Create class extending `BaseOrchestrator`
2. Implement abstract methods: `get_agent_definitions()`, `get_allowed_tools()`, `run()`
3. Add agent JSON files to `agents/<domain>/`
4. Update tests in `test_orchestrators.py`

**New MCP Tool**:
1. Add server config to `MCPRegistry.discover_mcp_servers()`
2. Include tools list and configuration requirements
3. Add fallback options in `get_fallback_options()`

**New Agent**:
1. Create JSON file in `agents/<domain>/<agent-name>.json`
2. Define: description, prompt, tools, model
3. Registry auto-discovers on next run

### Best Practices

- **Keep Documentation Synchronized**: Re-generate after major changes
- **Add Code Examples**: Update API Reference with practical examples
- **Update Diagrams**: Modify Mermaid diagrams when architecture changes
- **Document Design Decisions**: Add to "Key Design Decisions" section
- **Cross-Reference**: Link between documentation files for deep dives

---

## Summary

### Key Insights Synthesized

1. **Dual-Server Strategy**: Production (Neo4j) and development (mock) servers enable flexible deployment
2. **Phase-Based Orchestration**: Complex workflows decomposed into sequential phases with specialized agents
3. **Registry Pattern**: Centralized discovery enables dynamic tool availability and graceful degradation
4. **Layered Architecture**: 6 distinct layers with clear responsibilities and minimal coupling
5. **Extensibility Focus**: Abstract base classes and JSON-based agent definitions enable rapid extension

### Documentation Cross-References

**Total Cross-References**: 45+
- Component Inventory ↔ Architecture Diagrams: 12 references
- Architecture Diagrams ↔ Data Flows: 8 references
- Data Flows ↔ API Reference: 15 references
- API Reference ↔ Component Inventory: 10 references

### Main Themes Highlighted

1. **Multi-Domain Agent Orchestration**: Framework for coordinating specialized agents across workflows
2. **Psychological Relationship Modeling**: Graph-based data structures for attachment theory and relationship dynamics
3. **Tool Integration & Graceful Degradation**: Registry-based tool management with fallback options
4. **Observable & Measurable Workflows**: Real-time progress, cost tracking, and output verification
5. **Extensibility & Modularity**: Abstract base classes, JSON-driven configuration, plugin architecture

---

**Last Updated**: 2025-10-03
**Documentation Version**: 1.0
**Generated By**: ArchitectureOrchestrator v1.0
