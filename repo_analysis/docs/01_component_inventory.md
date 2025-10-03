# Component Inventory

## Public API

### MCP Server Classes

#### **LilaMCPServer** (`lila_mcp_server.py:29-779`)
FastMCP server exposing psychological relationship data with Neo4j integration.

**Key Methods:**
- `__init__()` (`lila_mcp_server.py:32-44`) - Initialize server with Neo4j connection
- `_setup_database()` (`lila_mcp_server.py:46-62`) - Configure Neo4j database connection
- `close()` (`lila_mcp_server.py:64-67`) - Clean shutdown of Neo4j connection
- `run_server(host, port)` (`lila_mcp_server.py:756-762`) - Run MCP server with SSE transport

**Resources Registered:**
- `neo4j://personas/all` (`lila_mcp_server.py:72-114`) - Retrieve all personas with psychological profiles
- `neo4j://personas/{persona_id}` (`lila_mcp_server.py:116-161`) - Get specific persona by ID
- `neo4j://relationships/all` (`lila_mcp_server.py:163-206`) - Retrieve all relationship data
- `neo4j://relationships/{persona1_id}/{persona2_id}` (`lila_mcp_server.py:208-253`) - Get relationship between two personas
- `neo4j://interactions/recent/{count}` (`lila_mcp_server.py:255-295`) - Get recent interactions

**Tools Registered:**
- `update_relationship_metrics()` (`lila_mcp_server.py:301-360`) - Update trust, intimacy, and strength metrics
- `record_interaction()` (`lila_mcp_server.py:363-399`) - Record interaction between personas
- `analyze_persona_compatibility()` (`lila_mcp_server.py:402-461`) - Assess relationship potential
- `autonomous_strategy_selection()` (`lila_mcp_server.py:464-513`) - AI-driven strategy selection based on attachment theory
- `assess_goal_progress()` (`lila_mcp_server.py:516-552`) - Assess progress toward relationship goals
- `generate_contextual_response()` (`lila_mcp_server.py:555-608`) - Generate psychologically authentic responses

**Prompts Registered:**
- `assess_attachment_style()` (`lila_mcp_server.py:614-643`) - Determine attachment style from behavioral observations
- `analyze_emotional_climate()` (`lila_mcp_server.py:646-694`) - Evaluate conversation emotional dynamics
- `generate_secure_response()` (`lila_mcp_server.py:697-739`) - Create attachment-security-building responses

**Health Check:**
- `/health` endpoint (`lila_mcp_server.py:746-754`) - HTTP health check for container orchestration

#### **SimpleLilaMCPServer** (`simple_lila_mcp_server.py:33-830`)
Simplified MCP server with mock data fallbacks for testing and demonstration.

**Key Methods:**
- `__init__()` (`simple_lila_mcp_server.py:36-100`) - Initialize with mock data and optional Neo4j
- `_setup_database()` (`simple_lila_mcp_server.py:102-118`) - Initialize Neo4j connection (optional)
- `close()` (`simple_lila_mcp_server.py:120-123`) - Close database connection

**Mock Data:**
- `mock_personas` (`simple_lila_mcp_server.py:42-71`) - Sample persona data (Lila, Don)
- `mock_relationships` (`simple_lila_mcp_server.py:73-80`) - Sample relationship metrics
- `mock_interactions` (`simple_lila_mcp_server.py:82-92`) - Sample interaction records

**Resources Registered:**
- `neo4j://personas/all` (`simple_lila_mcp_server.py:128-170`) - Retrieve all personas
- `neo4j://personas/{persona_id}` (`simple_lila_mcp_server.py:172-217`) - Get persona by ID
- `neo4j://relationships/all` (`simple_lila_mcp_server.py:219-235`) - Get all relationships
- `neo4j://relationships/{persona1_id}/{persona2_id}` (`simple_lila_mcp_server.py:237-256`) - Get specific relationship
- `neo4j://interactions/recent/{count}` (`simple_lila_mcp_server.py:258-268`) - Get recent interactions
- `neo4j://emotional_climate/current` (`simple_lila_mcp_server.py:270-289`) - Current emotional climate assessment
- `neo4j://attachment_styles/analysis` (`simple_lila_mcp_server.py:291-308`) - Attachment compatibility analysis
- `neo4j://goals/active` (`simple_lila_mcp_server.py:310-331`) - Active relationship goals
- `neo4j://psychological_insights/trends` (`simple_lila_mcp_server.py:333-358`) - Psychological trends over time

**Tools Registered:**
- `update_relationship_metrics()` (`simple_lila_mcp_server.py:364-400`) - Update relationship metrics
- `record_interaction()` (`simple_lila_mcp_server.py:402-435`) - Record interaction
- `analyze_persona_compatibility()` (`simple_lila_mcp_server.py:437-475`) - Compatibility analysis
- `autonomous_strategy_selection()` (`simple_lila_mcp_server.py:477-524`) - Strategy selection
- `assess_goal_progress()` (`simple_lila_mcp_server.py:526-567`) - Goal progress assessment
- `generate_contextual_response()` (`simple_lila_mcp_server.py:569-607`) - Generate persona responses
- `commit_relationship_state()` (`simple_lila_mcp_server.py:610-619`) - Commit relationship state
- `finalize_demo_session()` (`simple_lila_mcp_server.py:622-631`) - Finalize demo session

**Prompts Registered:**
- `assess_attachment_style()` (`simple_lila_mcp_server.py:637-697`) - Attachment style assessment
- `analyze_emotional_climate()` (`simple_lila_mcp_server.py:700-755`) - Emotional climate analysis
- `generate_secure_response()` (`simple_lila_mcp_server.py:758-822`) - Secure response generation

### Data Import/Export Utilities

#### **Neo4jDataImporter** (`import_data.py:22-407`)
Imports psychological intelligence data and schema into Neo4j.

**Key Methods:**
- `__init__(uri, user, password, max_retries)` (`import_data.py:25-32`) - Initialize with retry logic
- `_connect_with_retry()` (`import_data.py:34-49`) - Connect to Neo4j with retry mechanism
- `close()` (`import_data.py:51-54`) - Close Neo4j connection
- `clear_database()` (`import_data.py:56-61`) - Clear all existing data
- `load_schema(schema_path)` (`import_data.py:63-120`) - Load schema from JSON file
- `_load_family_graph_data(schema, session)` (`import_data.py:122-237`) - Load personas and relationships
- `_map_behavioral_to_bigfive(behavioral_style)` (`import_data.py:239-280`) - Map DISC to Big Five traits
- `import_seed_data(seed_data_path)` (`import_data.py:282-310`) - Import seed data from Cypher file
- `create_default_personas()` (`import_data.py:312-377`) - Create default personas (Lila and Alex)
- `verify_import()` (`import_data.py:379-406`) - Verify data import success

#### **Neo4jDataExporter** (`export_data.py:21-242`)
Exports psychological intelligence data from Neo4j for MCP standalone seeding.

**Key Methods:**
- `__init__(uri, user, password)` (`export_data.py:24-26`) - Initialize Neo4j connection
- `close()` (`export_data.py:28-30`) - Close Neo4j connection
- `export_personas()` (`export_data.py:32-62`) - Export all PersonaAgent nodes
- `export_relationships()` (`export_data.py:64-89`) - Export all relationships
- `export_memories()` (`export_data.py:91-113`) - Export memory nodes
- `export_goals()` (`export_data.py:115-139`) - Export goal nodes
- `generate_cypher_script(personas, relationships, memories, goals)` (`export_data.py:141-242`) - Generate Cypher import script

### Testing and Validation

#### Test Functions (`test_mcp_validation.py`)

**Async Test Functions:**
- `test_direct_connection()` (`test_mcp_validation.py:15-96`) - Test direct in-memory connection (FastMCP best practice)
- `test_inspector_connection()` (`test_mcp_validation.py:98-132`) - Test Inspector HTTP connection
- `main()` (`test_mcp_validation.py:134-168`) - Run comprehensive validation tests

**Test Coverage:**
- Server connectivity and ping tests (`test_mcp_validation.py:29-32`, `test_mcp_validation.py:111-114`)
- Resource listing and reading (`test_mcp_validation.py:35-50`)
- Tool invocation (`test_mcp_validation.py:59-71`)
- Prompt retrieval (`test_mcp_validation.py:80-93`)
- Inspector connection validation (`test_mcp_validation.py:98-132`)

## Internal Implementation

### Repository Analysis Infrastructure

#### **Architecture Script** (`architecture.py:1-363`)
Production repository analyzer using Claude Agent SDK for incremental analysis.

**Configuration:**
- Output directories (`architecture.py:27-30`): `repo_analysis/`, `docs/`, `diagrams/`, `reports/`
- Agent definitions (`architecture.py:295-330`): `analyzer` and `doc-writer` agents

**Display Utilities:**
- `display_message(msg, show_tools)` (`architecture.py:33-68`) - Display message content with tool usage visibility

**Analysis Phases:**
- `phase_1_component_inventory(client)` (`architecture.py:71-105`) - Generate component inventory
- `phase_2_architecture_diagrams(client)` (`architecture.py:107-146`) - Generate architecture diagrams
- `phase_3_data_flows(client)` (`architecture.py:149-186`) - Document data flows
- `phase_4_api_documentation(client)` (`architecture.py:189-210`) - Generate API documentation
- `phase_5_synthesis(client)` (`architecture.py:213-255`) - Create final synthesis document

**Verification:**
- `verify_outputs()` (`architecture.py:258-279`) - Verify all expected outputs were created

**Main Execution:**
- `main()` (`architecture.py:282-358`) - Run comprehensive repository analysis in phases

### Helper Functions and Utilities

#### Import Data Main Function (`import_data.py:409-466`)
Command-line interface for data import with argument parsing.

**Arguments:**
- `--seed-data` (`import_data.py:412-413`) - Seed data Cypher file path
- `--schema` (`import_data.py:414-415`) - Schema JSON file path
- `--uri` (`import_data.py:416-417`) - Neo4j URI
- `--user` (`import_data.py:418-419`) - Neo4j username
- `--password` (`import_data.py:420-421`) - Neo4j password
- `--create-defaults` (`import_data.py:422-423`) - Create default personas flag

#### Export Data Main Function (`export_data.py:245-295`)
Command-line interface for data export with argument parsing.

**Arguments:**
- `--output` (`export_data.py:248-249`) - Output Cypher file path
- `--uri` (`export_data.py:250-251`) - Neo4j URI
- `--user` (`export_data.py:252-253`) - Neo4j username
- `--password` (`export_data.py:254-255`) - Neo4j password

### Module-Level Initialization

**Server Instances:**
- `_server_instance` (`lila_mcp_server.py:765`) - Module-level LilaMCPServer instance
- `mcp` (`lila_mcp_server.py:766`) - FastMCP app instance for CLI discovery
- `mcp` (`simple_lila_mcp_server.py:825`) - SimpleLilaMCPServer app instance for CLI

**Environment Setup:**
- `load_dotenv()` (`lila_mcp_server.py:15-16`, `simple_lila_mcp_server.py:15-16`) - Load environment variables from .env

**Logging Configuration:**
- Basic logging (`lila_mcp_server.py:27`, `simple_lila_mcp_server.py:28-29`)
- Debug logging for FastMCP (`simple_lila_mcp_server.py:28-29`)

## Entry Points

### Main Server Entry Points

#### 1. **FastMCP Development Server** (`simple_lila_mcp_server.py:824-830`)
```python
mcp = SimpleLilaMCPServer().app
```
- **Usage:** `fastmcp dev simple_lila_mcp_server.py`
- **Purpose:** Run server in development mode with FastMCP Inspector
- **Line Reference:** `simple_lila_mcp_server.py:825`

#### 2. **Production MCP Server** (`lila_mcp_server.py:768-779`)
```python
async def main():
    server = LilaMCPServer()
    await server.run_server()
```
- **Entry Point:** `if __name__ == "__main__": asyncio.run(main())` (`lila_mcp_server.py:778-779`)
- **Purpose:** Run production MCP server with SSE transport
- **Line Reference:** `lila_mcp_server.py:768-779`

#### 3. **FastMCP CLI Discovery** (`lila_mcp_server.py:764-766`)
```python
_server_instance = LilaMCPServer()
mcp = _server_instance.app
```
- **Purpose:** Module-level instance for FastMCP CLI tools
- **Line Reference:** `lila_mcp_server.py:765-766`

### Data Management Entry Points

#### 4. **Import Data Script** (`import_data.py:465-466`)
```python
if __name__ == "__main__":
    main()
```
- **Usage:** `python import_data.py --seed-data seed_data.cypher --schema schema.json`
- **Purpose:** Import psychological intelligence data into Neo4j
- **Line Reference:** `import_data.py:465-466`
- **Main Function:** `import_data.py:409-462`

#### 5. **Export Data Script** (`export_data.py:294-295`)
```python
if __name__ == "__main__":
    main()
```
- **Usage:** `python export_data.py --output seed_data.cypher`
- **Purpose:** Export Neo4j data to Cypher script for seeding
- **Line Reference:** `export_data.py:294-295`
- **Main Function:** `export_data.py:245-291`

### Testing and Analysis Entry Points

#### 6. **MCP Validation Tests** (`test_mcp_validation.py:170-172`)
```python
if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)
```
- **Usage:** `python test_mcp_validation.py`
- **Purpose:** Comprehensive validation of MCP server functionality
- **Line Reference:** `test_mcp_validation.py:170-172`
- **Main Function:** `test_mcp_validation.py:134-168`

#### 7. **Repository Architecture Analyzer** (`architecture.py:361-362`)
```python
if __name__ == "__main__":
    asyncio.run(main())
```
- **Usage:** `python architecture.py`
- **Purpose:** Generate comprehensive repository documentation using Claude Agent SDK
- **Line Reference:** `architecture.py:361-362`
- **Main Function:** `architecture.py:282-358`

### Server Initialization Methods

#### Server Run Methods
- `LilaMCPServer.run_server(host, port)` (`lila_mcp_server.py:756-762`) - Run server with SSE transport
  - Default: `localhost:8765`
  - Transport: SSE (Server-Sent Events)

#### Health Check Endpoints
- `/health` GET endpoint (`lila_mcp_server.py:747-754`) - Container orchestration health check
  - Returns: `{"status": "healthy", "service": "lila-mcp-server", "neo4j_connected": bool}`
  - Status Code: 200

### Database Connection Methods

#### Connection Initialization
- `Neo4jDataImporter._connect_with_retry()` (`import_data.py:34-49`)
  - Max retries: 30
  - Retry delay: 2 seconds
  - Purpose: Handle container startup delays

- `LilaMCPServer._setup_database()` (`lila_mcp_server.py:46-62`)
  - Environment variables: `NEO4J_URI`, `NEO4J_USER`, `NEO4J_PASSWORD`
  - Fallback: Continues without database on connection failure

- `SimpleLilaMCPServer._setup_database()` (`simple_lila_mcp_server.py:102-118`)
  - Environment variables: `NEO4J_URI`, `NEO4J_USER`, `NEO4J_PASSWORD`
  - Graceful degradation to mock data on failure
