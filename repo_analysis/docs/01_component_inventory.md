# Component Inventory

**Repository**: lila-mcp (Lila Psychological Intelligence MCP Server)
**Analysis Date**: 2025-10-03
**Location**: /home/donbr/lila-graph/lila-mcp

## Executive Summary

This repository implements a standalone MCP (Model Context Protocol) server providing psychological intelligence capabilities. The system integrates Neo4j graph database for persona and relationship modeling, implements attachment theory and Big Five personality models, and exposes psychological analysis tools through the FastMCP framework.

**Key Statistics**:
- 6 Python modules (excluding tests)
- 2 main server implementations (full and simplified)
- 8 MCP tools for psychological operations
- 3 MCP prompts for psychological assessment
- 9 MCP resources (2 direct + 7 templated)
- Neo4j database integration with retry logic
- FastMCP framework for MCP protocol implementation

---

## Public API

### 1. MCP Server Modules

#### 1.1 `lila_mcp_server.py` - Full MCP Server Implementation
**Purpose**: Complete production MCP server with Neo4j integration and comprehensive psychological intelligence features.

**Location**: `/home/donbr/lila-graph/lila-mcp/lila_mcp_server.py`

**Key Classes**:

##### `LilaMCPServer` (lines 29-762)
- **Purpose**: Main MCP server class exposing Lila's psychological relationship data and tools
- **Initialization** (lines 32-44): Sets up FastMCP app, Neo4j connection, and registers all MCP endpoints
- **Database Setup** (lines 46-62): Establishes Neo4j connection with error handling

**Public Methods**:
- `close()` (lines 64-67): Close Neo4j database connection
- `run_server(host, port)` (lines 756-762): Start the MCP server with SSE transport

**MCP Resources** (5 resources exposed via Neo4j):
1. `neo4j://personas/all` (lines 72-114): Retrieve all personas with psychological profiles
   - Returns: JSON with personas array, count, and timestamp
   - Includes: persona_id, name, age, role, attachment_style, Big Five traits

2. `neo4j://personas/{persona_id}` (lines 116-161): Get specific persona by ID
   - Parameters: `persona_id` (string)
   - Returns: Full persona profile with description, trust_level, communication_style

3. `neo4j://relationships/all` (lines 163-206): Get all relationships with metrics
   - Returns: Relationships array with trust_level, intimacy_level, relationship_strength
   - Ordered by: relationship_strength DESC

4. `neo4j://relationships/{persona1_id}/{persona2_id}` (lines 208-253): Specific relationship metrics
   - Parameters: `persona1_id`, `persona2_id` (strings)
   - Returns: Bidirectional relationship with timestamps and emotional_valence

5. `neo4j://interactions/recent/{count}` (lines 255-295): Recent interaction history
   - Parameters: `count` (string, max 50)
   - Returns: Recent interactions with emotional_valence and relationship_type

**MCP Tools** (6 tools for psychological operations):

1. `update_relationship_metrics()` (lines 301-360): Update trust, intimacy, and strength
   - **Parameters**:
     - `persona1_id` (str): First persona identifier
     - `persona2_id` (str): Second persona identifier
     - `trust_delta` (float, default 0.0): Trust level change
     - `intimacy_delta` (float, default 0.0): Intimacy level change
     - `strength_delta` (float, default 0.0): Relationship strength change
   - **Returns**: JSON with updated metrics (bounded 0-10) and delta values
   - **Features**: Automatic bounds checking, bidirectional updates, timestamp tracking

2. `record_interaction()` (lines 363-399): Record interaction with emotional analysis
   - **Parameters**:
     - `sender_id` (str): Sender persona ID
     - `recipient_id` (str): Recipient persona ID
     - `content` (str): Interaction content
     - `emotional_valence` (float, default 0.0): Emotional tone (-1 to 1)
     - `relationship_impact` (float, default 0.0): Impact on relationship
   - **Returns**: Interaction ID and recorded metadata
   - **Features**: Generates unique interaction ID, updates last_interaction timestamp, calculates rolling average emotional_valence

3. `analyze_persona_compatibility()` (lines 402-461): Assess relationship potential
   - **Parameters**:
     - `persona1_id` (str): First persona ID
     - `persona2_id` (str): Second persona ID
     - `relationship_type` (str, default "romantic"): Type of relationship
   - **Returns**: Compatibility analysis with level, reasoning, and recommendations
   - **Features**: Uses attachment theory compatibility matrix
   - **Matrix** (lines 424-431):
     - secure + secure: High compatibility
     - secure + anxious: Good (secure provides reassurance)
     - secure + avoidant: Moderate (gradual opening)
     - anxious + anxious: Challenging (emotional intensity)
     - anxious + avoidant: Difficult (pursue-withdraw dynamic)
     - avoidant + avoidant: Low (mutual avoidance)

4. `autonomous_strategy_selection()` (lines 464-513): AI-driven strategy selection
   - **Parameters**:
     - `persona_id` (str): Persona making the decision
     - `conversation_context` (str, default ""): Current conversation context
     - `situation_assessment` (str, default ""): Situation analysis
     - `active_goals` (str, default ""): Current goals
     - `attachment_style` (str, default "secure"): Persona's attachment style
   - **Returns**: Selected strategy with reasoning and available alternatives
   - **Strategy Mapping** (lines 474-479):
     - secure: emotional_bonding, vulnerable_disclosure, supportive_listening, trust_building
     - anxious: reassurance_seeking, emotional_validation, secure_bonding, safety_creation
     - avoidant: autonomous_connection, thoughtful_presence, respectful_distance, gradual_opening
     - exploratory: growth_oriented_support, playful_engagement, curious_exploration, authentic_expression

5. `assess_goal_progress()` (lines 516-552): Assess relationship goal progress
   - **Parameters**:
     - `persona_id` (str): Persona being assessed
     - `goals` (str, default ""): Comma-separated goals
     - `recent_interactions` (str, default ""): Recent interaction summary
   - **Returns**: Progress assessment for each goal with overall progress score
   - **Progress Calculation**: Based on goal keywords (trust, intimacy, vulnerability)

6. `generate_contextual_response()` (lines 555-608): Generate persona-appropriate responses
   - **Parameters**:
     - `persona_id` (str): Persona generating response
     - `context` (str): Situation context
     - `goals` (str, default ""): Response goals
     - `constraints` (str, default ""): Response constraints
   - **Returns**: Psychologically authentic response with strategy and rationale
   - **Response Styles** (lines 582-593):
     - secure: Direct, supportive communication
     - anxious: Reassurance-seeking, validating
     - avoidant: Thoughtful, measured responses

**MCP Prompts** (3 assessment prompts):

1. `assess_attachment_style()` (lines 614-643): Determine attachment style from behavior
   - **Parameters**:
     - `persona_id` (str): Persona being assessed
     - `observation_period` (str, default "recent"): Timeframe for observations
     - `behavioral_examples` (str, default ""): Specific behavioral examples
   - **Returns**: Comprehensive assessment framework prompt
   - **Includes**: Four attachment styles (secure, anxious, avoidant, exploratory), five analysis dimensions, therapeutic implications

2. `analyze_emotional_climate()` (lines 646-694): Evaluate emotional dynamics
   - **Parameters**:
     - `conversation_text` (str, default ""): Conversation content
     - `interaction_id` (str, default ""): Interaction identifier
     - `participants` (str, default ""): Participant names/IDs
   - **Returns**: Emotional climate assessment framework
   - **Assessment Areas**: Safety level (1-10), emotional attunement, communication quality, power dynamics, attachment activation

3. `generate_secure_response()` (lines 697-739): Create security-building responses
   - **Parameters**:
     - `scenario_description` (str): Situation description
     - `personas` (str): Involved personas
     - `insecurity_triggers` (str, default ""): Known triggers
     - `growth_goals` (str, default ""): Relationship goals
   - **Returns**: Response generation framework with secure attachment principles
   - **Principles**: Emotional safety first, attunement, secure base behaviors, repair and growth

**Health Check Endpoint** (lines 741-754):
- **Route**: `/health` (HTTP GET)
- **Purpose**: Container orchestration health monitoring
- **Returns**: JSON with status, service name, and Neo4j connection state
- **Status Code**: 200

**Module-Level Exports** (lines 764-779):
- `_server_instance` (line 765): Global LilaMCPServer instance for CLI discovery
- `mcp` (line 766): FastMCP app reference (FastMCP looks for 'mcp', 'server', or 'app')
- `main()` (lines 768-776): Async entry point with logging setup and server startup

---

#### 1.2 `simple_lila_mcp_server.py` - Simplified MCP Server
**Purpose**: Development-friendly MCP server with mock data for testing without Neo4j dependency.

**Location**: `/home/donbr/lila-graph/lila-mcp/simple_lila_mcp_server.py`

**Key Classes**:

##### `SimpleLilaMCPServer` (lines 33-823)
- **Purpose**: Simplified server with in-memory mock data for development/testing
- **Initialization** (lines 36-100): Creates FastMCP app with mock personas and relationships
- **Debug Logging** (lines 27-29): Enables FastMCP and module debug logging

**Mock Data Structures**:

1. `mock_personas` (lines 42-71): Pre-configured persona dictionary
   - **Lila**: Age 28, Psychological Intelligence Agent, secure attachment
     - Personality: High openness (0.8), agreeableness (0.85), low neuroticism (0.3)
   - **Don**: Age 45, Software Developer, anxious attachment
     - Personality: High conscientiousness (0.8), moderate neuroticism (0.6)

2. `mock_relationships` (lines 73-80): Relationship metrics dictionary
   - Key: Tuple of (persona1_id, persona2_id)
   - Values: trust_level (7.5), intimacy_level (6.8), relationship_strength (7.2)

3. `mock_interactions` (lines 82-92): Interaction history list
   - Sample interaction with ID, content, emotional_valence, timestamp

**Database Setup** (lines 102-118):
- Attempts Neo4j connection but continues without failure
- Falls back to mock data if connection fails

**Additional Resources** (beyond full server):

4. `neo4j://emotional_climate/current` (lines 271-289): Current emotional climate
   - Returns: overall_climate (safety, positivity, authenticity, growth_potential)
   - Includes: risk_factors and strengths arrays

5. `neo4j://attachment_styles/analysis` (lines 291-308): Attachment compatibility
   - Returns: compatibility_matrix with scores and recommendations
   - Example: lila_don pairing with 7.8 overall score

6. `neo4j://goals/active` (lines 310-331): Active relationship goals
   - Returns: Array of goals with progress, strategies, and completion_rate

7. `neo4j://psychological_insights/trends` (lines 333-358): Psychological trends
   - Returns: trust_evolution, intimacy_development, attachment_security trends
   - Includes: predictions for next month and quarter

**Modified Tool Implementations**:

All tools from full server plus:

7. `commit_relationship_state()` (lines 610-619): Mock state persistence
   - **Parameters**: `persona1_id`, `persona2_id`
   - **Returns**: Success confirmation with timestamp
   - **Purpose**: Simulate explicit state commits for CQRS pattern

8. `finalize_demo_session()` (lines 622-631): Session finalization
   - **Parameters**: None
   - **Returns**: Count of committed relationships and timestamp
   - **Purpose**: Batch finalization for demo sessions

**Simplified Tool Logic**:
- Tools use in-memory data structures instead of database queries
- Automatic creation of relationships on first update
- Immediate state updates without transactions

**Module Export** (line 825):
- `mcp = SimpleLilaMCPServer().app`: FastMCP CLI discovery

---

### 2. Data Management Modules

#### 2.1 `import_data.py` - Neo4j Data Import Utility
**Purpose**: Import seed data and schema into Neo4j for MCP server initialization.

**Location**: `/home/donbr/lila-graph/lila-mcp/import_data.py`

**Key Classes**:

##### `Neo4jDataImporter` (lines 22-407)
- **Purpose**: Import psychological intelligence data and schema into Neo4j
- **Initialization** (lines 25-32): Connect with retry logic for container startup delays

**Connection Management**:

1. `_connect_with_retry()` (lines 34-49): Robust connection with retry logic
   - **Max Retries**: 30 attempts
   - **Retry Delay**: 2 seconds between attempts
   - **Purpose**: Handle Neo4j container startup delays
   - **Error Handling**: Raises exception after max attempts

2. `close()` (lines 51-54): Clean database connection closure

**Data Management Methods**:

3. `clear_database()` (lines 56-61): Remove all existing data
   - **Query**: `MATCH (n) DETACH DELETE n`
   - **Purpose**: Clean slate for import

4. `load_schema(schema_path)` (lines 63-121): Load constraints, indexes, and data
   - **Parameters**: `schema_path` (Path) - JSON schema file
   - **Constraints Created** (lines 77-90):
     - PersonaAgent: unique persona_id, unique name
     - Memory: unique memory_id
     - Goal: unique goal_id
   - **Indexes Created** (lines 93-98):
     - PersonaAgent.attachment_style
     - Memory.memory_type
     - Goal.goal_type
     - RELATIONSHIP.relationship_type
   - **Data Loading**: Calls `_load_family_graph_data()` for persona import

5. `_load_family_graph_data(schema, session)` (lines 122-237): Import personas and relationships
   - **Source**: family_graph.nodes and family_graph.edges from JSON schema
   - **Persona Creation** (lines 135-195):
     - Maps behavioral_style to Big Five traits
     - Parses attachment_style (secure, anxious, avoidant)
     - Sets default communication_style based on behavioral traits
     - Creates PersonaAgent nodes with full psychological profiles
   - **Relationship Creation** (lines 197-237):
     - Creates bidirectional RELATIONSHIP edges
     - Maps relationship_type (intimate, friendship)
     - Normalizes union_metric to emotional_valence (0-1 scale)
     - Sets default interaction_count to 0

6. `_map_behavioral_to_bigfive(behavioral_style)` (lines 239-280): DISC to Big Five mapping
   - **Input**: DISC behavioral style string (e.g., "DI", "SC")
   - **Output**: Dictionary with Big Five traits (0-1 scale)
   - **Mapping Logic**:
     - D (Dominance): +extraversion, +openness, -agreeableness
     - I (Influence): +extraversion, +openness, +agreeableness
     - S (Steadiness): +agreeableness, +conscientiousness, -neuroticism
     - C (Conscientiousness): +conscientiousness, +openness, +neuroticism
   - **Normalization**: All values clamped to [0.0, 1.0]

7. `import_seed_data(seed_data_path)` (lines 282-310): Import Cypher statements
   - **Parameters**: `seed_data_path` (Path) - Cypher script file
   - **Processing**: Splits on semicolons, skips comments
   - **Progress**: Reports every 10 statements
   - **Error Handling**: Logs individual statement failures but continues

8. `create_default_personas()` (lines 312-377): Create fallback personas
   - **Personas Created**:
     - **Lila** (lines 317-331): AI Research Assistant, age 28, secure attachment
       - High openness (0.85), agreeableness (0.90), low neuroticism (0.25)
       - Communication style: empathetic
     - **Alex** (lines 332-346): Software Engineer, age 32, secure attachment
       - High conscientiousness (0.85), moderate extraversion (0.60)
       - Communication style: analytical
   - **Relationship** (lines 364-375): Friendship with moderate metrics
     - trust_level: 0.70, intimacy_level: 0.60, relationship_strength: 0.65
     - interaction_count: 5, relationship_type: friendship, emotional_valence: 0.75

9. `verify_import()` (lines 379-406): Verify successful import
   - **Counts**:
     - PersonaAgent nodes
     - RELATIONSHIP edges
     - Memory nodes
     - Goal nodes
   - **Returns**: Boolean indicating personas exist
   - **Output**: Formatted verification report

**CLI Interface** (lines 409-466):

```bash
python import_data.py \
  --seed-data seed_data.cypher \
  --schema graphs/lila-graph-schema-v8.json \
  --uri bolt://localhost:7687 \
  --user neo4j \
  --password passw0rd \
  --create-defaults
```

**Arguments**:
- `--seed-data` (line 412): Cypher file path (default: seed_data.cypher)
- `--schema` (line 414): JSON schema path (default: graphs/lila-graph-schema-v8.json)
- `--uri` (line 416): Neo4j connection URI (default: bolt://localhost:7687)
- `--user` (line 418): Database username (default: neo4j)
- `--password` (line 420): Database password (supports NEO4J_PASSWORD env var)
- `--create-defaults` (line 422): Create default personas if no seed data

**Main Function** (lines 409-463):
1. Parse arguments
2. Initialize importer with retry logic
3. Load schema (constraints, indexes, personas)
4. Import seed data or create defaults
5. Verify import success
6. Report results with emoji indicators

---

#### 2.2 `export_data.py` - Neo4j Data Export Utility
**Purpose**: Export persona and relationship data from Neo4j for backup/migration.

**Location**: `/home/donbr/lila-graph/lila-mcp/export_data.py`

**Key Classes**:

##### `Neo4jDataExporter` (lines 21-243)
- **Purpose**: Export psychological intelligence data to Cypher format

**Connection Management**:
- `__init__(uri, user, password)` (lines 24-26): Initialize Neo4j driver
- `close()` (lines 28-30): Close connection

**Export Methods**:

1. `export_personas()` (lines 32-62): Export all PersonaAgent nodes
   - **Query**: Returns all persona properties including psychological profiles
   - **Fields**: persona_id, name, age, role, description, attachment_style
   - **Traits**: Big Five (openness, conscientiousness, extraversion, agreeableness, neuroticism)
   - **Additional**: trust_level, relationship_history, communication_style, timestamps
   - **Returns**: List of persona dictionaries

2. `export_relationships()` (lines 64-89): Export relationship edges
   - **Query**: Returns all RELATIONSHIP properties between PersonaAgent nodes
   - **Fields**: persona1_id, persona2_id, trust_level, intimacy_level, relationship_strength
   - **Metrics**: interaction_count, last_interaction, relationship_type, emotional_valence
   - **Timestamps**: created_at, updated_at
   - **Returns**: List of relationship dictionaries

3. `export_memories()` (lines 91-113): Export memory nodes
   - **Query**: Returns memories with HAS_MEMORY relationships
   - **Fields**: persona_id, memory_id, content, memory_type
   - **Metrics**: importance_score, emotional_valence, participants
   - **Timestamp**: created_at
   - **Returns**: List of memory dictionaries

4. `export_goals()` (lines 115-139): Export goal nodes
   - **Query**: Returns goals with HAS_GOAL relationships
   - **Fields**: persona_id, goal_id, goal_type, description
   - **Progress**: progress score, target_persona, priority, status
   - **Timestamps**: created_at, updated_at
   - **Returns**: List of goal dictionaries

5. `generate_cypher_script(personas, relationships, memories, goals)` (lines 141-242): Generate import script
   - **Purpose**: Create self-contained Cypher file for data import
   - **Header** (lines 145-152): Comment block with clear command and section headers
   - **Persona Generation** (lines 155-170):
     - Converts persona dictionaries to CREATE statements
     - Handles None values and type conversions
     - Escapes quotes and newlines in strings
     - Generates property lists for node creation
   - **Relationship Generation** (lines 172-194):
     - Creates MATCH-CREATE pattern for relationships
     - Finds both personas by persona_id
     - Builds relationship property map
     - Handles bidirectional relationships
   - **Memory Generation** (lines 196-217):
     - Creates HAS_MEMORY relationships
     - Links memories to personas
     - Includes all memory properties
   - **Goal Generation** (lines 219-240):
     - Creates HAS_GOAL relationships
     - Links goals to personas
     - Includes progress and status tracking
   - **Returns**: Complete Cypher script as string

**CLI Interface** (lines 245-295):

```bash
python export_data.py \
  --output seed_data.cypher \
  --uri bolt://localhost:7687 \
  --user neo4j \
  --password passw0rd
```

**Arguments**:
- `--output` (line 248): Output file path (default: seed_data.cypher)
- `--uri` (line 250): Neo4j URI (default: bolt://localhost:7687)
- `--user` (line 252): Username (default: neo4j)
- `--password` (line 254): Password (supports NEO4J_PASSWORD env var)

**Main Function** (lines 245-291):
1. Parse command-line arguments
2. Connect to Neo4j
3. Export all data types (personas, relationships, memories, goals)
4. Generate Cypher import script
5. Write to output file
6. Report statistics with emoji indicators
7. Handle errors with exit codes

---

### 3. Testing and Validation

#### 3.1 `test_mcp_validation.py` - MCP Server Validation Suite
**Purpose**: Comprehensive validation for MCP server connectivity and functionality.

**Location**: `/home/donbr/lila-graph/lila-mcp/test_mcp_validation.py`

**Module Configuration** (lines 12-13):
- Logging level: INFO for debugging
- Import: FastMCP Client and SimpleLilaMCPServer

**Key Functions**:

1. `test_direct_connection()` (lines 15-96): Test in-memory connection
   - **Purpose**: Validate FastMCP best practice (direct in-memory connection)
   - **Setup** (lines 22-26):
     - Creates SimpleLilaMCPServer instance
     - Uses FastMCP Client with direct server reference
     - Async context manager for connection lifecycle
   - **Tests Performed**:
     - Connection validation (line 27): `client.is_connected()`
     - Server ping test (lines 30-32): `await client.ping()`
     - Resource listing (lines 35-40): `await client.list_resources()`
     - Resource reading (lines 42-50): `await client.read_resource(uri)`
     - Tool listing (lines 53-58): `await client.list_tools()`
     - Tool invocation (lines 60-71): `await client.call_tool()` with analyze_persona_compatibility
     - Prompt listing (lines 74-78): `await client.list_prompts()`
     - Prompt retrieval (lines 80-93): `await client.get_prompt()` with parameters
   - **Returns**: Tuple of (success: bool, resources_count: int, tools_count: int, prompts_count: int)
   - **Test Data** (lines 63-67):
     - persona1_id: "lila"
     - persona2_id: "don"
     - relationship_type: "romantic"

2. `test_inspector_connection()` (lines 98-132): Test HTTP Inspector connection
   - **Purpose**: Validate Inspector integration (requires running server)
   - **Connection** (line 105): `Client("http://localhost:6274/")`
   - **Tests Performed**:
     - Connection check (line 109)
     - Server ping (lines 112-114)
     - Component listing (lines 117-119): resources, tools, prompts
     - Count reporting (lines 121-123)
   - **Error Handling** (lines 128-131):
     - Catches connection failures
     - Provides helpful startup instructions
     - Returns False if Inspector not running
   - **Returns**: Boolean success indicator

3. `main()` (lines 134-168): Run comprehensive validation
   - **Execution Flow**:
     - Prints banner (lines 137-138)
     - Runs direct connection test (line 141)
     - Runs Inspector connection test (line 144)
     - Generates summary report (lines 147-166)
   - **Summary Report** (lines 148-153):
     - Direct connection result
     - Inspector connection result
     - Resources count
     - Tools count
     - Prompts count
   - **Success Messages** (lines 155-158):
     - Confirms server functionality
     - Validates self-contained operation
   - **Inspector Status** (lines 159-166):
     - Shows Inspector URL with auth token if running
     - Provides startup instructions if not running
   - **Returns**: Boolean indicating direct test success

**Usage Pattern**:
```python
# Run validation
success = asyncio.run(main())
exit(0 if success else 1)
```

**Entry Point** (lines 170-172):
```python
if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)
```

---

#### 3.2 `architecture.py` - Architecture Analysis Tool
**Purpose**: Repository analyzer using Claude Agent SDK for documentation generation.

**Location**: `/home/donbr/lila-graph/lila-mcp/architecture.py`

**Module Configuration** (lines 26-30):
- Output directories defined with Path objects
- OUTPUT_DIR: "repo_analysis"
- DOCS_DIR: "repo_analysis/docs"
- DIAGRAMS_DIR: "repo_analysis/diagrams"
- REPORTS_DIR: "repo_analysis/reports"

**Display Utilities**:

1. `display_message(msg, show_tools=True)` (lines 33-68): Display agent messages with tool visibility
   - **Purpose**: Show full visibility into tool usage during analysis
   - **Message Types**:
     - AssistantMessage (lines 36-54): Shows text blocks and tool uses
     - UserMessage (lines 56-61): Shows tool results
     - ResultMessage (lines 63-68): Shows phase completion and costs
   - **Tool Display** (lines 39-54):
     - Read operations: Shows file_path being read
     - Grep operations: Shows search pattern
     - Write operations: Shows file_path being written
     - Bash operations: Shows command being executed
   - **Result Display** (lines 59-61): Shows first 200 characters of tool results

**Analysis Phases**:

2. `phase_1_component_inventory(client)` (lines 71-105): Generate component inventory
   - **Query Content** (lines 77-100):
     - Analyze all Python modules and purposes
     - Document key classes and functions
     - Distinguish public API vs internal implementation
     - Identify entry points and main interfaces
   - **Output**: `{DOCS_DIR}/01_component_inventory.md`
   - **Structure**: Public API, Internal Implementation, Entry Points sections

3. `phase_2_architecture_diagrams(client)` (lines 107-146): Generate architecture diagrams
   - **Query Content** (lines 113-142):
     - System architecture (layered view)
     - Component relationships
     - Class hierarchies
     - Module dependencies
   - **Output**: `{DIAGRAMS_DIR}/02_architecture_diagrams.md`
   - **Format**: Mermaid diagrams with explanations

4. `phase_3_data_flows(client)` (lines 149-186): Document data flows
   - **Query Content** (lines 156-182):
     - Simple query flow
     - Interactive client session flow
     - Tool permission callback flow
     - MCP server communication flow
     - Message parsing and routing
   - **Output**: `{DOCS_DIR}/03_data_flows.md`
   - **Format**: Sequence diagrams with explanations

5. `phase_4_api_documentation(client)` (lines 189-211): Generate API documentation
   - **Query Content** (lines 196-206):
     - All public functions and classes
     - Parameters, return types, and examples
     - Usage patterns and best practices
     - Configuration options
   - **Output**: `{DOCS_DIR}/04_api_reference.md`
   - **Format**: Clear examples with source file links

6. `phase_5_synthesis(client)` (lines 213-256): Create final synthesis document
   - **Query Content** (lines 219-251):
     - Reviews all previously generated documents
     - Creates high-level summary
     - Provides quick start guide
     - Summarizes architecture and components
     - Highlights key flow patterns
   - **Output**: `{OUTPUT_DIR}/README.md`
   - **Structure**: Overview, Quick Start, Architecture Summary, Component Overview, Data Flows, References

**Verification**:

7. `verify_outputs()` (lines 258-280): Verify all expected outputs were created
   - **Expected Files** (lines 264-270):
     - 01_component_inventory.md
     - 02_architecture_diagrams.md
     - 03_data_flows.md
     - 04_api_reference.md
     - README.md
   - **Output**: File existence checks with file sizes

**Main Execution**:

8. `main()` (lines 282-362): Run comprehensive repository analysis in phases
   - **Banner** (lines 284-293): Displays analysis configuration
   - **Agent Definitions** (lines 295-330):
     - **analyzer_agent**: Code structure and architecture analysis
       - Model: "sonnet"
       - Tools: Read, Grep, Glob, Write, Bash
       - Prompt: Emphasizes writing actual files, not just descriptions
     - **doc_writer_agent**: Technical documentation creation
       - Model: "sonnet"
       - Tools: Read, Write, Grep, Glob
       - Prompt: Focuses on clarity and developer experience
   - **Options Configuration** (lines 332-337):
     - Agents: analyzer and doc-writer
     - Allowed tools: Read, Write, Grep, Glob, Bash
     - Permission mode: "acceptEdits" (auto-approve writes)
     - Working directory: "." (current directory)
   - **Execution** (lines 340-349):
     - Runs all 5 phases sequentially
     - Each phase uses async/await
     - Messages displayed during execution
   - **Verification and Summary** (lines 349-357):
     - Verifies output files
     - Reports completion location
     - Handles errors with partial results message

**Entry Point** (lines 361-362):
```python
if __name__ == "__main__":
    asyncio.run(main())
```

---

## Internal Implementation

### 4. Configuration Files

#### 4.1 `pyproject.toml` - Project Configuration
**Location**: `/home/donbr/lila-graph/lila-mcp/pyproject.toml`

**Project Metadata** (lines 1-32):
- **Name**: `lila-mcp-standalone`
- **Version**: `1.0.0`
- **Description**: Standalone Lila MCP Server - Minimal psychological relationship intelligence
- **Authors**: Lila Team <team@lila.dev>
- **Python Requirement**: `>=3.12`

**Core Dependencies** (lines 10-32):

**MCP Framework**:
- `fastmcp>=2.12.3` (line 12): FastMCP server framework

**Database**:
- `neo4j>=5.15.0` (line 14): Neo4j graph database driver

**LLM Integration**:
- `openai>=1.30.0` (line 16): OpenAI API client
- `anthropic>=0.25.0` (line 17): Anthropic API client

**Data Validation**:
- `pydantic>=2.6.0` (line 19): Data validation with type hints
- `pydantic-settings>=2.2.0` (line 20): Settings management

**HTTP Clients**:
- `httpx>=0.27.0` (line 21): Modern async HTTP client
- `aiohttp>=3.9.0` (line 22): Async HTTP client/server

**Observability**:
- `logfire>=0.28.0` (line 24): Telemetry and monitoring

**Configuration**:
- `python-dotenv>=1.0.0` (line 26): .env file loading

**CLI**:
- `click>=8.1.0` (line 28): Command-line interface creation

**Async Utilities**:
- `asyncio-mqtt>=0.16.0` (line 30): MQTT async support

**Agent Framework**:
- `claude-agent-sdk>=0.1.0` (line 31): Claude Agent SDK

**Optional Development Dependencies** (lines 34-40):
- `pytest>=8.0.0` (line 36): Testing framework
- `pytest-asyncio>=0.23.0` (line 37): Async test support
- `black>=24.0.0` (line 38): Code formatter
- `ruff>=0.3.0` (line 39): Fast Python linter

**Build System** (lines 42-44):
- Requires: `hatchling`
- Backend: `hatchling.build`

**Tool Configuration**:

**Black Formatter** (lines 46-48):
- Line length: 120 characters
- Target version: Python 3.12

**Ruff Linter** (lines 50-52):
- Line length: 120 characters
- Target version: Python 3.12

**Pytest** (lines 54-59):
- Asyncio mode: auto
- Test paths: ["tests"]
- File pattern: test_*.py
- Class pattern: Test*
- Function pattern: test_*

**Hatch Build Configuration** (lines 61-76):
- Allow direct references: true
- Wheel targets include (lines 64-72):
  - All `*.py` files in root
  - `agents/**/*.py` subdirectory
  - `llm/**/*.py` subdirectory
  - `graph/**/*.py` subdirectory
  - `.env` file
- Source mapping (lines 74-76):
  - Current directory "." maps to "lila_mcp_standalone" package

---

#### 4.2 `fastmcp.json` - FastMCP Server Configuration
**Location**: `/home/donbr/lila-graph/lila-mcp/fastmcp.json`

**Schema** (line 2):
- Reference: `https://gofastmcp.com/public/schemas/fastmcp.json/v1.json`

**Source Configuration** (lines 4-8):
- **Type**: `filesystem` (line 5)
- **Path**: `lila_mcp_server.py` (line 6)
- **Entrypoint**: `mcp` (line 7)
  - References module-level `mcp` variable at line 766 of lila_mcp_server.py

**Environment Configuration** (lines 10-14):
- **Type**: `uv` (line 11) - Uses UV package manager
- **Python**: `3.12` (line 12) - Python version requirement
- **Project**: `.` (line 13) - Current directory
  - Note: Using "." instead of version specifier to avoid MCP Inspector bugs

**Purpose**:
- Auto-configuration for `fastmcp dev` command (development with Inspector)
- Auto-configuration for `fastmcp run` command (production HTTP server)
- Auto-configuration for `fastmcp inspect` command (capability inspection)

---

#### 4.3 `.env.example` - Environment Template
**Location**: `/home/donbr/lila-graph/lila-mcp/.env.example`

**Configuration Categories**:

**1. UV Environment Management** (lines 12-21):
- Purpose: Address VIRTUAL_ENV mismatch warnings
- Variables:
  - `UV_PROJECT_ENVIRONMENT`: Override project environment path (optional)
  - `UV_PYTHON`: Specify Python version for uv (optional)

**2. Neo4j Database Configuration** (lines 24-34):
- `NEO4J_URI`: Connection string (placeholder: `<fill>`)
- `NEO4J_USER`: Database username
- `NEO4J_PASSWORD`: Database password
- `DISABLE_NEO4J`: Disable database connection flag
- `NEO4J_TIMEOUT`: Connection timeout setting
- `NEO4J_MAX_RETRY_TIME`: Maximum retry duration

**3. LLM Configuration** (lines 37-43):
- `DEFAULT_LLM_MODEL`: Model selection
- `LLM_TEMPERATURE`: Temperature parameter
- `OPENAI_API_KEY`: OpenAI API key (commented)
- `ANTHROPIC_API_KEY`: Anthropic API key (commented)

**4. FastMCP and Telemetry Configuration** (lines 46-56):
- `ENABLE_LOGFIRE_TELEMETRY`: Enable observability
- `LOGFIRE_PROJECT_NAME`: Project name for telemetry
- `LOGFIRE_TOKEN`: Authentication token (optional, commented)
- `FASTMCP_AUTO_RELOAD`: Development auto-reload
- `FASTMCP_LOG_LEVEL`: Logging verbosity

**5. Environment and Logging Configuration** (lines 59-69):
- `ENV`: Environment name
- `LOG_LEVEL`: Logging level
- `LOG_FORMAT`: Log message format
- `LOG_FILE_ENABLED`: File logging flag (optional)
- `LOG_FILE_PATH`: Log file location (optional)
- `LOG_ROTATION_SIZE`: Rotation threshold (optional)
- `LOG_RETENTION_DAYS`: Retention period (optional)

**6. MCP Server Configuration** (lines 72-84):
- `MCP_HOST`: Server host address
- `MCP_PORT`: Server port number
- `MCP_INSPECTOR_HOST`: Inspector host address
- `MCP_INSPECTOR_PORT`: Inspector port number
- `MCP_TRANSPORT`: Transport protocol (SSE, HTTP)
- `MCP_REQUEST_TIMEOUT`: Request timeout duration
- `MCP_MAX_CONNECTIONS`: Maximum concurrent connections

**7. Development and Performance Configuration** (lines 87-100):
- `MIGRATION_PHASE`: Migration status tracking
- `DEBUG_MODE`: Debug features flag
- `ENABLE_DEV_FEATURES`: Development features flag
- `ENABLE_PERFORMANCE_MONITORING`: Performance tracking flag
- `MAX_CONCURRENT_REQUESTS`: Concurrency limit
- `MEMORY_LIMIT_MB`: Memory limit in MB
- `REQUEST_TIMEOUT_SECONDS`: Request timeout

**8. Security Configuration** (lines 103-114):
- `ENABLE_AUTH`: Authentication flag
- `CORS_ALLOWED_ORIGINS`: CORS origins
- `RATE_LIMIT_ENABLED`: Rate limiting flag
- `RATE_LIMIT_REQUESTS_PER_MINUTE`: Rate limit threshold
- `TLS_ENABLED`: TLS/SSL flag
- `TLS_CERT_PATH`: Certificate path (optional, commented)
- `TLS_KEY_PATH`: Private key path (optional, commented)

**9. Development Tools and Debugging** (lines 117-126):
- `ENABLE_INSPECTOR_INTEGRATION`: Inspector integration flag
- `ENABLE_PROTOCOL_LOGGING`: Protocol logging flag
- `ENABLE_PERFORMANCE_PROFILING`: Profiling flag
- `UV_DEBUG`: UV package manager debug flag
- `PYTHONPATH_DEBUG`: Python path debugging flag

**10. Data and Storage Configuration** (lines 129-138):
- `DATA_DIR`: Data directory path
- `CACHE_DIR`: Cache directory path
- `TEMP_DIR`: Temporary files directory
- `ENABLE_MEMORY_FALLBACK`: In-memory fallback flag
- `MEMORY_DB_SIZE_LIMIT`: Memory database limit

**11. Deployment Configuration** (lines 141-151):
- `CONTAINER_MODE`: Container deployment flag
- `HEALTH_CHECK_ENABLED`: Health check endpoint flag
- `HEALTH_CHECK_INTERVAL`: Health check interval
- `SERVICE_NAME`: Service name for discovery
- `SERVICE_VERSION`: Service version
- `SERVICE_ENVIRONMENT`: Deployment environment

**Notes**:
- All values are placeholders (`<fill>`) requiring configuration
- Environment variables support multiple deployment scenarios
- Comprehensive coverage from development to production
- Optional variables are commented out

---

#### 4.4 `.mcp.json` - MCP Client Configuration
**Location**: `/home/donbr/lila-graph/lila-mcp/.mcp.json`

**Purpose**: Claude Desktop/client configuration for MCP server discovery

**MCP Servers Configured** (lines 2-70):

**1. mcp-server-time** (lines 3-10):
- **Command**: `uvx`
- **Args**: `["mcp-server-time", "--local-timezone=America/Los_Angeles"]`
- **Purpose**: Time utilities and timezone operations

**2. sequential-thinking** (lines 11-17):
- **Command**: `npx`
- **Args**: `["-y", "@modelcontextprotocol/server-sequential-thinking"]`
- **Purpose**: Sequential thinking and reasoning support

**3. ai-docs-server** (lines 18-42):
- **Command**: `uvx`
- **Package**: `mcpdoc`
- **URLs** (concise documentation):
  - MCPProtocol: https://modelcontextprotocol.io/llms.txt
  - FastMCP: https://gofastmcp.com/llms.txt
  - LangGraph: https://langchain-ai.github.io/langgraph/llms.txt
  - Anthropic: https://docs.anthropic.com/llms.txt
- **Settings**:
  - Transport: stdio
  - Follow redirects: enabled
  - Timeout: 20 seconds
  - Allowed domains: modelcontextprotocol.io, langchain-ai.github.io, docs.anthropic.com, gofastmcp.com

**4. ai-docs-server-full** (lines 43-69):
- **Command**: `uvx`
- **Package**: `mcpdoc`
- **URLs** (full documentation):
  - McpProtocolFull: https://modelcontextprotocol.io/llms-full.txt
  - FastMCPFull: https://gofastmcp.com/llms-full.txt
  - LangGraphFull: https://langchain-ai.github.io/langgraph/llms-full.txt
  - AnthropicFull: https://docs.anthropic.com/llms-full.txt
- **Settings**: Same as ai-docs-server

---

### 5. Infrastructure Scripts

#### 5.1 `init_mcp_database.sh` - Database Initialization Script
**Location**: `/home/donbr/lila-graph/lila-mcp/init_mcp_database.sh` (lines 1-203)

**Purpose**: Automatically initialize Neo4j database for MCP standalone deployment

**Script Configuration** (lines 1-8):
- Shebang: `#!/bin/bash`
- Error handling: `set -e` (exit on error)
- Usage: `./init_mcp_database.sh`

**Color Definitions** (lines 11-16):
- GREEN, BLUE, YELLOW, RED: Terminal color codes for output
- NC: No Color reset

**Environment Variables** (lines 20-26):
- `NEO4J_URI`: Default `bolt://localhost:7687`
- `NEO4J_USER`: Default `neo4j`
- `NEO4J_PASSWORD`: Default `passw0rd`
- `DATA_DIR`: `./data`
- `SEED_DATA_FILE`: `seed_data.cypher`
- `SCHEMA_FILE`: `../../graphs/lila-graph-schema-v8.json`

**Key Functions**:

1. `check_neo4j_ready()` (lines 29-59): Wait for Neo4j startup
   - **Max Attempts**: 30 (line 30)
   - **Retry Delay**: 2 seconds (line 54)
   - **Method**: Python inline script to test connection
   - **Query**: `RETURN 1` to verify connectivity
   - **Output**: Progress messages with attempt counter
   - **Return**: 0 on success, 1 on failure after max attempts

2. `check_database_has_data()` (lines 62-85): Verify existing data
   - **Method**: Python inline script to count personas
   - **Query**: `MATCH (p:PersonaAgent) RETURN count(p) as count`
   - **Return**: 0 if personas exist, 1 if empty
   - **Output**: Persona count message

3. `export_main_system_data()` (lines 88-101): Export from main Lila system
   - **Target**: `bolt://localhost:7687` (main system)
   - **Script**: Calls `export_data.py` with output to seed file
   - **Error Handling**: Silent failure if main system not running
   - **Return**: 0 on success, 1 on failure

4. `import_database_data()` (lines 104-116): Import seed data
   - **Arguments**: Uses NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
   - **Script**: Calls `import_data.py` with seed data or --create-defaults
   - **Fallback**: Creates default personas if no seed file exists

5. `start_services()` (lines 119-132): Start Docker Compose infrastructure
   - **UID/GID Export** (lines 123-124): Set user/group for permissions
   - **Command**: `docker compose up -d`
   - **Wait**: 10-second sleep for service health (line 131)

6. `verify_mcp_server()` (lines 135-148): Verify FastMCP functionality
   - **Check**: `fastmcp` command availability
   - **Test**: `fastmcp inspect` to verify server
   - **Output**: Startup instructions for development and production
   - **Fallback**: Installation message if FastMCP not found

7. `main()` (lines 151-203): Orchestrate initialization workflow
   - **Directory Check** (lines 155-158): Verify fastmcp.json exists
   - **Execution Flow**:
     1. Start services (line 161)
     2. Wait for Neo4j ready (line 164-167)
     3. Check for existing data (line 170)
     4. Export from main system or create defaults (lines 173-178)
     5. Import data (line 181)
     6. Verify import success (line 184-189)
     7. Verify MCP server (line 193)
   - **Output** (lines 195-199):
     - Success message
     - Next steps for development and production
     - Instructions for stopping services

**Entry Point** (line 203):
```bash
main "$@"
```

---

## Entry Points

### Main Entry Points

#### 1. MCP Server Entry Points

**A. Full Production Server** (`lila_mcp_server.py`):

**Direct Execution** (lines 768-779):
```python
async def main():
    logging.basicConfig(level=logging.INFO)
    server = LilaMCPServer()
    try:
        await server.run_server()
    finally:
        server.close()

if __name__ == "__main__":
    asyncio.run(main())
```
- **Command**: `python lila_mcp_server.py`
- **Transport**: SSE (Server-Sent Events)
- **Default Host**: localhost
- **Default Port**: 8765
- **Database**: Requires Neo4j connection

**FastMCP CLI** (lines 764-766):
```python
_server_instance = LilaMCPServer()
mcp = _server_instance.app  # FastMCP looks for 'mcp', 'server', or 'app'
```
- **Development**: `fastmcp dev` (with Inspector UI)
- **Production**: `fastmcp run` (HTTP server)
- **Inspection**: `fastmcp inspect` (capability listing)
- **Configuration**: Uses `fastmcp.json` for auto-configuration

**B. Simplified Development Server** (`simple_lila_mcp_server.py`):

**Module Export** (line 825):
```python
mcp = SimpleLilaMCPServer().app
```
- **Command**: `fastmcp dev simple_lila_mcp_server.py`
- **Purpose**: Development testing with mock data
- **Database**: Optional Neo4j, falls back to mock data
- **Features**: Enhanced debug logging, additional resources

---

#### 2. Data Management Entry Points

**A. Import Data** (`import_data.py`):

**CLI Execution** (lines 465-466):
```python
if __name__ == "__main__":
    main()
```

**Full Command**:
```bash
python import_data.py \
  --seed-data seed_data.cypher \
  --schema graphs/lila-graph-schema-v8.json \
  --uri bolt://localhost:7687 \
  --user neo4j \
  --password passw0rd \
  --create-defaults
```

**Main Function** (lines 409-463):
1. Parse arguments
2. Connect to Neo4j with retry logic (30 attempts, 2s intervals)
3. Load schema (constraints, indexes)
4. Import seed data OR create defaults
5. Verify import (count nodes and relationships)
6. Report results

**B. Export Data** (`export_data.py`):

**CLI Execution** (lines 294-295):
```python
if __name__ == "__main__":
    main()
```

**Full Command**:
```bash
python export_data.py \
  --output seed_data.cypher \
  --uri bolt://localhost:7687 \
  --user neo4j \
  --password passw0rd
```

**Main Function** (lines 245-291):
1. Parse arguments
2. Connect to Neo4j
3. Export personas, relationships, memories, goals
4. Generate Cypher import script
5. Write to output file
6. Report statistics

---

#### 3. Testing Entry Points

**A. Validation Test** (`test_mcp_validation.py`):

**CLI Execution** (lines 170-172):
```python
if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)
```

**Command**:
```bash
python test_mcp_validation.py
```

**Main Function** (lines 134-168):
1. Print banner
2. Test direct connection (in-memory)
   - Connect to SimpleLilaMCPServer
   - Test resources, tools, prompts
   - Return component counts
3. Test Inspector connection (HTTP)
   - Connect to localhost:6274
   - Validate Inspector integration
4. Generate summary report
5. Exit with status code

**Test Coverage**:
- Server connectivity (ping)
- Resource listing and reading
- Tool invocation (analyze_persona_compatibility)
- Prompt retrieval (assess_attachment_style)
- Inspector HTTP connection

**B. Architecture Analysis** (`architecture.py`):

**CLI Execution** (lines 361-362):
```python
if __name__ == "__main__":
    asyncio.run(main())
```

**Command**:
```bash
python architecture.py
```

**Main Function** (lines 282-358):
1. Print configuration banner
2. Define agents (analyzer, doc-writer)
3. Create ClaudeSDKClient with options
4. Run 5 analysis phases:
   - Phase 1: Component inventory
   - Phase 2: Architecture diagrams
   - Phase 3: Data flows
   - Phase 4: API documentation
   - Phase 5: Synthesis
5. Verify outputs
6. Report completion

**Output Files**:
- `repo_analysis/docs/01_component_inventory.md`
- `repo_analysis/diagrams/02_architecture_diagrams.md`
- `repo_analysis/docs/03_data_flows.md`
- `repo_analysis/docs/04_api_reference.md`
- `repo_analysis/README.md`

---

#### 4. Infrastructure Entry Points

**A. Database Initialization** (`init_mcp_database.sh`):

**CLI Execution**:
```bash
./init_mcp_database.sh
```

**Main Function** (lines 151-203):
1. Verify correct directory (check for fastmcp.json)
2. Start Docker Compose services
3. Wait for Neo4j readiness (30 attempts, 2s intervals)
4. Check for existing data
5. Export from main system OR prepare for defaults
6. Import data using import_data.py
7. Verify import success
8. Test MCP server with FastMCP
9. Display next steps

**Prerequisites**:
- Docker Compose installed
- Python 3 with neo4j package
- fastmcp.json in current directory

**Environment Variables**:
- `NEO4J_URI` (default: bolt://localhost:7687)
- `NEO4J_USER` (default: neo4j)
- `NEO4J_PASSWORD` (default: passw0rd)

---

## Dependencies and Imports

### External Dependencies

**MCP Framework**:
- **fastmcp** (v2.12.3+)
  - Used in: `lila_mcp_server.py`, `simple_lila_mcp_server.py`, `test_mcp_validation.py`
  - Key imports: `FastMCP`, `Client`, `Resource`, `Tool`, `Prompt`
  - Purpose: MCP protocol implementation and server framework

**Database**:
- **neo4j** (v5.15.0+)
  - Used in: `lila_mcp_server.py`, `simple_lila_mcp_server.py`, `import_data.py`, `export_data.py`
  - Key imports: `GraphDatabase`
  - Purpose: Neo4j Python driver for graph database operations

**LLM Integration**:
- **openai** (v1.30.0+): OpenAI API client (configured but not directly used in main modules)
- **anthropic** (v0.25.0+): Anthropic API client (configured but not directly used in main modules)

**Data Validation**:
- **pydantic** (v2.6.0+): Data validation and type safety
- **pydantic-settings** (v2.2.0+): Settings management from environment

**Configuration**:
- **python-dotenv**
  - Used in: `lila_mcp_server.py` (lines 15-16), `simple_lila_mcp_server.py` (lines 15-16)
  - Key imports: `load_dotenv`
  - Purpose: Load environment variables from .env file

**Observability**:
- **logfire** (v0.28.0+): Telemetry and monitoring (configured, usage optional)

**Agent Framework**:
- **claude-agent-sdk** (v0.1.0+)
  - Used in: `architecture.py` (lines 13-24)
  - Key imports: `AgentDefinition`, `AssistantMessage`, `ClaudeAgentOptions`, `ClaudeSDKClient`, `ResultMessage`, `TextBlock`, `ToolResultBlock`, `ToolUseBlock`, `UserMessage`
  - Purpose: Claude Agent SDK for automated documentation generation

**HTTP Clients**:
- **httpx** (v0.27.0+): Modern async HTTP client (configured but not directly imported)
- **aiohttp** (v3.9.0+): Async HTTP client/server (configured but not directly imported)

**CLI**:
- **click** (v8.1.0+): Command-line interface creation (configured but not directly used)

### Standard Library Imports

**Core Async and System**:
- `asyncio`: Async runtime and event loops
  - Used in: All async modules for coroutines and tasks
- `logging`: Logging framework
  - Used in: All modules for structured logging
- `os`: Operating system interface
  - Used in: All modules for environment variables and file operations
- `sys`: System-specific parameters and functions
  - Used in: `import_data.py` (line 13), `export_data.py` (line 14) for exit codes
- `pathlib.Path`: Object-oriented filesystem paths
  - Used in: `architecture.py` (line 12), `import_data.py` (line 17), `export_data.py` (line 15)

**Data Handling**:
- `datetime`: Date and time handling
  - Used in: `lila_mcp_server.py` (line 10), `simple_lila_mcp_server.py` (line 10)
  - Purpose: Timestamps for interactions and updates
- `json`: JSON encoding/decoding
  - Used in: `import_data.py` (line 15), `export_data.py` (line 18)
  - Purpose: Schema parsing and data serialization
- `argparse`: Command-line argument parsing
  - Used in: `import_data.py` (line 14), `export_data.py` (line 14)
  - Purpose: CLI interface for data management scripts
- `time`: Time access and conversions
  - Used in: `import_data.py` (line 16)
  - Purpose: Retry delay in connection logic

**Type Hints**:
- `typing`: Type hints support
  - Used in: All modules for type annotations
  - Common imports: `Dict`, `List`, `Optional`, `Any`, `Union`
  - Purpose: Static type checking and IDE support

---

## Component Relationships

### Dependency Graph

```
Production Stack:
├── lila_mcp_server.py (Entry: Production MCP Server)
│   ├── fastmcp → MCP protocol implementation
│   ├── neo4j → Live database queries
│   ├── dotenv → Environment configuration
│   └── logging → Server observability
│
├── import_data.py (Entry: Database Import)
│   ├── neo4j → Database writes with retry logic
│   ├── json → Schema parsing
│   └── argparse → CLI interface
│
├── export_data.py (Entry: Database Export)
│   ├── neo4j → Database reads
│   └── argparse → CLI interface
│
└── init_mcp_database.sh (Entry: Infrastructure Setup)
    ├── docker-compose → Container orchestration
    ├── import_data.py → Data initialization
    └── export_data.py → Main system export

Development Stack:
├── simple_lila_mcp_server.py (Entry: Development Server)
│   ├── fastmcp → MCP protocol implementation
│   └── logging → Debug output (enhanced)
│
├── test_mcp_validation.py (Entry: Validation Tests)
│   ├── fastmcp.Client → Server testing framework
│   └── simple_lila_mcp_server → Test target
│
└── architecture.py (Entry: Documentation Generator)
    ├── claude_agent_sdk → Automated analysis
    └── asyncio → Async execution

Configuration Files:
├── pyproject.toml → Project dependencies and build
├── fastmcp.json → FastMCP server discovery
├── .env.example → Environment template
└── .mcp.json → Claude Desktop MCP client config
```

### Data Flow Patterns

**1. Production Data Flow**:
```
Neo4j Database
    ↓ (read)
lila_mcp_server.py
    ↓ (MCP protocol)
FastMCP Framework
    ↓ (SSE/HTTP)
MCP Clients (Claude, etc.)
```

**2. Development Data Flow**:
```
Mock Data (in-memory)
    ↓ (read)
simple_lila_mcp_server.py
    ↓ (MCP protocol)
FastMCP Framework
    ↓ (SSE/HTTP)
MCP Inspector / Test Clients
```

**3. Database Initialization Flow**:
```
Main Lila System (optional)
    ↓ (export via export_data.py)
seed_data.cypher
    ↓ (import via import_data.py)
Neo4j Database
    ↑ (verify)
init_mcp_database.sh (orchestration)
```

**4. Testing Flow**:
```
SimpleLilaMCPServer
    ↓ (direct connection)
FastMCP Client
    ↓ (test assertions)
test_mcp_validation.py
    ↓ (exit code)
CI/CD Pipeline
```

---

## File Size Statistics

| File | Lines | Purpose | Complexity |
|------|-------|---------|------------|
| `lila_mcp_server.py` | 779 | Full production MCP server | High |
| `simple_lila_mcp_server.py` | 830 | Simplified development server | Medium |
| `import_data.py` | 466 | Neo4j data import utility | Medium |
| `export_data.py` | 295 | Neo4j data export utility | Low |
| `test_mcp_validation.py` | 172 | MCP validation test suite | Low |
| `architecture.py` | 363 | Architecture analysis tool | Medium |
| `init_mcp_database.sh` | 203 | Database initialization script | Medium |
| `pyproject.toml` | 77 | Project configuration | Low |
| `.env.example` | 151 | Environment template | Low |

**Total Code**: ~3,336 lines (excluding tests and documentation)

**Code Distribution**:
- MCP Servers: 1,609 lines (48%)
- Data Management: 761 lines (23%)
- Testing/Analysis: 535 lines (16%)
- Configuration: 431 lines (13%)

---

## Configuration Surface

### Required Environment Variables

**Production Deployment**:
- `NEO4J_URI`: Neo4j connection string (default: `bolt://localhost:7687`)
- `NEO4J_USER`: Database username (default: `neo4j`)
- `NEO4J_PASSWORD`: Database password (default: `passw0rd`)

### Optional Configuration

**Server Settings**:
- `MCP_HOST`: Server host (default: `localhost`)
- `MCP_PORT`: Server port (default: `8765`)
- `MCP_TRANSPORT`: Transport protocol (default: `sse`)

**Logging and Observability**:
- `LOG_LEVEL`: Logging verbosity (default: `INFO`)
- `ENABLE_LOGFIRE_TELEMETRY`: Enable observability (default: `false`)
- `LOGFIRE_PROJECT_NAME`: Project name for telemetry

**Development Options**:
- `DEBUG_MODE`: Enable debug features
- `DISABLE_NEO4J`: Disable database connection (use mock data)
- `MIGRATION_PHASE`: Track migration progress

**Performance Tuning**:
- `NEO4J_TIMEOUT`: Connection timeout
- `NEO4J_MAX_RETRY_TIME`: Maximum retry duration
- `MAX_CONCURRENT_REQUESTS`: Concurrency limit
- `MEMORY_LIMIT_MB`: Memory limit

**Security Settings**:
- `ENABLE_AUTH`: Authentication flag
- `CORS_ALLOWED_ORIGINS`: CORS configuration
- `RATE_LIMIT_ENABLED`: Rate limiting flag
- `TLS_ENABLED`: TLS/SSL flag

### Configuration File Hierarchy

1. **fastmcp.json**: FastMCP server discovery and entrypoint
2. **.env**: Runtime environment variables (loaded by python-dotenv)
3. **.env.example**: Template for environment configuration
4. **pyproject.toml**: Project dependencies and build configuration
5. **.mcp.json**: MCP client configuration for Claude Desktop

---

## Summary

This codebase implements a complete psychological intelligence MCP server with:

### Core Features

**1. Dual Server Implementations**:
- **Production** (`lila_mcp_server.py`): Full Neo4j integration, 5 resources, 6 tools, 3 prompts
- **Development** (`simple_lila_mcp_server.py`): Mock data fallback, 9 resources, 8 tools, 3 prompts

**2. Comprehensive MCP Interface**:
- **Resources**: Persona profiles, relationships, interactions, emotional climate, psychological insights
- **Tools**: Relationship updates, interaction recording, compatibility analysis, strategy selection, goal assessment, response generation
- **Prompts**: Attachment style assessment, emotional climate analysis, secure response generation

**3. Database Management**:
- **Import Utility**: Schema loading, retry logic, DISC to Big Five mapping, default persona creation
- **Export Utility**: Multi-entity export (personas, relationships, memories, goals), Cypher script generation

**4. Testing Infrastructure**:
- **Validation Suite**: Direct connection testing, Inspector integration testing, comprehensive component validation
- **Architecture Analysis**: Automated documentation generation using Claude Agent SDK

**5. Infrastructure Automation**:
- **Initialization Script**: Docker Compose orchestration, Neo4j readiness checks, data import/export coordination

### Key Design Patterns

**Psychological Modeling**:
- Attachment theory (secure, anxious, avoidant, exploratory)
- Big Five personality traits (OCEAN model)
- Graph database for relationship modeling
- Emotional valence tracking
- Relationship metrics (trust, intimacy, strength)

**Software Architecture**:
- MCP protocol for AI integration
- Retry logic and error handling for reliability
- Mock data for development without infrastructure
- Health check endpoints for container orchestration
- CLI interfaces for all utilities
- Async/await throughout for scalability

**Development Workflow**:
- FastMCP Inspector for visual testing
- Direct in-memory testing for fast iteration
- Comprehensive validation suite
- Automated documentation generation
- Environment-based configuration

### Deployment Options

**Development**:
```bash
fastmcp dev                          # Full server with Inspector
fastmcp dev simple_lila_mcp_server.py  # Simplified server with Inspector
python test_mcp_validation.py       # Validation tests
```

**Production**:
```bash
./init_mcp_database.sh              # Initialize infrastructure
fastmcp run                         # Production HTTP server
python lila_mcp_server.py           # Direct SSE server
```

**Data Management**:
```bash
python import_data.py --schema schema.json --create-defaults
python export_data.py --output seed_data.cypher
```

**Documentation**:
```bash
python architecture.py              # Generate comprehensive docs
```

### Technology Stack

**Core Technologies**:
- Python 3.12+
- FastMCP framework
- Neo4j graph database
- Docker Compose

**Key Libraries**:
- fastmcp: MCP protocol implementation
- neo4j: Graph database driver
- pydantic: Data validation
- python-dotenv: Configuration management
- claude-agent-sdk: Automated documentation

**Development Tools**:
- pytest: Testing framework
- black: Code formatting
- ruff: Linting
- uv: Package management
