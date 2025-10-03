# API Reference

## Overview

The Lila MCP (Model Context Protocol) system provides a comprehensive API for psychological relationship modeling and analysis. The system exposes three main interface types:

- **MCP Resources**: Read-only data access endpoints for personas, relationships, and interactions
- **MCP Tools**: Action-oriented endpoints for updating data and generating analyses
- **MCP Prompts**: Templated prompts for LLM-based psychological assessments

The API is built on FastMCP and integrates with Neo4j for graph-based relationship storage.

**Base Components:**
- Primary Server: `/home/donbr/lila-graph/lila-mcp/lila_mcp_server.py`
- Simplified Server: `/home/donbr/lila-graph/lila-mcp/simple_lila_mcp_server.py`
- Data Import: `/home/donbr/lila-graph/lila-mcp/import_data.py`
- Data Export: `/home/donbr/lila-graph/lila-mcp/export_data.py`

---

## Core Classes

### LilaMCPServer

**Source:** `/home/donbr/lila-graph/lila-mcp/lila_mcp_server.py:29-750`

The primary MCP server class that connects to Neo4j and exposes psychological relationship data.

```python
class LilaMCPServer:
    """MCP server exposing Lila's psychological relationship data and tools with Neo4j integration."""

    def __init__(self):
        """Initialize the MCP server with Neo4j database connection."""
```

#### Methods

##### `__init__(self) -> None`

**Lines:** 32-43

Initializes the server, sets up Neo4j connection, and registers all MCP endpoints.

**Example:**
```python
from lila_mcp_server import LilaMCPServer

server = LilaMCPServer()
# Server is now ready with Neo4j connected
```

**Configuration Required:**
- `NEO4J_URI`: Default `bolt://localhost:7687`
- `NEO4J_USER`: Default `neo4j`
- `NEO4J_PASSWORD`: Required

##### `_setup_database(self) -> None`

**Lines:** 45-62

Establishes Neo4j connection with environment-based configuration.

**Environment Variables:**
- `NEO4J_URI`: Neo4j connection URI
- `NEO4J_USER`: Database username
- `NEO4J_PASSWORD`: Database password

**Error Handling:**
```python
# If connection fails, driver is set to None
# All resources/tools will return error JSON responses
```

##### `close(self) -> None`

**Lines:** 63-66

Safely closes the Neo4j driver connection.

**Example:**
```python
server = LilaMCPServer()
try:
    await server.run_server()
finally:
    server.close()  # Always close the connection
```

##### `async run_server(self, host: str = "localhost", port: int = 8765) -> None`

**Lines:** 740-746

Starts the MCP server with SSE transport.

**Parameters:**
- `host` (str): Server host address (default: "localhost")
- `port` (int): Server port (default: 8765)

**Example:**
```python
import asyncio

server = LilaMCPServer()
asyncio.run(server.run_server(host="0.0.0.0", port=8766))
```

---

### SimpleLilaMCPServer

**Source:** `/home/donbr/lila-graph/lila-mcp/simple_lila_mcp_server.py:33-843`

A simplified MCP server with the same interface as LilaMCPServer, useful for testing and development.

```python
class SimpleLilaMCPServer:
    """MCP server exposing Lila's psychological relationship data and tools with Neo4j integration."""

    def __init__(self):
        """Initialize the MCP server with Neo4j database connection."""
```

**Key Differences from LilaMCPServer:**
- Enhanced debug logging enabled by default (line 28-29)
- Same API surface but optimized for development
- Includes additional development-focused resources

---

## MCP Resources

Resources provide read-only access to psychological data stored in Neo4j.

### neo4j://personas/all

**Lines:** 71-113 (lila_mcp_server.py)

Retrieves all personas with their psychological profiles.

**URI:** `neo4j://personas/all`

**Return Type:** JSON string

**Return Schema:**
```json
{
  "personas": [
    {
      "id": "string",
      "name": "string",
      "age": number,
      "role": "string",
      "attachment_style": "secure|anxious|avoidant|exploratory",
      "personality": {
        "openness": number,        // 0.0-1.0
        "conscientiousness": number,
        "extraversion": number,
        "agreeableness": number,
        "neuroticism": number
      }
    }
  ],
  "count": number,
  "last_updated": "ISO-8601 timestamp"
}
```

**Cypher Query:**
```cypher
MATCH (p:PersonaAgent)
RETURN p.persona_id as persona_id, p.name as name, p.age as age, p.role as role,
       p.attachment_style as attachment_style,
       p.openness as openness, p.conscientiousness as conscientiousness,
       p.extraversion as extraversion, p.agreeableness as agreeableness, p.neuroticism as neuroticism
ORDER BY p.name
```

**Usage Example:**
```python
from fastmcp import Client

async with Client(mcp_server) as client:
    personas = await client.read_resource("neo4j://personas/all")
    print(f"Found {personas['count']} personas")
```

**Error Response:**
```json
{"error": "Neo4j database not available"}
```

---

### neo4j://personas/{persona_id}

**Lines:** 115-160 (lila_mcp_server.py)

Retrieves a specific persona by ID with full psychological profile.

**URI Pattern:** `neo4j://personas/{persona_id}`

**Parameters:**
- `persona_id` (str): Unique identifier for the persona (e.g., "lila", "alex")

**Return Schema:**
```json
{
  "persona": {
    "id": "string",
    "name": "string",
    "age": number,
    "role": "string",
    "description": "string",
    "attachment_style": "string",
    "personality": {
      "openness": number,
      "conscientiousness": number,
      "extraversion": number,
      "agreeableness": number,
      "neuroticism": number
    },
    "trust_level": number,        // 0.0-1.0
    "communication_style": "string"
  },
  "last_updated": "ISO-8601 timestamp"
}
```

**Cypher Query:**
```cypher
MATCH (p:PersonaAgent {persona_id: $persona_id})
RETURN p.persona_id as persona_id, p.name as name, p.age as age, p.role as role,
       p.description as description, p.attachment_style as attachment_style,
       p.openness as openness, p.conscientiousness as conscientiousness,
       p.extraversion as extraversion, p.agreeableness as agreeableness, p.neuroticism as neuroticism,
       p.trust_level as trust_level, p.communication_style as communication_style
```

**Usage Example:**
```python
async with Client(mcp_server) as client:
    lila = await client.read_resource("neo4j://personas/lila")
    print(f"Attachment style: {lila['persona']['attachment_style']}")
```

**Error Response:**
```json
{"error": "Persona {persona_id} not found"}
```

---

### neo4j://relationships/all

**Lines:** 162-205 (lila_mcp_server.py)

Retrieves all relationships with psychological metrics.

**URI:** `neo4j://relationships/all`

**Return Schema:**
```json
{
  "relationships": [
    {
      "persona1_id": "string",
      "persona1_name": "string",
      "persona2_id": "string",
      "persona2_name": "string",
      "trust_level": number,           // 0.0-10.0
      "intimacy_level": number,        // 0.0-10.0
      "relationship_strength": number, // 0.0-10.0
      "interaction_count": number,
      "relationship_type": "string",
      "emotional_valence": number      // -1.0 to 1.0
    }
  ],
  "count": number,
  "last_updated": "ISO-8601 timestamp"
}
```

**Cypher Query:**
```cypher
MATCH (p1:PersonaAgent)-[r:RELATIONSHIP]->(p2:PersonaAgent)
RETURN p1.persona_id as persona1_id, p1.name as persona1_name,
       p2.persona_id as persona2_id, p2.name as persona2_name,
       r.trust_level as trust_level, r.intimacy_level as intimacy_level,
       r.relationship_strength as relationship_strength,
       r.interaction_count as interaction_count,
       r.relationship_type as relationship_type,
       r.emotional_valence as emotional_valence
ORDER BY r.relationship_strength DESC
```

**Usage Example:**
```python
async with Client(mcp_server) as client:
    relationships = await client.read_resource("neo4j://relationships/all")
    for rel in relationships['relationships']:
        print(f"{rel['persona1_name']} ↔ {rel['persona2_name']}: Trust {rel['trust_level']}/10")
```

---

### neo4j://relationships/{persona1_id}/{persona2_id}

**Lines:** 207-252 (lila_mcp_server.py)

Retrieves specific relationship metrics between two personas.

**URI Pattern:** `neo4j://relationships/{persona1_id}/{persona2_id}`

**Parameters:**
- `persona1_id` (str): First persona identifier
- `persona2_id` (str): Second persona identifier

**Return Schema:**
```json
{
  "relationship": {
    "persona1_id": "string",
    "persona1_name": "string",
    "persona2_id": "string",
    "persona2_name": "string",
    "trust_level": number,
    "intimacy_level": number,
    "relationship_strength": number,
    "interaction_count": number,
    "relationship_type": "string",
    "emotional_valence": number,
    "created_at": "string|null",
    "updated_at": "string|null"
  },
  "last_updated": "ISO-8601 timestamp"
}
```

**Cypher Query:**
```cypher
MATCH (p1:PersonaAgent {persona_id: $persona1_id})-[r:RELATIONSHIP]-(p2:PersonaAgent {persona_id: $persona2_id})
RETURN p1.name as name1, p2.name as name2,
       r.trust_level as trust_level, r.intimacy_level as intimacy_level,
       r.relationship_strength as relationship_strength,
       r.interaction_count as interaction_count,
       r.relationship_type as relationship_type,
       r.emotional_valence as emotional_valence,
       r.created_at as created_at, r.updated_at as updated_at
LIMIT 1
```

**Note:** Query is bidirectional - works regardless of persona order.

**Usage Example:**
```python
async with Client(mcp_server) as client:
    rel = await client.read_resource("neo4j://relationships/lila/alex")
    print(f"Trust: {rel['relationship']['trust_level']}/10")
    print(f"Interactions: {rel['relationship']['interaction_count']}")
```

**Error Response:**
```json
{"error": "No relationship found between {persona1_id} and {persona2_id}"}
```

---

### neo4j://interactions/recent/{count}

**Lines:** 254-294 (lila_mcp_server.py)

Retrieves recent interactions with psychological analysis.

**URI Pattern:** `neo4j://interactions/recent/{count}`

**Parameters:**
- `count` (str): Number of interactions to retrieve (max: 50, default: "10")

**Return Schema:**
```json
{
  "interactions": [
    {
      "id": "string",
      "from": "string",
      "to": "string",
      "content": "string",
      "emotional_valence": number,
      "timestamp": "ISO-8601 timestamp"
    }
  ],
  "count": number,
  "last_updated": "ISO-8601 timestamp"
}
```

**Cypher Query:**
```cypher
MATCH (p1:PersonaAgent)-[r:RELATIONSHIP]-(p2:PersonaAgent)
RETURN p1.name as from_name, p2.name as to_name,
       r.last_interaction as last_interaction,
       r.relationship_type as relationship_type,
       r.emotional_valence as emotional_valence
ORDER BY r.updated_at DESC
LIMIT $count
```

**Usage Example:**
```python
async with Client(mcp_server) as client:
    interactions = await client.read_resource("neo4j://interactions/recent/20")
    print(f"Retrieved {interactions['count']} recent interactions")
```

---

## MCP Tools

Tools provide action-oriented endpoints for modifying data and generating analyses.

### update_relationship_metrics

**Lines:** 299-359 (lila_mcp_server.py)

Updates relationship metrics between two personas with bounds checking.

**Function Signature:**
```python
async def update_relationship_metrics(
    persona1_id: str,
    persona2_id: str,
    trust_delta: float = 0.0,
    intimacy_delta: float = 0.0,
    strength_delta: float = 0.0
) -> str
```

**Parameters:**
- `persona1_id` (str): First persona identifier
- `persona2_id` (str): Second persona identifier
- `trust_delta` (float): Change in trust level (-10.0 to +10.0)
- `intimacy_delta` (float): Change in intimacy level (-10.0 to +10.0)
- `strength_delta` (float): Change in relationship strength (-10.0 to +10.0)

**Returns:** JSON string with updated metrics

**Return Schema:**
```json
{
  "success": true,
  "updated_relationship": {
    "participants": ["persona1_id", "persona2_id"],
    "participant_names": ["name1", "name2"],
    "trust_level": number,          // 0.0-10.0
    "intimacy_level": number,       // 0.0-10.0
    "relationship_strength": number, // 0.0-10.0
    "changes": {
      "trust_delta": number,
      "intimacy_delta": number,
      "strength_delta": number
    }
  }
}
```

**Cypher Query:**
```cypher
MATCH (p1:PersonaAgent {persona_id: $persona1_id})-[r:RELATIONSHIP]-(p2:PersonaAgent {persona_id: $persona2_id})
SET r.trust_level = CASE
    WHEN r.trust_level + $trust_delta > 10.0 THEN 10.0
    WHEN r.trust_level + $trust_delta < 0.0 THEN 0.0
    ELSE r.trust_level + $trust_delta
END,
r.intimacy_level = CASE
    WHEN r.intimacy_level + $intimacy_delta > 10.0 THEN 10.0
    WHEN r.intimacy_level + $intimacy_delta < 0.0 THEN 0.0
    ELSE r.intimacy_level + $intimacy_delta
END,
r.relationship_strength = CASE
    WHEN r.relationship_strength + $strength_delta > 10.0 THEN 10.0
    WHEN r.relationship_strength + $strength_delta < 0.0 THEN 0.0
    ELSE r.relationship_strength + $strength_delta
END,
r.updated_at = datetime()
RETURN p1.name as name1, p2.name as name2,
       r.trust_level as trust, r.intimacy_level as intimacy,
       r.relationship_strength as strength
```

**Usage Example:**
```python
async with Client(mcp_server) as client:
    # Increase trust by 0.5 after positive interaction
    result = await client.call_tool("update_relationship_metrics", {
        "persona1_id": "lila",
        "persona2_id": "alex",
        "trust_delta": 0.5,
        "intimacy_delta": 0.2,
        "strength_delta": 0.3
    })
    print(result.content[0].text)
```

**Error Response:**
```json
{"error": "No relationship found between {persona1_id} and {persona2_id}"}
```

**Best Practices:**
- Use small delta values (0.1-0.5) for realistic progression
- Negative deltas represent deterioration in relationship quality
- All metrics are automatically bounded to 0.0-10.0 range
- Updates are atomic and immediately persisted to Neo4j

---

### record_interaction

**Lines:** 361-398 (lila_mcp_server.py)

Records an interaction between two personas with psychological analysis.

**Function Signature:**
```python
async def record_interaction(
    sender_id: str,
    recipient_id: str,
    content: str,
    emotional_valence: float = 0.0,
    relationship_impact: float = 0.0
) -> str
```

**Parameters:**
- `sender_id` (str): Persona who initiated the interaction
- `recipient_id` (str): Persona who received the interaction
- `content` (str): Interaction content/message
- `emotional_valence` (float): Emotional tone (-1.0 to +1.0, default: 0.0)
- `relationship_impact` (float): Expected impact on relationship (0.0-1.0)

**Returns:** JSON string with interaction record

**Return Schema:**
```json
{
  "success": true,
  "interaction_id": "string",
  "recorded": {
    "sender_id": "string",
    "recipient_id": "string",
    "content_length": number,
    "emotional_valence": number,
    "relationship_impact": number
  }
}
```

**Cypher Query:**
```cypher
MATCH (p1:PersonaAgent {persona_id: $sender_id})-[r:RELATIONSHIP]-(p2:PersonaAgent {persona_id: $recipient_id})
SET r.last_interaction = datetime(),
    r.interaction_count = COALESCE(r.interaction_count, 0) + 1,
    r.emotional_valence = ($emotional_valence + COALESCE(r.emotional_valence, 0.0)) / 2
```

**Usage Example:**
```python
async with Client(mcp_server) as client:
    result = await client.call_tool("record_interaction", {
        "sender_id": "lila",
        "recipient_id": "alex",
        "content": "I really appreciate your support today!",
        "emotional_valence": 0.8,
        "relationship_impact": 0.3
    })
    interaction_data = json.loads(result.content[0].text)
    print(f"Recorded: {interaction_data['interaction_id']}")
```

**Notes:**
- Interaction ID format: `int_{sender}_{recipient}_{timestamp_ms}`
- Updates relationship's emotional valence as moving average
- Increments interaction counter
- Sets last_interaction timestamp

---

### analyze_persona_compatibility

**Lines:** 400-460 (lila_mcp_server.py)

Assesses relationship potential between two personas based on attachment styles.

**Function Signature:**
```python
async def analyze_persona_compatibility(
    persona1_id: str,
    persona2_id: str,
    relationship_type: str = "romantic"
) -> str
```

**Parameters:**
- `persona1_id` (str): First persona identifier
- `persona2_id` (str): Second persona identifier
- `relationship_type` (str): Type of relationship context (default: "romantic")

**Returns:** JSON string with compatibility analysis

**Return Schema:**
```json
{
  "compatibility_analysis": {
    "persona1": {
      "id": "string",
      "name": "string",
      "attachment_style": "string"
    },
    "persona2": {
      "id": "string",
      "name": "string",
      "attachment_style": "string"
    },
    "relationship_type": "string",
    "compatibility_level": "High|Good|Moderate|Challenging|Difficult|Low",
    "analysis": "string",
    "recommendations": ["string"]
  }
}
```

**Compatibility Matrix:**
```python
{
    ("secure", "secure"): ("High", "Both partners provide stability and emotional availability"),
    ("secure", "anxious"): ("Good", "Secure partner can provide reassurance to anxious partner"),
    ("secure", "avoidant"): ("Moderate", "Secure partner may help avoidant partner open up gradually"),
    ("anxious", "anxious"): ("Challenging", "Both partners may escalate emotional intensity"),
    ("anxious", "avoidant"): ("Difficult", "Classic pursue-withdraw dynamic may develop"),
    ("avoidant", "avoidant"): ("Low", "Both partners may avoid emotional intimacy"),
}
```

**Cypher Query:**
```cypher
MATCH (p1:PersonaAgent {persona_id: $persona1_id}), (p2:PersonaAgent {persona_id: $persona2_id})
RETURN p1.name as name1, p1.attachment_style as style1,
       p2.name as name2, p2.attachment_style as style2
```

**Usage Example:**
```python
async with Client(mcp_server) as client:
    compatibility = await client.call_tool("analyze_persona_compatibility", {
        "persona1_id": "lila",
        "persona2_id": "alex",
        "relationship_type": "friendship"
    })
    analysis = json.loads(compatibility.content[0].text)
    print(f"Compatibility: {analysis['compatibility_analysis']['compatibility_level']}")
    print(f"Analysis: {analysis['compatibility_analysis']['analysis']}")
```

**Recommendations Always Include:**
1. Focus on understanding each other's attachment needs
2. Practice clear, consistent communication
3. Respect differences in emotional expression and intimacy pace

---

### autonomous_strategy_selection

**Lines:** 462-512 (lila_mcp_server.py)

AI-driven strategy selection based on attachment theory and context analysis.

**Function Signature:**
```python
async def autonomous_strategy_selection(
    persona_id: str,
    conversation_context: str = "",
    situation_assessment: str = "",
    active_goals: str = "",
    attachment_style: str = "secure"
) -> str
```

**Parameters:**
- `persona_id` (str): Persona making the strategic decision
- `conversation_context` (str): Current conversation context
- `situation_assessment` (str): Assessment of the current situation
- `active_goals` (str): Active relationship goals
- `attachment_style` (str): Persona's attachment style

**Returns:** JSON string with selected strategy

**Return Schema:**
```json
{
  "strategy_selection": {
    "persona_id": "string",
    "selected_strategy": "string",
    "attachment_style": "string",
    "context": "string",
    "available_strategies": ["string"],
    "reasoning": "string"
  }
}
```

**Strategy Mapping:**
```python
attachment_strategies = {
    "secure": [
        "emotional_bonding",
        "vulnerable_disclosure",
        "supportive_listening",
        "trust_building"
    ],
    "anxious": [
        "reassurance_seeking",
        "emotional_validation",
        "secure_bonding",
        "safety_creation"
    ],
    "avoidant": [
        "autonomous_connection",
        "thoughtful_presence",
        "respectful_distance",
        "gradual_opening"
    ],
    "exploratory": [
        "growth_oriented_support",
        "playful_engagement",
        "curious_exploration",
        "authentic_expression"
    ]
}
```

**Context-Based Selection Logic:**
- **"first" or "new" in context:**
  - Anxious → reassurance_seeking
  - Avoidant → thoughtful_presence
  - Other → emotional_bonding
- **"deep" or "intimate" in context:**
  - Non-avoidant → vulnerable_disclosure
  - Avoidant → gradual_opening
- **"trust" in goals:** → trust_building
- **"vulnerability" in goals:** → vulnerable_disclosure
- **Default:** First strategy from attachment list

**Usage Example:**
```python
async with Client(mcp_server) as client:
    strategy = await client.call_tool("autonomous_strategy_selection", {
        "persona_id": "lila",
        "conversation_context": "First deep conversation about feelings",
        "active_goals": "build trust, increase vulnerability",
        "attachment_style": "secure"
    })
    selection = json.loads(strategy.content[0].text)
    print(f"Selected: {selection['strategy_selection']['selected_strategy']}")
    print(f"Reasoning: {selection['strategy_selection']['reasoning']}")
```

---

### assess_goal_progress

**Lines:** 514-551 (lila_mcp_server.py)

Assesses progress toward relationship goals based on recent interactions.

**Function Signature:**
```python
async def assess_goal_progress(
    persona_id: str,
    goals: str = "",
    recent_interactions: str = ""
) -> str
```

**Parameters:**
- `persona_id` (str): Persona whose goals are being assessed
- `goals` (str): Comma-separated list of goals
- `recent_interactions` (str): Summary of recent interactions

**Returns:** JSON string with progress assessment

**Return Schema:**
```json
{
  "goal_progress": {
    "persona_id": "string",
    "assessed_goals": [
      {
        "goal": "string",
        "progress": number,      // 0.0-1.0
        "assessment": "string"
      }
    ],
    "overall_progress": number,  // 0.0-1.0
    "assessment_timestamp": "ISO-8601 timestamp"
  }
}
```

**Default Progress Rates:**
- Trust goals: 0.15
- Intimacy goals: 0.08
- Vulnerability goals: 0.12
- Other goals: 0.10

**Usage Example:**
```python
async with Client(mcp_server) as client:
    progress = await client.call_tool("assess_goal_progress", {
        "persona_id": "lila",
        "goals": "build trust, increase intimacy, practice vulnerability"
    })
    assessment = json.loads(progress.content[0].text)
    print(f"Overall progress: {assessment['goal_progress']['overall_progress']:.1%}")
    for goal in assessment['goal_progress']['assessed_goals']:
        print(f"  {goal['goal']}: {goal['progress']:.1%}")
```

---

### generate_contextual_response

**Lines:** 553-607 (lila_mcp_server.py)

Generates psychologically authentic response for a persona in a given context.

**Function Signature:**
```python
async def generate_contextual_response(
    persona_id: str,
    context: str,
    goals: str = "",
    constraints: str = ""
) -> str
```

**Parameters:**
- `persona_id` (str): Persona generating the response
- `context` (str): Situational context for the response
- `goals` (str): Active goals influencing the response
- `constraints` (str): Any constraints on the response

**Returns:** JSON string with generated response

**Return Schema:**
```json
{
  "contextual_response": {
    "persona_id": "string",
    "persona_name": "string",
    "response": "string",
    "strategy_used": "string",
    "attachment_style": "string",
    "context": "string",
    "psychological_rationale": "string"
  }
}
```

**Response Patterns by Attachment Style:**

**Secure:**
```python
response_text = "I appreciate you sharing that with me. How can we work together on this?"
strategy = "supportive_listening"
```

**Anxious:**
```python
response_text = "Thank you for telling me this. I want to make sure I understand how you're feeling."
strategy = "emotional_validation"
```

**Avoidant:**
```python
response_text = "I hear what you're saying. Let me think about that for a moment."
strategy = "thoughtful_presence"
```

**Exploratory:**
```python
response_text = "That's really interesting. I'd love to explore this more with you."
strategy = "curious_exploration"
```

**Cypher Query:**
```cypher
MATCH (p:PersonaAgent {persona_id: $persona_id})
RETURN p.name as name, p.attachment_style as attachment_style,
       p.communication_style as communication_style
```

**Usage Example:**
```python
async with Client(mcp_server) as client:
    response = await client.call_tool("generate_contextual_response", {
        "persona_id": "lila",
        "context": "Partner shared a difficult childhood memory",
        "goals": "provide support, deepen intimacy"
    })
    generated = json.loads(response.content[0].text)
    print(f"Response: {generated['contextual_response']['response']}")
    print(f"Strategy: {generated['contextual_response']['strategy_used']}")
```

---

## MCP Prompts

Prompts provide templated LLM prompts for psychological assessments and therapeutic guidance.

### assess_attachment_style

**Lines:** 612-642 (lila_mcp_server.py)

Determines persona's attachment style from behavioral observations.

**Function Signature:**
```python
def assess_attachment_style(
    persona_id: str,
    observation_period: str = "recent",
    behavioral_examples: str = ""
) -> str
```

**Parameters:**
- `persona_id` (str): Persona being assessed
- `observation_period` (str): Timeframe of observations (default: "recent")
- `behavioral_examples` (str): Specific behavioral observations

**Returns:** Formatted prompt string for LLM analysis

**Prompt Structure:**

1. **Attachment Styles to Consider:**
   - Secure: Comfortable with intimacy and autonomy, emotionally available, trusting
   - Anxious: Seeks closeness but fears abandonment, heightened emotional responses
   - Avoidant: Values independence, uncomfortable with too much closeness
   - Exploratory: Seeks authentic expression and freedom, values personal growth

2. **Analysis Framework:**
   - Emotional Regulation
   - Intimacy Comfort
   - Relationship Patterns
   - Communication Style
   - Response to Partner Distress

3. **Expected Output:**
   - Primary Attachment Style with confidence level
   - Supporting Evidence from behavioral observations
   - Secondary Patterns if present
   - Therapeutic Implications
   - Recommendations for healthy attachment behaviors

**Usage Example:**
```python
async with Client(mcp_server) as client:
    prompt_result = await client.get_prompt("assess_attachment_style", {
        "persona_id": "alex",
        "observation_period": "past 3 months",
        "behavioral_examples": "Shows hesitation to share emotions, prefers solving problems alone, withdraws during conflict"
    })

    # Send to LLM for analysis
    llm_response = await llm.complete(prompt_result.messages[0].content)
    print(llm_response)
```

**Prompt Template (excerpt):**
```
You are a psychological researcher specializing in attachment theory.
Please analyze the behavioral patterns of persona {persona_id} to
determine their attachment style.

ATTACHMENT STYLES TO CONSIDER:
• Secure: Comfortable with intimacy and autonomy, emotionally available, trusting
• Anxious: Seeks closeness but fears abandonment, heightened emotional responses
• Avoidant: Values independence, uncomfortable with too much closeness
• Exploratory: Seeks authentic expression and freedom, values personal growth

ANALYSIS FRAMEWORK:
1. Emotional Regulation: How does this persona handle stress, conflict, or intense emotions?
2. Intimacy Comfort: How do they approach emotional closeness and vulnerability?
...
```

---

### analyze_emotional_climate

**Lines:** 644-693 (lila_mcp_server.py)

Evaluates conversation emotional dynamics and safety levels.

**Function Signature:**
```python
def analyze_emotional_climate(
    conversation_text: str = "",
    interaction_id: str = "",
    participants: str = ""
) -> str
```

**Parameters:**
- `conversation_text` (str): Full conversation transcript
- `interaction_id` (str): Optional interaction identifier
- `participants` (str): Names/IDs of participants

**Returns:** Formatted prompt string for LLM analysis

**Assessment Framework:**

1. **Safety Level (1-10 scale):**
   - Psychological safety for vulnerability
   - Respect for boundaries
   - Absence of criticism, contempt, defensiveness, stonewalling

2. **Emotional Attunement:**
   - Recognition of emotional needs
   - Empathic responses
   - Emotional validation vs. dismissal

3. **Communication Quality:**
   - Active listening indicators
   - "I" statements vs. "you" statements
   - Constructive vs. destructive patterns

4. **Power Dynamics:**
   - Balance vs. imbalance in speaking time
   - Respect for autonomy
   - Coercive or manipulative elements

5. **Attachment Activation:**
   - Signs of attachment system activation
   - Security-building vs. threat responses
   - Repair attempts during conflict

**Expected Output:**
- Overall Safety Score (1-10) with rationale
- Key Emotional Patterns observed
- Attachment Dynamics at play
- Warning Signs if present
- Strengths in the interaction
- Recommendations for improving emotional climate
- Therapeutic Focus Areas for future work

**Usage Example:**
```python
async with Client(mcp_server) as client:
    conversation = """
    Alex: I feel like you never listen to me.
    Lila: I hear you're frustrated. Can you tell me more about what you need?
    Alex: I just need to know you care about what I'm saying.
    Lila: I do care. Your feelings matter to me. Let me put my phone down.
    """

    prompt_result = await client.get_prompt("analyze_emotional_climate", {
        "conversation_text": conversation,
        "participants": "Alex, Lila"
    })

    llm_response = await llm.complete(prompt_result.messages[0].content)
    print(f"Safety assessment: {llm_response}")
```

**Prompt Template (excerpt):**
```
You are a relationship therapist analyzing emotional dynamics in
interpersonal communication. Please evaluate the emotional climate
and safety levels in this interaction.

EMOTIONAL CLIMATE ASSESSMENT FRAMEWORK:

1. Safety Level (1-10 scale):
   - Psychological safety for vulnerability
   - Respect for boundaries
   - Absence of criticism, contempt, defensiveness, stonewalling
...
```

---

### generate_secure_response

**Lines:** 695-738 (lila_mcp_server.py)

Creates attachment-security-building responses for various scenarios.

**Function Signature:**
```python
def generate_secure_response(
    scenario_description: str,
    personas: str,
    insecurity_triggers: str = "",
    growth_goals: str = ""
) -> str
```

**Parameters:**
- `scenario_description` (str): Description of the situation
- `personas` (str): Personas involved in the scenario
- `insecurity_triggers` (str): Known insecurity triggers present
- `growth_goals` (str): Relationship growth objectives

**Returns:** Formatted prompt string for LLM response generation

**Secure Response Framework:**

1. **Emotional Safety First:**
   - Validate emotions without necessarily agreeing with behaviors
   - Create space for vulnerability
   - Avoid criticism, contempt, or defensiveness

2. **Attunement and Understanding:**
   - Reflect what you hear (emotional and content)
   - Ask curious, non-judgmental questions
   - Show genuine interest in their experience

3. **Secure Base Behaviors:**
   - Provide consistent, reliable responses
   - Balance support with encouragement of autonomy
   - Offer comfort without rescuing

4. **Repair and Growth:**
   - Take responsibility for your part in misunderstandings
   - Focus on connection over being "right"
   - Model healthy vulnerability and boundary-setting

**Expected Output:**
1. Primary Response that embodies secure attachment principles
2. Alternative Responses for different attachment styles of receiver
3. Body Language/Tone suggestions to accompany words
4. What NOT to Say - responses that would increase insecurity
5. Follow-up Actions to reinforce security over time
6. Rationale explaining how this builds attachment security

**Usage Example:**
```python
async with Client(mcp_server) as client:
    prompt_result = await client.get_prompt("generate_secure_response", {
        "scenario_description": "Partner expressed fear of abandonment after you spent evening with friends",
        "personas": "Lila (secure), Alex (anxious)",
        "insecurity_triggers": "Time apart, seeing partner having fun without them",
        "growth_goals": "Build secure attachment, reduce anxiety"
    })

    llm_response = await llm.complete(prompt_result.messages[0].content)
    print(f"Recommended response: {llm_response}")
```

**Prompt Template (excerpt):**
```
You are an attachment-informed therapist helping develop secure,
emotionally attuned responses. Please generate responses that build
attachment security and emotional safety.

SCENARIO: {scenario_description}
PARTICIPANTS: {personas}
INSECURITY TRIGGERS PRESENT: {insecurity_triggers}
GROWTH GOALS: {growth_goals}

SECURE RESPONSE FRAMEWORK:

1. Emotional Safety First:
   - Validate emotions without necessarily agreeing with behaviors
   - Create space for vulnerability
...
```

---

## Data Management APIs

### Neo4jDataImporter

**Source:** `/home/donbr/lila-graph/lila-mcp/import_data.py:22-407`

Imports psychological intelligence data and schema into Neo4j.

```python
class Neo4jDataImporter:
    """Imports psychological intelligence data and schema into Neo4j for MCP standalone."""
```

#### Constructor

**Lines:** 25-32

```python
def __init__(self, uri: str, user: str, password: str, max_retries: int = 30):
    """Initialize Neo4j connection with retry logic."""
```

**Parameters:**
- `uri` (str): Neo4j connection URI (e.g., "bolt://localhost:7687")
- `user` (str): Database username
- `password` (str): Database password
- `max_retries` (int): Maximum connection retry attempts (default: 30)

**Usage Example:**
```python
from import_data import Neo4jDataImporter

importer = Neo4jDataImporter(
    uri="bolt://localhost:7687",
    user="neo4j",
    password="your_password",
    max_retries=30
)
```

#### Methods

##### `_connect_with_retry(self) -> None`

**Lines:** 34-49

Connects to Neo4j with exponential backoff retry logic for container startup.

**Retry Logic:**
- Attempts connection up to `max_retries` times
- Waits 2 seconds between attempts
- Raises exception if all retries exhausted

##### `close(self) -> None`

**Lines:** 51-54

Safely closes Neo4j driver connection.

##### `clear_database(self) -> None`

**Lines:** 56-61

Deletes all nodes and relationships from the database.

**Cypher Query:**
```cypher
MATCH (n) DETACH DELETE n
```

**Warning:** This is destructive and irreversible!

##### `load_schema(self, schema_path: Path) -> None`

**Lines:** 63-120

Loads schema constraints, indexes, and persona data from JSON file.

**Parameters:**
- `schema_path` (Path): Path to schema JSON file

**Creates:**
- Unique constraints on PersonaAgent.persona_id and PersonaAgent.name
- Unique constraints on Memory.memory_id
- Unique constraints on Goal.goal_id
- Indexes on attachment_style, memory_type, goal_type, relationship_type

**Constraint Examples:**
```cypher
CREATE CONSTRAINT persona_id_unique IF NOT EXISTS
FOR (p:PersonaAgent) REQUIRE p.persona_id IS UNIQUE

CREATE CONSTRAINT persona_name_unique IF NOT EXISTS
FOR (p:PersonaAgent) REQUIRE p.name IS UNIQUE
```

**Index Examples:**
```cypher
CREATE INDEX persona_attachment_style IF NOT EXISTS
FOR (p:PersonaAgent) ON (p.attachment_style)

CREATE INDEX relationship_type IF NOT EXISTS
FOR ()-[r:RELATIONSHIP]-() ON (r.relationship_type)
```

**Usage Example:**
```python
from pathlib import Path

importer = Neo4jDataImporter("bolt://localhost:7687", "neo4j", "password")
schema_path = Path("graphs/lila-graph-schema-v8.json")
importer.load_schema(schema_path)
```

##### `_load_family_graph_data(self, schema: dict, session) -> None`

**Lines:** 122-237

Loads personas and relationships from family_graph JSON structure.

**Schema Format Expected:**
```json
{
  "family_graph": {
    "nodes": [
      {
        "name": "Lila",
        "age": 28,
        "role": "AI Assistant",
        "description": "...",
        "attachment_style": "secure attachment",
        "behavioral_style": "Si",
        "journey_stage": "...",
        "current_challenge": "...",
        "knowsAbout": "..."
      }
    ],
    "edges": [
      {
        "from": "Lila",
        "to": "Alex",
        "type": "intimate partnership",
        "trust_level": 8.5,
        "strength": 7.8,
        "union_metric": 8.2
      }
    ]
  }
}
```

**Created Persona Properties:**
- persona_id, name, age, role, description
- attachment_style, journey_stage, behavioral_style
- current_challenge, knowsAbout
- Big Five personality traits (derived from behavioral_style)
- trust_level, communication_style
- created_at, updated_at timestamps

**Created Relationship Properties:**
- trust_level, intimacy_level, relationship_strength
- relationship_type, emotional_valence
- interaction_count (initialized to 0)
- created_at, updated_at timestamps

##### `_map_behavioral_to_bigfive(self, behavioral_style: str) -> dict`

**Lines:** 239-280

Maps DISC behavioral style to Big Five personality traits.

**Parameters:**
- `behavioral_style` (str): DISC style code (e.g., "Si", "Dc", "Cs")

**Returns:** Dictionary with Big Five traits (0.0-1.0 scale)

**DISC to Big Five Mapping:**

**D (Dominance):**
- Extraversion +0.2
- Agreeableness -0.1
- Openness +0.1

**I (Influence):**
- Extraversion +0.3
- Openness +0.2
- Agreeableness +0.1

**S (Steadiness):**
- Agreeableness +0.3
- Conscientiousness +0.2
- Neuroticism -0.1

**C (Conscientiousness):**
- Conscientiousness +0.3
- Openness +0.1
- Neuroticism +0.1

**Usage Example:**
```python
importer = Neo4jDataImporter("bolt://localhost:7687", "neo4j", "password")
traits = importer._map_behavioral_to_bigfive("Si")
print(traits)
# {'openness': 0.6, 'conscientiousness': 0.7, 'extraversion': 0.8,
#  'agreeableness': 0.8, 'neuroticism': 0.2}
```

##### `import_seed_data(self, seed_data_path: Path) -> None`

**Lines:** 282-310

Imports seed data from Cypher file.

**Parameters:**
- `seed_data_path` (Path): Path to .cypher file

**File Format:**
- Semicolon-separated Cypher statements
- Comments starting with // are ignored
- Each statement executed individually

**Usage Example:**
```python
importer = Neo4jDataImporter("bolt://localhost:7687", "neo4j", "password")
importer.import_seed_data(Path("seed_data.cypher"))
```

##### `create_default_personas(self) -> None`

**Lines:** 312-377

Creates default Lila and Alex personas if no data was imported.

**Default Personas:**

**Lila:**
- persona_id: "lila"
- age: 28, role: "AI Research Assistant"
- attachment_style: "secure"
- Personality: High openness (0.85), agreeableness (0.90), conscientiousness (0.80)

**Alex:**
- persona_id: "alex"
- age: 32, role: "Software Engineer"
- attachment_style: "secure"
- Personality: High conscientiousness (0.85), moderate extraversion (0.60)

**Default Relationship:**
- trust_level: 0.70
- intimacy_level: 0.60
- relationship_strength: 0.65
- interaction_count: 5
- relationship_type: "friendship"

##### `verify_import(self) -> bool`

**Lines:** 379-406

Verifies data was imported successfully by counting nodes.

**Returns:** True if personas exist, False otherwise

**Counts:**
- PersonaAgent nodes
- RELATIONSHIP edges
- Memory nodes
- Goal nodes

**Usage Example:**
```python
importer = Neo4jDataImporter("bolt://localhost:7687", "neo4j", "password")
importer.load_schema(Path("schema.json"))
success = importer.verify_import()
if success:
    print("Import successful!")
importer.close()
```

---

### Neo4jDataExporter

**Source:** `/home/donbr/lila-graph/lila-mcp/export_data.py:21-292`

Exports psychological intelligence data from Neo4j for MCP standalone seeding.

```python
class Neo4jDataExporter:
    """Exports psychological intelligence data from Neo4j for MCP standalone seeding."""
```

#### Constructor

**Lines:** 24-26

```python
def __init__(self, uri: str, user: str, password: str):
    """Initialize Neo4j connection."""
```

**Parameters:**
- `uri` (str): Neo4j connection URI
- `user` (str): Database username
- `password` (str): Database password

**Usage Example:**
```python
from export_data import Neo4jDataExporter

exporter = Neo4jDataExporter(
    uri="bolt://localhost:7687",
    user="neo4j",
    password="your_password"
)
```

#### Methods

##### `close(self) -> None`

**Lines:** 28-30

Closes Neo4j driver connection.

##### `export_personas(self) -> List[Dict[str, Any]]`

**Lines:** 32-62

Exports all PersonaAgent nodes with their psychological profiles.

**Returns:** List of persona dictionaries

**Cypher Query:**
```cypher
MATCH (p:PersonaAgent)
RETURN p.persona_id as persona_id,
       p.name as name,
       p.age as age,
       p.role as role,
       p.description as description,
       p.attachment_style as attachment_style,
       p.openness as openness,
       p.conscientiousness as conscientiousness,
       p.extraversion as extraversion,
       p.agreeableness as agreeableness,
       p.neuroticism as neuroticism,
       p.trust_level as trust_level,
       p.relationship_history as relationship_history,
       p.communication_style as communication_style,
       p.created_at as created_at,
       p.updated_at as updated_at
```

##### `export_relationships(self) -> List[Dict[str, Any]]`

**Lines:** 64-89

Exports all relationships between personas.

**Returns:** List of relationship dictionaries

**Cypher Query:**
```cypher
MATCH (p1:PersonaAgent)-[r:RELATIONSHIP]->(p2:PersonaAgent)
RETURN p1.persona_id as persona1_id,
       p2.persona_id as persona2_id,
       r.trust_level as trust_level,
       r.intimacy_level as intimacy_level,
       r.relationship_strength as relationship_strength,
       r.interaction_count as interaction_count,
       r.last_interaction as last_interaction,
       r.relationship_type as relationship_type,
       r.emotional_valence as emotional_valence,
       r.created_at as created_at,
       r.updated_at as updated_at
```

##### `export_memories(self) -> List[Dict[str, Any]]`

**Lines:** 91-113

Exports memory nodes associated with personas.

**Returns:** List of memory dictionaries

**Cypher Query:**
```cypher
MATCH (p:PersonaAgent)-[:HAS_MEMORY]->(m:Memory)
RETURN p.persona_id as persona_id,
       m.memory_id as memory_id,
       m.content as content,
       m.memory_type as memory_type,
       m.importance_score as importance_score,
       m.emotional_valence as emotional_valence,
       m.participants as participants,
       m.created_at as created_at
```

##### `export_goals(self) -> List[Dict[str, Any]]`

**Lines:** 115-139

Exports goal nodes associated with personas.

**Returns:** List of goal dictionaries

**Cypher Query:**
```cypher
MATCH (p:PersonaAgent)-[:HAS_GOAL]->(g:Goal)
RETURN p.persona_id as persona_id,
       g.goal_id as goal_id,
       g.goal_type as goal_type,
       g.description as description,
       g.progress as progress,
       g.target_persona as target_persona,
       g.priority as priority,
       g.status as status,
       g.created_at as created_at,
       g.updated_at as updated_at
```

##### `generate_cypher_script(self, personas, relationships, memories, goals) -> str`

**Lines:** 141-242

Generates Cypher script for importing data into MCP standalone.

**Parameters:**
- `personas` (List[Dict]): Persona data
- `relationships` (List[Dict]): Relationship data
- `memories` (List[Dict]): Memory data
- `goals` (List[Dict]): Goal data

**Returns:** Complete Cypher script as string

**Output Format:**
```cypher
// Lila Psychological Intelligence System - Seed Data for MCP Standalone
// Generated from main system export

// Clear existing data
MATCH (n) DETACH DELETE n;

// Create Personas
CREATE (:PersonaAgent {persona_id: 'lila', name: 'Lila', ...});
CREATE (:PersonaAgent {persona_id: 'alex', name: 'Alex', ...});

// Create Relationships
MATCH (p1:PersonaAgent {persona_id: 'lila'}), (p2:PersonaAgent {persona_id: 'alex'})
CREATE (p1)-[:RELATIONSHIP {trust_level: 8.5, ...}]->(p2);

// Create Memories
MATCH (p:PersonaAgent {persona_id: 'lila'})
CREATE (p)-[:HAS_MEMORY]->(:Memory {memory_id: 'mem_001', ...});

// Create Goals
MATCH (p:PersonaAgent {persona_id: 'lila'})
CREATE (p)-[:HAS_GOAL]->(:Goal {goal_id: 'goal_001', ...});
```

**Usage Example:**
```python
exporter = Neo4jDataExporter("bolt://localhost:7687", "neo4j", "password")

personas = exporter.export_personas()
relationships = exporter.export_relationships()
memories = exporter.export_memories()
goals = exporter.export_goals()

script = exporter.generate_cypher_script(personas, relationships, memories, goals)

with open("seed_data.cypher", "w") as f:
    f.write(script)

exporter.close()
```

---

## Configuration

### Environment Variables

**Source:** `/home/donbr/lila-graph/lila-mcp/.env.example`

Complete list of environment variables supported by the system.

#### Neo4j Database Configuration

```bash
# Neo4j connection settings
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password_here
DISABLE_NEO4J=false

# Connection timeout and retry settings
NEO4J_TIMEOUT=30
NEO4J_MAX_RETRY_TIME=60
```

**Usage:**
- `NEO4J_URI`: Connection string (bolt://, neo4j://, or neo4j+s://)
- `NEO4J_USER`: Database username (default: neo4j)
- `NEO4J_PASSWORD`: Required for authentication
- `DISABLE_NEO4J`: Set to "true" to run without Neo4j (mock mode)
- `NEO4J_TIMEOUT`: Query timeout in seconds
- `NEO4J_MAX_RETRY_TIME`: Maximum retry duration for connection

#### LLM Configuration

```bash
# LLM model settings
DEFAULT_LLM_MODEL=gpt-4
LLM_TEMPERATURE=0.7

# API Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

**Supported Models:**
- OpenAI: gpt-4, gpt-4-turbo, gpt-3.5-turbo
- Anthropic: claude-3-opus, claude-3-sonnet, claude-3-haiku

#### FastMCP and Telemetry

```bash
# Telemetry configuration
ENABLE_LOGFIRE_TELEMETRY=false
LOGFIRE_PROJECT_NAME=lila-mcp
LOGFIRE_TOKEN=your_token_here

# FastMCP development settings
FASTMCP_AUTO_RELOAD=true
FASTMCP_LOG_LEVEL=INFO
```

**Logfire Integration:**
- Provides observability for MCP server
- Requires Logfire account and token
- Recommended for production deployments

#### Environment and Logging

```bash
# Environment
ENV=development
LOG_LEVEL=INFO
LOG_FORMAT=json

# Enhanced logging
LOG_FILE_ENABLED=true
LOG_FILE_PATH=logs/lila-mcp.log
LOG_ROTATION_SIZE=10485760  # 10MB
LOG_RETENTION_DAYS=30
```

**Log Levels:** DEBUG, INFO, WARNING, ERROR, CRITICAL

**Log Formats:** json, text

#### MCP Server Configuration

```bash
# Server settings
MCP_HOST=0.0.0.0
MCP_PORT=8766

# MCP Inspector (development)
MCP_INSPECTOR_HOST=localhost
MCP_INSPECTOR_PORT=6274

# HTTP transport
MCP_TRANSPORT=sse
MCP_REQUEST_TIMEOUT=30
MCP_MAX_CONNECTIONS=100
```

**Transport Options:**
- `sse`: Server-Sent Events (recommended)
- `stdio`: Standard input/output

#### Development and Performance

```bash
# Migration phase tracking
MIGRATION_PHASE=phase1_minimal_viable

# Development mode
DEBUG_MODE=false
ENABLE_DEV_FEATURES=false
ENABLE_PERFORMANCE_MONITORING=false

# Resource limits
MAX_CONCURRENT_REQUESTS=50
MEMORY_LIMIT_MB=512
REQUEST_TIMEOUT_SECONDS=30
```

#### Security Configuration

```bash
# Security settings
ENABLE_AUTH=false
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS_PER_MINUTE=60

# TLS/SSL (production)
TLS_ENABLED=false
TLS_CERT_PATH=/path/to/cert.pem
TLS_KEY_PATH=/path/to/key.pem
```

#### Data and Storage

```bash
# Local storage paths
DATA_DIR=./data
CACHE_DIR=./cache
TEMP_DIR=./temp

# Database fallback
ENABLE_MEMORY_FALLBACK=true
MEMORY_DB_SIZE_LIMIT=100000000  # 100MB
```

#### Deployment Configuration

```bash
# Container and deployment
CONTAINER_MODE=false
HEALTH_CHECK_ENABLED=true
HEALTH_CHECK_INTERVAL=30

# Service discovery
SERVICE_NAME=lila-mcp-server
SERVICE_VERSION=1.0.0
SERVICE_ENVIRONMENT=development
```

---

### Configuration Files

#### pyproject.toml

**Source:** `/home/donbr/lila-graph/lila-mcp/pyproject.toml`

Python project configuration and dependencies.

**Key Sections:**

**Project Metadata:**
```toml
[project]
name = "lila-mcp-standalone"
version = "1.0.0"
description = "Standalone Lila MCP Server - Minimal psychological relationship intelligence"
requires-python = ">=3.12"
```

**Core Dependencies:**
```toml
dependencies = [
    "fastmcp>=2.12.3",        # Core MCP framework
    "neo4j>=5.15.0",          # Database connectivity
    "openai>=1.30.0",         # LLM integration
    "anthropic>=0.25.0",      # LLM integration
    "pydantic>=2.6.0",        # Data validation
    "python-dotenv>=1.0.0",   # Configuration
    "logfire>=0.28.0",        # Observability
]
```

**Development Dependencies:**
```toml
[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",
    "black>=24.0.0",
    "ruff>=0.3.0",
]
```

**Tool Configuration:**
```toml
[tool.black]
line-length = 120
target-version = ['py312']

[tool.ruff]
line-length = 120
target-version = "py312"

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

#### fastmcp.json

**Source:** `/home/donbr/lila-graph/lila-mcp/fastmcp.json`

FastMCP server deployment configuration.

**Complete Configuration:**
```json
{
  "$schema": "https://gofastmcp.com/public/schemas/fastmcp.json/v1.json",

  "source": {
    "type": "filesystem",
    "path": "lila_mcp_server.py",
    "entrypoint": "mcp"
  },

  "environment": {
    "type": "uv",
    "python": ">=3.12",
    "dependencies": [
      "fastmcp>=2.12.3",
      "neo4j>=5.15.0",
      "pydantic>=2.6.0",
      "pydantic-settings>=2.2.0",
      "python-dotenv>=1.0.0",
      "openai>=1.30.0",
      "anthropic>=0.25.0",
      "httpx>=0.27.0",
      "aiohttp>=3.9.0",
      "logfire>=0.28.0",
      "click>=8.1.0",
      "asyncio-mqtt>=0.16.0"
    ]
  },

  "deployment": {
    "transport": "http",
    "host": "0.0.0.0",
    "port": 8766,
    "log_level": "INFO"
  }
}
```

**Configuration Options:**

**source:**
- `type`: "filesystem" for local Python files
- `path`: Python file containing MCP server
- `entrypoint`: Variable name of FastMCP app instance

**environment:**
- `type`: "uv" for UV package manager
- `python`: Python version requirement
- `dependencies`: Runtime dependencies

**deployment:**
- `transport`: "http" or "stdio"
- `host`: Server bind address
- `port`: Server port
- `log_level`: Logging verbosity

---

## Usage Patterns and Best Practices

### Basic Usage

#### Starting the Server

**Development Mode with FastMCP Inspector:**
```bash
# Using fastmcp dev command
fastmcp dev lila_mcp_server.py

# Access Inspector at:
# http://localhost:6274/
```

**Production Mode:**
```bash
# Direct Python execution
python lila_mcp_server.py

# Or with uvicorn
uvicorn lila_mcp_server:mcp --host 0.0.0.0 --port 8766
```

#### Connecting as a Client

**In-Memory Connection (Testing):**
```python
from fastmcp import Client
from lila_mcp_server import LilaMCPServer

server = LilaMCPServer()

async with Client(server.app) as client:
    # Client is now connected
    resources = await client.list_resources()
    print(f"Available resources: {len(resources)}")
```

**HTTP Connection (Production):**
```python
from fastmcp import Client

async with Client("http://localhost:8766/") as client:
    # Test connectivity
    await client.ping()

    # List available capabilities
    resources = await client.list_resources()
    tools = await client.list_tools()
    prompts = await client.list_prompts()
```

#### Reading Resources

**Get All Personas:**
```python
async with Client(mcp_server) as client:
    personas_json = await client.read_resource("neo4j://personas/all")
    personas = json.loads(personas_json)

    for persona in personas['personas']:
        print(f"{persona['name']}: {persona['attachment_style']} attachment")
```

**Get Specific Relationship:**
```python
async with Client(mcp_server) as client:
    rel_json = await client.read_resource("neo4j://relationships/lila/alex")
    rel = json.loads(rel_json)

    metrics = rel['relationship']
    print(f"Trust: {metrics['trust_level']}/10")
    print(f"Intimacy: {metrics['intimacy_level']}/10")
    print(f"Strength: {metrics['relationship_strength']}/10")
```

#### Calling Tools

**Update Relationship After Interaction:**
```python
async with Client(mcp_server) as client:
    # Record the interaction
    interaction = await client.call_tool("record_interaction", {
        "sender_id": "lila",
        "recipient_id": "alex",
        "content": "Thank you for your support today!",
        "emotional_valence": 0.8,
        "relationship_impact": 0.3
    })

    # Update relationship metrics
    update = await client.call_tool("update_relationship_metrics", {
        "persona1_id": "lila",
        "persona2_id": "alex",
        "trust_delta": 0.3,
        "intimacy_delta": 0.2,
        "strength_delta": 0.25
    })

    result = json.loads(update.content[0].text)
    print(f"New trust level: {result['updated_relationship']['trust_level']}")
```

**Analyze Compatibility:**
```python
async with Client(mcp_server) as client:
    analysis = await client.call_tool("analyze_persona_compatibility", {
        "persona1_id": "lila",
        "persona2_id": "alex",
        "relationship_type": "romantic"
    })

    result = json.loads(analysis.content[0].text)
    compat = result['compatibility_analysis']

    print(f"Compatibility: {compat['compatibility_level']}")
    print(f"Analysis: {compat['analysis']}")
    for rec in compat['recommendations']:
        print(f"  - {rec}")
```

#### Using Prompts with LLM

**Assess Attachment Style:**
```python
from openai import AsyncOpenAI

async with Client(mcp_server) as client:
    # Get the prompt
    prompt = await client.get_prompt("assess_attachment_style", {
        "persona_id": "alex",
        "observation_period": "past 6 months",
        "behavioral_examples": "Withdraws during conflict, prefers independence, difficulty sharing emotions"
    })

    # Send to LLM
    llm = AsyncOpenAI()
    response = await llm.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt.messages[0].content}]
    )

    print(response.choices[0].message.content)
```

**Analyze Emotional Climate:**
```python
async with Client(mcp_server) as client:
    conversation = """
    Alex: I feel like you're always busy and don't have time for me.
    Lila: I'm sorry you feel that way. Can we talk about what you need?
    Alex: I just need to feel like I matter to you.
    Lila: You absolutely matter. Let me show you that better.
    """

    prompt = await client.get_prompt("analyze_emotional_climate", {
        "conversation_text": conversation,
        "participants": "Alex, Lila"
    })

    llm = AsyncOpenAI()
    analysis = await llm.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt.messages[0].content}]
    )

    print(analysis.choices[0].message.content)
```

---

### Error Handling

#### Handling Database Unavailability

**Pattern:**
```python
async with Client(mcp_server) as client:
    try:
        personas = await client.read_resource("neo4j://personas/all")
        data = json.loads(personas)

        if "error" in data:
            print(f"Database error: {data['error']}")
            # Fall back to mock data or cached data
        else:
            # Process normal data
            process_personas(data['personas'])

    except Exception as e:
        print(f"Connection error: {e}")
        # Handle connection failure
```

#### Handling Missing Resources

**Pattern:**
```python
async with Client(mcp_server) as client:
    persona_id = "unknown_persona"

    try:
        persona_json = await client.read_resource(f"neo4j://personas/{persona_id}")
        persona = json.loads(persona_json)

        if "error" in persona:
            print(f"Persona not found: {persona['error']}")
            return None

        return persona['persona']

    except Exception as e:
        print(f"Error fetching persona: {e}")
        return None
```

#### Handling Tool Failures

**Pattern:**
```python
async with Client(mcp_server) as client:
    try:
        result = await client.call_tool("update_relationship_metrics", {
            "persona1_id": "lila",
            "persona2_id": "nonexistent",
            "trust_delta": 0.5
        })

        data = json.loads(result.content[0].text)

        if "error" in data:
            print(f"Tool error: {data['error']}")
            # Log error, notify user, or retry
            return False

        if data.get("success"):
            print("Update successful!")
            return True

    except Exception as e:
        print(f"Unexpected error: {e}")
        # Log for debugging
        import traceback
        traceback.print_exc()
        return False
```

#### Retry Logic for Transient Errors

**Pattern:**
```python
import asyncio
from typing import Optional

async def call_tool_with_retry(
    client: Client,
    tool_name: str,
    params: dict,
    max_retries: int = 3,
    delay: float = 1.0
) -> Optional[dict]:
    """Call MCP tool with exponential backoff retry."""

    for attempt in range(max_retries):
        try:
            result = await client.call_tool(tool_name, params)
            data = json.loads(result.content[0].text)

            if "error" not in data:
                return data

            print(f"Attempt {attempt + 1} failed: {data['error']}")

        except Exception as e:
            print(f"Attempt {attempt + 1} error: {e}")

        if attempt < max_retries - 1:
            await asyncio.sleep(delay * (2 ** attempt))

    print(f"All {max_retries} attempts failed")
    return None

# Usage
async with Client(mcp_server) as client:
    result = await call_tool_with_retry(client, "update_relationship_metrics", {
        "persona1_id": "lila",
        "persona2_id": "alex",
        "trust_delta": 0.5
    })
```

---

### Performance Optimization

#### Batch Resource Reads

**Anti-Pattern (Slow):**
```python
# DON'T: Make individual requests for each persona
personas = ["lila", "alex", "jordan", "taylor"]
persona_data = []

for persona_id in personas:
    data = await client.read_resource(f"neo4j://personas/{persona_id}")
    persona_data.append(json.loads(data))
```

**Better Pattern:**
```python
# DO: Use single request for all personas
all_personas = await client.read_resource("neo4j://personas/all")
data = json.loads(all_personas)

# Filter in memory
target_ids = {"lila", "alex", "jordan", "taylor"}
filtered = [p for p in data['personas'] if p['id'] in target_ids]
```

#### Connection Pooling

**Pattern:**
```python
from contextlib import asynccontextmanager

class MCPClientPool:
    """Maintain connection pool for MCP clients."""

    def __init__(self, server_url: str, pool_size: int = 5):
        self.server_url = server_url
        self.pool_size = pool_size
        self.clients = []

    async def initialize(self):
        """Create connection pool."""
        for _ in range(self.pool_size):
            client = Client(self.server_url)
            await client.__aenter__()
            self.clients.append(client)

    async def close(self):
        """Close all connections."""
        for client in self.clients:
            await client.__aexit__(None, None, None)

    @asynccontextmanager
    async def get_client(self):
        """Get client from pool."""
        if not self.clients:
            raise RuntimeError("Pool not initialized")

        client = self.clients.pop()
        try:
            yield client
        finally:
            self.clients.append(client)

# Usage
pool = MCPClientPool("http://localhost:8766/", pool_size=10)
await pool.initialize()

async with pool.get_client() as client:
    personas = await client.read_resource("neo4j://personas/all")

await pool.close()
```

#### Caching Frequent Reads

**Pattern:**
```python
from datetime import datetime, timedelta
from typing import Optional

class MCPResourceCache:
    """Simple time-based cache for MCP resources."""

    def __init__(self, ttl_seconds: int = 60):
        self.cache = {}
        self.ttl = timedelta(seconds=ttl_seconds)

    def get(self, key: str) -> Optional[dict]:
        """Get cached value if not expired."""
        if key in self.cache:
            value, timestamp = self.cache[key]
            if datetime.now() - timestamp < self.ttl:
                return value
        return None

    def set(self, key: str, value: dict):
        """Cache value with current timestamp."""
        self.cache[key] = (value, datetime.now())

# Usage
cache = MCPResourceCache(ttl_seconds=30)

async def get_personas_cached(client: Client) -> dict:
    """Get personas with caching."""
    cached = cache.get("personas_all")
    if cached:
        return cached

    personas_json = await client.read_resource("neo4j://personas/all")
    personas = json.loads(personas_json)
    cache.set("personas_all", personas)
    return personas
```

#### Parallel Tool Calls

**Pattern:**
```python
import asyncio

async def update_multiple_relationships(
    client: Client,
    updates: list[dict]
) -> list[dict]:
    """Update multiple relationships in parallel."""

    tasks = [
        client.call_tool("update_relationship_metrics", update)
        for update in updates
    ]

    results = await asyncio.gather(*tasks, return_exceptions=True)

    processed = []
    for result in results:
        if isinstance(result, Exception):
            print(f"Error: {result}")
            processed.append({"error": str(result)})
        else:
            processed.append(json.loads(result.content[0].text))

    return processed

# Usage
async with Client(mcp_server) as client:
    updates = [
        {"persona1_id": "lila", "persona2_id": "alex", "trust_delta": 0.3},
        {"persona1_id": "lila", "persona2_id": "jordan", "trust_delta": 0.2},
        {"persona1_id": "alex", "persona2_id": "taylor", "intimacy_delta": 0.4},
    ]

    results = await update_multiple_relationships(client, updates)
    print(f"Updated {len(results)} relationships")
```

---

## Code Examples

### Complete Example: Interaction Recording and Analysis

```python
"""
Complete example: Record interaction, update metrics, and analyze emotional climate.
"""
import asyncio
import json
from fastmcp import Client
from openai import AsyncOpenAI

async def process_interaction(
    client: Client,
    llm: AsyncOpenAI,
    sender_id: str,
    recipient_id: str,
    message: str,
    emotional_valence: float
):
    """Process a complete interaction with analysis."""

    print(f"\n{'='*60}")
    print(f"Processing interaction: {sender_id} → {recipient_id}")
    print(f"Message: {message}")
    print(f"{'='*60}\n")

    # Step 1: Record the interaction
    print("Step 1: Recording interaction...")
    interaction = await client.call_tool("record_interaction", {
        "sender_id": sender_id,
        "recipient_id": recipient_id,
        "content": message,
        "emotional_valence": emotional_valence,
        "relationship_impact": abs(emotional_valence) * 0.5
    })

    interaction_data = json.loads(interaction.content[0].text)
    print(f"✓ Recorded: {interaction_data['interaction_id']}")

    # Step 2: Update relationship metrics
    print("\nStep 2: Updating relationship metrics...")
    trust_delta = emotional_valence * 0.3
    intimacy_delta = emotional_valence * 0.2
    strength_delta = emotional_valence * 0.25

    update = await client.call_tool("update_relationship_metrics", {
        "persona1_id": sender_id,
        "persona2_id": recipient_id,
        "trust_delta": trust_delta,
        "intimacy_delta": intimacy_delta,
        "strength_delta": strength_delta
    })

    update_data = json.loads(update.content[0].text)
    rel = update_data['updated_relationship']
    print(f"✓ Trust: {rel['trust_level']:.2f}/10 ({rel['changes']['trust_delta']:+.2f})")
    print(f"✓ Intimacy: {rel['intimacy_level']:.2f}/10 ({rel['changes']['intimacy_delta']:+.2f})")
    print(f"✓ Strength: {rel['relationship_strength']:.2f}/10 ({rel['changes']['strength_delta']:+.2f})")

    # Step 3: Analyze emotional climate
    print("\nStep 3: Analyzing emotional climate...")
    prompt = await client.get_prompt("analyze_emotional_climate", {
        "conversation_text": f"{sender_id}: {message}",
        "participants": f"{sender_id}, {recipient_id}"
    })

    analysis = await llm.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt.messages[0].content}],
        max_tokens=500
    )

    print(f"✓ Emotional analysis:\n{analysis.choices[0].message.content[:300]}...\n")

    # Step 4: Get current relationship status
    print("Step 4: Current relationship status...")
    rel_status = await client.read_resource(f"neo4j://relationships/{sender_id}/{recipient_id}")
    rel_data = json.loads(rel_status)

    relationship = rel_data['relationship']
    print(f"✓ Type: {relationship['relationship_type']}")
    print(f"✓ Total interactions: {relationship['interaction_count']}")
    print(f"✓ Emotional valence: {relationship['emotional_valence']:.2f}")

    return {
        "interaction_id": interaction_data['interaction_id'],
        "metrics": rel,
        "relationship": relationship
    }

async def main():
    """Main example execution."""

    # Initialize clients
    mcp_client = Client("http://localhost:8766/")
    llm_client = AsyncOpenAI()

    async with mcp_client as client:
        # Process a positive interaction
        result1 = await process_interaction(
            client,
            llm_client,
            sender_id="lila",
            recipient_id="alex",
            message="Thank you so much for being there for me today. Your support means everything.",
            emotional_valence=0.9
        )

        # Process another interaction
        result2 = await process_interaction(
            client,
            llm_client,
            sender_id="alex",
            recipient_id="lila",
            message="I'm always here for you. We're in this together.",
            emotional_valence=0.8
        )

        print(f"\n{'='*60}")
        print("Summary:")
        print(f"{'='*60}")
        print(f"Processed {2} interactions")
        print(f"Final trust level: {result2['metrics']['trust_level']:.2f}/10")
        print(f"Total interactions: {result2['relationship']['interaction_count']}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Complete Example: Compatibility Analysis and Strategy Selection

```python
"""
Complete example: Analyze compatibility and select interaction strategies.
"""
import asyncio
import json
from fastmcp import Client
from typing import Dict

async def analyze_and_strategize(
    client: Client,
    persona1_id: str,
    persona2_id: str,
    relationship_type: str = "romantic"
) -> Dict:
    """Analyze compatibility and select optimal strategies."""

    print(f"\n{'='*60}")
    print(f"Analyzing: {persona1_id} ↔ {persona2_id}")
    print(f"Relationship type: {relationship_type}")
    print(f"{'='*60}\n")

    # Step 1: Get persona details
    print("Step 1: Loading persona profiles...")
    persona1_json = await client.read_resource(f"neo4j://personas/{persona1_id}")
    persona2_json = await client.read_resource(f"neo4j://personas/{persona2_id}")

    persona1 = json.loads(persona1_json)['persona']
    persona2 = json.loads(persona2_json)['persona']

    print(f"✓ {persona1['name']}: {persona1['attachment_style']} attachment")
    print(f"✓ {persona2['name']}: {persona2['attachment_style']} attachment")

    # Step 2: Analyze compatibility
    print("\nStep 2: Analyzing compatibility...")
    compat_result = await client.call_tool("analyze_persona_compatibility", {
        "persona1_id": persona1_id,
        "persona2_id": persona2_id,
        "relationship_type": relationship_type
    })

    compat = json.loads(compat_result.content[0].text)['compatibility_analysis']

    print(f"✓ Compatibility level: {compat['compatibility_level']}")
    print(f"✓ Analysis: {compat['analysis']}")
    print("\nRecommendations:")
    for rec in compat['recommendations']:
        print(f"  • {rec}")

    # Step 3: Select strategies for each persona
    print("\nStep 3: Selecting interaction strategies...")

    # Strategy for persona1
    strategy1_result = await client.call_tool("autonomous_strategy_selection", {
        "persona_id": persona1_id,
        "conversation_context": f"Building {relationship_type} relationship with {persona2['name']}",
        "active_goals": "build trust, increase intimacy",
        "attachment_style": persona1['attachment_style']
    })

    strategy1 = json.loads(strategy1_result.content[0].text)['strategy_selection']

    # Strategy for persona2
    strategy2_result = await client.call_tool("autonomous_strategy_selection", {
        "persona_id": persona2_id,
        "conversation_context": f"Building {relationship_type} relationship with {persona1['name']}",
        "active_goals": "build trust, increase intimacy",
        "attachment_style": persona2['attachment_style']
    })

    strategy2 = json.loads(strategy2_result.content[0].text)['strategy_selection']

    print(f"✓ {persona1['name']}'s strategy: {strategy1['selected_strategy']}")
    print(f"  Reasoning: {strategy1['reasoning']}")
    print(f"\n✓ {persona2['name']}'s strategy: {strategy2['selected_strategy']}")
    print(f"  Reasoning: {strategy2['reasoning']}")

    # Step 4: Generate contextual responses
    print("\nStep 4: Generating contextual responses...")

    response1_result = await client.call_tool("generate_contextual_response", {
        "persona_id": persona1_id,
        "context": f"First deep conversation with {persona2['name']}",
        "goals": "build trust, show vulnerability"
    })

    response1 = json.loads(response1_result.content[0].text)['contextual_response']

    print(f"\n{persona1['name']}'s response:")
    print(f'  "{response1["response"]}"')
    print(f"  Strategy: {response1['strategy_used']}")

    return {
        "compatibility": compat,
        "strategies": {
            persona1_id: strategy1,
            persona2_id: strategy2
        },
        "personas": {
            persona1_id: persona1,
            persona2_id: persona2
        }
    }

async def main():
    """Main example execution."""

    async with Client("http://localhost:8766/") as client:
        # Analyze secure-anxious pairing
        result = await analyze_and_strategize(
            client,
            persona1_id="lila",
            persona2_id="alex",
            relationship_type="romantic"
        )

        print(f"\n{'='*60}")
        print("Analysis Complete!")
        print(f"{'='*60}")
        print(f"Compatibility: {result['compatibility']['compatibility_level']}")
        print(f"Strategies selected for both personas")

if __name__ == "__main__":
    asyncio.run(main())
```

### Complete Example: Data Import and Validation

```python
"""
Complete example: Import data and validate Neo4j setup.
"""
import asyncio
from pathlib import Path
from import_data import Neo4jDataImporter
from fastmcp import Client

async def setup_and_validate():
    """Import data and validate MCP server."""

    print(f"\n{'='*60}")
    print("Lila MCP Data Import and Validation")
    print(f"{'='*60}\n")

    # Step 1: Import data
    print("Step 1: Importing data to Neo4j...")
    importer = Neo4jDataImporter(
        uri="bolt://localhost:7687",
        user="neo4j",
        password="passw0rd",
        max_retries=30
    )

    try:
        # Load schema
        schema_path = Path("graphs/lila-graph-schema-v8.json")
        if schema_path.exists():
            importer.load_schema(schema_path)
        else:
            print("⚠️  Schema file not found, creating default personas...")
            importer.create_default_personas()

        # Verify import
        success = importer.verify_import()
        if success:
            print("✓ Data import successful!")
        else:
            print("⚠️  No data imported")
            return False

    finally:
        importer.close()

    # Step 2: Validate MCP server
    print("\nStep 2: Validating MCP server...")

    async with Client("http://localhost:8766/") as client:
        # Test connectivity
        await client.ping()
        print("✓ Server is reachable")

        # Test resources
        personas = await client.read_resource("neo4j://personas/all")
        personas_data = json.loads(personas)

        if "error" in personas_data:
            print(f"❌ Error: {personas_data['error']}")
            return False

        print(f"✓ Found {personas_data['count']} personas")

        # Test relationships
        rels = await client.read_resource("neo4j://relationships/all")
        rels_data = json.loads(rels)
        print(f"✓ Found {rels_data['count']} relationships")

        # Test tools
        tools = await client.list_tools()
        print(f"✓ {len(tools)} tools available")

        # Test prompts
        prompts = await client.list_prompts()
        print(f"✓ {len(prompts)} prompts available")

    print(f"\n{'='*60}")
    print("✅ Setup and validation complete!")
    print(f"{'='*60}\n")

    return True

if __name__ == "__main__":
    success = asyncio.run(setup_and_validate())
    exit(0 if success else 1)
```

---

## Summary

This API reference provides complete documentation for:

1. **Core Classes**: LilaMCPServer, SimpleLilaMCPServer, Neo4jDataImporter, Neo4jDataExporter
2. **MCP Resources**: 5 read-only endpoints for personas, relationships, and interactions
3. **MCP Tools**: 6 action-oriented endpoints for updates and analysis
4. **MCP Prompts**: 3 templated prompts for LLM-based psychological assessments
5. **Configuration**: Environment variables and configuration files
6. **Best Practices**: Error handling, performance optimization, and usage patterns
7. **Complete Examples**: Working code for common use cases

All APIs are production-ready and integrated with Neo4j for persistent psychological relationship modeling.

**Quick Links:**
- Main Server: `/home/donbr/lila-graph/lila-mcp/lila_mcp_server.py`
- Simple Server: `/home/donbr/lila-graph/lila-mcp/simple_lila_mcp_server.py`
- Data Import: `/home/donbr/lila-graph/lila-mcp/import_data.py`
- Data Export: `/home/donbr/lila-graph/lila-mcp/export_data.py`
- Configuration: `/home/donbr/lila-graph/lila-mcp/.env.example`
- Project Config: `/home/donbr/lila-graph/lila-mcp/pyproject.toml`
- FastMCP Config: `/home/donbr/lila-graph/lila-mcp/fastmcp.json`
