"""FastMCP server for Lila psychological relationship modeling system.

Connects to Neo4j database for real-time psychological intelligence data.
Provides comprehensive MCP interface for psychological analysis and relationship modeling.
"""

import asyncio
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from pathlib import Path

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Neo4j imports
from neo4j import GraphDatabase

# FastMCP imports
from fastmcp import FastMCP
from fastmcp.resources import Resource
from fastmcp.tools import Tool
from fastmcp.prompts import Prompt

# Enable FastMCP debug logging (from FastMCP documentation)
logging.basicConfig(level=logging.DEBUG)
logging.getLogger("fastmcp.server").setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)

class SimpleLilaMCPServer:
    """MCP server exposing Lila's psychological relationship data and tools with Neo4j integration."""

    def __init__(self):
        """Initialize the MCP server with Neo4j database connection."""
        self.app = FastMCP("lila-psychological-relationships")
        self.driver: Optional[GraphDatabase] = None

        # Initialize mock data for fallback scenarios
        self.mock_personas = {
            "lila": {
                "id": "lila",
                "name": "Lila",
                "age": 28,
                "role": "Psychological Intelligence Agent",
                "attachment_style": "secure",
                "personality": {
                    "openness": 0.8,
                    "conscientiousness": 0.75,
                    "extraversion": 0.65,
                    "agreeableness": 0.85,
                    "neuroticism": 0.3
                }
            },
            "don": {
                "id": "don",
                "name": "Don",
                "age": 45,
                "role": "Software Developer",
                "attachment_style": "anxious",
                "personality": {
                    "openness": 0.7,
                    "conscientiousness": 0.8,
                    "extraversion": 0.4,
                    "agreeableness": 0.7,
                    "neuroticism": 0.6
                }
            }
        }

        self.mock_relationships = {
            ("lila", "don"): {
                "trust_level": 7.5,
                "intimacy_level": 6.8,
                "relationship_strength": 7.2,
                "last_updated": datetime.now().isoformat()
            }
        }

        self.mock_interactions = [
            {
                "id": "int_001",
                "sender_id": "lila",
                "recipient_id": "don",
                "content": "How are you feeling about our project collaboration?",
                "emotional_valence": 0.7,
                "relationship_impact": 0.3,
                "timestamp": datetime.now().isoformat()
            }
        ]

        # Initialize Neo4j connection
        self._setup_database()

        # Register MCP endpoints
        self._register_resources()
        self._register_tools()
        self._register_prompts()

    def _setup_database(self):
        """Initialize Neo4j database connection."""
        try:
            neo4j_uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
            neo4j_user = os.getenv("NEO4J_USER", "neo4j")
            neo4j_password = os.getenv("NEO4J_PASSWORD", "passw0rd")

            self.driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

            # Test the connection
            with self.driver.session() as session:
                session.run("RETURN 1")

            logger.info(f"Connected to Neo4j database at {neo4j_uri}")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            self.driver = None

    def close(self):
        """Close Neo4j connection."""
        if self.driver:
            self.driver.close()

    def _register_resources(self):
        """Register Neo4j and psychological data resources."""

        @self.app.resource("neo4j://personas/all")
        def get_all_personas() -> str:
            """Retrieve all personas with their psychological profiles."""
            if not self.driver:
                return '{"error": "Neo4j database not available"}'

            try:
                with self.driver.session() as session:
                    result = session.run("""
                        MATCH (p:PersonaAgent)
                        RETURN p.persona_id as persona_id, p.name as name, p.age as age, p.role as role,
                               p.attachment_style as attachment_style,
                               p.openness as openness, p.conscientiousness as conscientiousness,
                               p.extraversion as extraversion, p.agreeableness as agreeableness, p.neuroticism as neuroticism
                        ORDER BY p.name
                    """)

                    personas = []
                    for record in result:
                        persona = {
                            "id": record["persona_id"],
                            "name": record["name"],
                            "age": record["age"],
                            "role": record["role"],
                            "attachment_style": record["attachment_style"],
                            "personality": {
                                "openness": record["openness"] or 0.5,
                                "conscientiousness": record["conscientiousness"] or 0.5,
                                "extraversion": record["extraversion"] or 0.5,
                                "agreeableness": record["agreeableness"] or 0.5,
                                "neuroticism": record["neuroticism"] or 0.5
                            }
                        }
                        personas.append(persona)

                    return f'''{{
                "personas": {personas},
                "count": {len(personas)},
                "last_updated": "{datetime.now().isoformat()}"
            }}'''
            except Exception as e:
                logger.error(f"Error querying personas: {e}")
                return f'{{"error": "Error retrieving personas: {str(e)}"}}'

        @self.app.resource("neo4j://personas/{persona_id}")
        def get_persona_by_id(persona_id: str) -> str:
            """Retrieve specific persona by ID with full psychological profile."""
            if not self.driver:
                return '{"error": "Neo4j database not available"}'

            try:
                with self.driver.session() as session:
                    result = session.run("""
                        MATCH (p:PersonaAgent {persona_id: $persona_id})
                        RETURN p.persona_id as persona_id, p.name as name, p.age as age, p.role as role,
                               p.description as description, p.attachment_style as attachment_style,
                               p.openness as openness, p.conscientiousness as conscientiousness,
                               p.extraversion as extraversion, p.agreeableness as agreeableness, p.neuroticism as neuroticism,
                               p.trust_level as trust_level, p.communication_style as communication_style
                    """, persona_id=persona_id)

                    record = result.single()
                    if not record:
                        return f'{{"error": "Persona {persona_id} not found"}}'

                    persona = {
                        "id": record["persona_id"],
                        "name": record["name"],
                        "age": record["age"],
                        "role": record["role"],
                        "description": record["description"],
                        "attachment_style": record["attachment_style"],
                        "personality": {
                            "openness": record["openness"] or 0.5,
                            "conscientiousness": record["conscientiousness"] or 0.5,
                            "extraversion": record["extraversion"] or 0.5,
                            "agreeableness": record["agreeableness"] or 0.5,
                            "neuroticism": record["neuroticism"] or 0.5
                        },
                        "trust_level": record["trust_level"] or 0.5,
                        "communication_style": record["communication_style"]
                    }

                    return f'''{{
                "persona": {persona},
                "last_updated": "{datetime.now().isoformat()}"
            }}'''
            except Exception as e:
                logger.error(f"Error querying persona {persona_id}: {e}")
                return f'{{"error": "Error retrieving persona: {str(e)}"}}'

        @self.app.resource("neo4j://relationships/all")
        def get_all_relationships() -> str:
            """Retrieve all relationship data with psychological metrics."""
            relationships = []
            for (p1, p2), metrics in self.mock_relationships.items():
                relationships.append({
                    "persona1_id": p1,
                    "persona2_id": p2,
                    **metrics
                })

            return f'''{{
                "relationships": {relationships},
                "count": {len(relationships)},
                "average_trust": 7.5,
                "average_intimacy": 6.8
            }}'''

        @self.app.resource("neo4j://relationships/{persona1_id}/{persona2_id}")
        def get_relationship_by_personas(persona1_id: str, persona2_id: str) -> str:
            """Retrieve specific relationship metrics between two personas."""
            key = (persona1_id, persona2_id)
            reverse_key = (persona2_id, persona1_id)

            metrics = self.mock_relationships.get(key) or self.mock_relationships.get(reverse_key)
            if not metrics:
                return f'{{"error": "Relationship between {persona1_id} and {persona2_id} not found"}}'

            return f'''{{
                "relationship": {{
                    "persona1_id": "{persona1_id}",
                    "persona2_id": "{persona2_id}",
                    "trust_level": {metrics["trust_level"]},
                    "intimacy_level": {metrics["intimacy_level"]},
                    "relationship_strength": {metrics["relationship_strength"]},
                    "last_updated": "{metrics["last_updated"]}"
                }}
            }}'''

        @self.app.resource("neo4j://interactions/recent/{count}")
        def get_recent_interactions(count: str = "10") -> str:
            """Retrieve recent interactions with psychological analysis."""
            limit = min(int(count), len(self.mock_interactions))
            recent = self.mock_interactions[:limit]

            return f'''{{
                "interactions": {recent},
                "count": {len(recent)},
                "total_available": {len(self.mock_interactions)}
            }}'''

        @self.app.resource("neo4j://emotional_climate/current")
        def get_current_emotional_climate() -> str:
            """Assess current emotional climate across all relationships."""
            return '''{
                "overall_climate": {
                    "safety_level": 8.2,
                    "positivity": 7.6,
                    "authenticity": 7.9,
                    "growth_potential": 8.1
                },
                "risk_factors": [
                    "Mild anxiety patterns in 'don' persona",
                    "Need for reassurance seeking behaviors"
                ],
                "strengths": [
                    "Strong secure attachment from 'lila'",
                    "High openness and conscientiousness levels",
                    "Active communication patterns"
                ]
            }'''

        @self.app.resource("neo4j://attachment_styles/analysis")
        def get_attachment_analysis() -> str:
            """Analyze attachment style compatibility and dynamics."""
            return '''{
                "compatibility_matrix": {
                    "lila_don": {
                        "overall_score": 7.8,
                        "attachment_compatibility": 8.2,
                        "challenges": ["Anxious-secure dynamic requires patience"],
                        "strengths": ["Secure partner can provide stability"]
                    }
                },
                "recommendations": [
                    "Consistent reassurance for anxious attachment",
                    "Gradual trust building exercises",
                    "Open communication about emotional needs"
                ]
            }'''

        @self.app.resource("neo4j://goals/active")
        def get_active_goals() -> str:
            """Retrieve all active relationship goals across personas."""
            return '''{
                "active_goals": [
                    {
                        "persona_id": "lila",
                        "goal_type": "emotional",
                        "description": "Support partner through career transition",
                        "progress": 0.6,
                        "strategies": ["Active listening", "Emotional validation"]
                    },
                    {
                        "persona_id": "don",
                        "goal_type": "trust",
                        "description": "Open up about vulnerabilities",
                        "progress": 0.4,
                        "strategies": ["Gradual disclosure", "Safe space creation"]
                    }
                ],
                "completion_rate": 0.5
            }'''

        @self.app.resource("neo4j://psychological_insights/trends")
        def get_psychological_trends() -> str:
            """Track psychological development trends over time."""
            return '''{
                "trends": {
                    "trust_evolution": {
                        "direction": "increasing",
                        "rate": 0.2,
                        "stability": "high"
                    },
                    "intimacy_development": {
                        "direction": "steady",
                        "rate": 0.1,
                        "stability": "medium"
                    },
                    "attachment_security": {
                        "direction": "improving",
                        "rate": 0.15,
                        "stability": "high"
                    }
                },
                "predictions": {
                    "next_month": "Continued trust building with minor setbacks",
                    "next_quarter": "Significant intimacy breakthroughs expected"
                }
            }'''

    def _register_tools(self):
        """Register MCP tools for system interaction."""

        @self.app.tool()
        async def update_relationship_metrics(
            persona1_id: str,
            persona2_id: str,
            trust_delta: float = 0.0,
            intimacy_delta: float = 0.0,
            strength_delta: float = 0.0
        ) -> str:
            """Update relationship metrics between two personas."""
            key = (persona1_id, persona2_id)
            reverse_key = (persona2_id, persona1_id)

            # Find existing relationship
            if key in self.mock_relationships:
                metrics = self.mock_relationships[key]
            elif reverse_key in self.mock_relationships:
                metrics = self.mock_relationships[reverse_key]
                key = reverse_key
            else:
                # Create new relationship
                metrics = {"trust_level": 5.0, "intimacy_level": 5.0, "relationship_strength": 5.0}
                self.mock_relationships[key] = metrics

            # Update metrics
            metrics["trust_level"] = max(0, min(10, metrics["trust_level"] + trust_delta))
            metrics["intimacy_level"] = max(0, min(10, metrics["intimacy_level"] + intimacy_delta))
            metrics["relationship_strength"] = max(0, min(10, metrics["relationship_strength"] + strength_delta))
            metrics["last_updated"] = datetime.now().isoformat()

            return f'''{{
                "success": true,
                "updated_relationship": {{
                    "participants": ["{persona1_id}", "{persona2_id}"],
                    "trust_level": {metrics["trust_level"]:.2f},
                    "intimacy_level": {metrics["intimacy_level"]:.2f},
                    "relationship_strength": {metrics["relationship_strength"]:.2f}
                }}
            }}'''

        @self.app.tool()
        async def record_interaction(
            sender_id: str,
            recipient_id: str,
            content: str,
            emotional_valence: float = 0.0,
            relationship_impact: float = 0.0
        ) -> str:
            """Record an interaction between two personas with psychological analysis."""
            interaction_id = f"int_{len(self.mock_interactions) + 1:03d}"

            new_interaction = {
                "id": interaction_id,
                "sender_id": sender_id,
                "recipient_id": recipient_id,
                "content": content,
                "emotional_valence": emotional_valence,
                "relationship_impact": relationship_impact,
                "timestamp": datetime.now().isoformat()
            }

            self.mock_interactions.insert(0, new_interaction)  # Add to front

            return f'''{{
                "success": true,
                "interaction_id": "{interaction_id}",
                "recorded": {{
                    "sender_id": "{sender_id}",
                    "recipient_id": "{recipient_id}",
                    "content_length": {len(content)},
                    "emotional_valence": {emotional_valence},
                    "relationship_impact": {relationship_impact}
                }}
            }}'''

        @self.app.tool()
        async def analyze_persona_compatibility(
            persona1_id: str,
            persona2_id: str,
            relationship_type: str = "romantic"
        ) -> str:
            """Assess relationship potential between two personas based on attachment styles."""
            if persona1_id not in self.mock_personas or persona2_id not in self.mock_personas:
                return f'{{"error": "One or both personas not found"}}'

            persona1 = self.mock_personas[persona1_id]
            persona2 = self.mock_personas[persona2_id]

            # Mock compatibility analysis
            compatibility_score = 0.75  # Based on secure-anxious pairing

            return f'''{{
                "compatibility_analysis": {{
                    "overall_score": {compatibility_score:.2f},
                    "attachment_compatibility": 0.82,
                    "personality_compatibility": 0.73,
                    "goal_alignment": 0.68,
                    "communication_style": 0.79,
                    "recommendations": [
                        "Focus on consistent reassurance for anxious partner",
                        "Leverage secure partner's stability",
                        "Practice open emotional communication"
                    ],
                    "challenges": [
                        "Different emotional processing speeds",
                        "Reassurance needs vs independence balance"
                    ],
                    "strengths": [
                        "High mutual respect and understanding",
                        "Complementary personality traits",
                        "Shared values around growth"
                    ]
                }}
            }}'''

        @self.app.tool()
        async def autonomous_strategy_selection(
            persona_id: str,
            conversation_context: str = "",
            goals: str = "",
            constraints: str = ""
        ) -> str:
            """Select optimal autonomous strategy for persona based on current context."""
            if persona_id not in self.mock_personas:
                return f'{{"error": "Persona {persona_id} not found"}}'

            persona = self.mock_personas[persona_id]
            attachment_style = persona["attachment_style"]

            # Strategy selection based on attachment style
            if attachment_style == "secure":
                strategy = {
                    "strategy_name": "balanced_connection",
                    "confidence": 0.85,
                    "reasoning": "Secure attachment allows for balanced approach to connection and autonomy",
                    "approach": "Direct, empathetic communication with clear boundaries",
                    "tactics": ["Active listening", "Emotional validation", "Gentle guidance"],
                    "expected_outcome": "Strengthened trust and deeper connection"
                }
            else:  # anxious
                strategy = {
                    "strategy_name": "reassurance_seeking",
                    "confidence": 0.78,
                    "reasoning": "Anxious attachment requires extra reassurance and validation",
                    "approach": "Seek explicit confirmation and emotional support",
                    "tactics": ["Request reassurance", "Share vulnerabilities", "Seek validation"],
                    "expected_outcome": "Reduced anxiety and increased security"
                }

            return f'''{{
                "strategy_selection": {{
                    "selected_strategy": "{strategy["strategy_name"]}",
                    "confidence": {strategy["confidence"]:.2f},
                    "reasoning": "{strategy["reasoning"]}",
                    "implementation": {{
                        "approach": "{strategy["approach"]}",
                        "tactics": {strategy["tactics"]},
                        "expected_outcome": "{strategy["expected_outcome"]}"
                    }},
                    "attachment_basis": "{attachment_style}",
                    "personality_factors": {persona["personality"]}
                }}
            }}'''

        @self.app.tool()
        async def assess_goal_progress(
            persona_id: str,
            goals: str = "",
            timeframe: str = "recent"
        ) -> str:
            """Assess progress towards relationship goals for a persona."""
            if persona_id not in self.mock_personas:
                return f'{{"error": "Persona {persona_id} not found"}}'

            # Mock goal progress assessment
            progress_data = {
                "overall_progress": 0.65,
                "goal_details": [
                    {"goal": "trust building", "progress": 0.7, "status": "on_track"},
                    {"goal": "emotional intimacy", "progress": 0.6, "status": "needs_attention"}
                ],
                "achievements": [
                    "Successful vulnerable conversation last week",
                    "Consistent daily check-ins established"
                ],
                "recommendations": [
                    "Continue vulnerability practices",
                    "Schedule weekly relationship reviews"
                ],
                "next_steps": [
                    "Plan deeper emotional sharing session",
                    "Address remaining trust concerns"
                ]
            }

            return f'''{{
                "goal_assessment": {{
                    "persona_id": "{persona_id}",
                    "timeframe": "{timeframe}",
                    "overall_progress": {progress_data["overall_progress"]:.2f},
                    "goal_details": {progress_data["goal_details"]},
                    "achievements": {progress_data["achievements"]},
                    "recommendations": {progress_data["recommendations"]},
                    "next_steps": {progress_data["next_steps"]}
                }}
            }}'''

        @self.app.tool()
        async def generate_contextual_response(
            persona_id: str,
            context: str,
            goals: str = "",
            constraints: str = ""
        ) -> str:
            """Generate psychologically authentic response for a persona in a given context."""
            if persona_id not in self.mock_personas:
                return f'{{"error": "Persona {persona_id} not found"}}'

            persona = self.mock_personas[persona_id]

            # Generate mock response based on persona characteristics
            if persona["attachment_style"] == "secure":
                response_text = "I appreciate you sharing that with me. How can we work together on this?"
                attachment_influence = "Secure attachment promotes direct, supportive communication"
            else:  # anxious
                response_text = "I'm feeling a bit uncertain about this. Can we talk through it together?"
                attachment_influence = "Anxious attachment seeks reassurance and connection"

            return f'''{{
                "generated_response": {{
                    "persona_id": "{persona_id}",
                    "response_text": "{response_text}",
                    "psychological_basis": {{
                        "attachment_influence": "{attachment_influence}",
                        "personality_expression": {persona["personality"]},
                        "goal_alignment": 0.8,
                        "emotional_tone": 0.7
                    }},
                    "confidence": 0.82,
                    "alternative_approaches": [
                        "More direct communication style",
                        "Greater emotional vulnerability",
                        "Focus on problem-solving approach"
                    ]
                }}
            }}'''

        @self.app.tool()
        async def commit_relationship_state(persona1_id: str, persona2_id: str) -> str:
            """Explicitly commit current relationship state to ensure persistence."""
            # In the simplified version, data is already "persisted" in memory
            return f'''{{
                "success": true,
                "committed": {{
                    "participants": ["{persona1_id}", "{persona2_id}"],
                    "timestamp": "{datetime.now().isoformat()}"
                }}
            }}'''

        @self.app.tool()
        async def finalize_demo_session() -> str:
            """Finalize all relationship states at end of demo to ensure persistence."""
            committed_count = len(self.mock_relationships)
            return f'''{{
                "success": true,
                "finalized": {{
                    "committed_relationships": {committed_count},
                    "timestamp": "{datetime.now().isoformat()}"
                }}
            }}'''

    def _register_prompts(self):
        """Register MCP prompts for psychological analysis."""

        @self.app.prompt()
        def assess_attachment_style(
            persona_id: str,
            observation_period: str = "recent",
            behavioral_examples: str = ""
        ) -> str:
            """Determine persona's attachment style from behavioral observations."""
            return f"""# Attachment Style Assessment for Persona {persona_id}

## Assessment Framework

Based on observed behaviors during {observation_period} period:
{behavioral_examples}

### Analyze for Attachment Patterns:

**Secure Attachment Indicators:**
- Comfortable with intimacy and autonomy
- Effective communication during conflict
- Consistent emotional availability
- Trusting and emotionally responsive
- Balances independence with connection

**Anxious Attachment Patterns:**
- Seeks frequent reassurance
- Fear of abandonment or rejection
- Heightened emotional reactivity
- May be clingy or demanding
- Hypervigilant to relationship threats

**Avoidant Attachment Behaviors:**
- Values independence over connection
- Difficulty with emotional intimacy
- Withdraws during conflict or stress
- Minimizes emotional expression
- Self-reliant to a fault

**Disorganized Attachment Signs:**
- Inconsistent relationship patterns
- Conflicting needs for closeness/distance
- Chaotic or unpredictable responses
- Unresolved trauma responses
- Difficulty with emotional regulation

## Assessment Criteria:

1. **Primary attachment style** (with confidence level 1-10)
2. **Secondary influences** from other styles
3. **Supporting behavioral evidence**
4. **Contextual factors** affecting presentation
5. **Relationship implications** and patterns
6. **Recommendations** for healthy relationship development

## Provide Detailed Analysis:

- How does this attachment style manifest in their relationships?
- What triggers their attachment system?
- What are their core emotional needs?
- How do they handle relationship stress?
- What interventions would support secure functioning?

Remember: Attachment styles exist on a continuum and can vary by relationship context."""

        @self.app.prompt()
        def analyze_emotional_climate(
            conversation_text: str = "",
            interaction_id: str = "",
            participants: str = ""
        ) -> str:
            """Evaluate conversation emotional dynamics and safety levels."""
            return f"""# Emotional Climate Analysis

## Conversation Data
**Interaction ID:** {interaction_id}
**Participants:** {participants}
**Conversation Text:**
{conversation_text}

## Analysis Framework

### Emotional Safety Indicators:
1. **Validation and Empathy**
   - Are emotions acknowledged and validated?
   - Is empathy expressed genuinely?
   - Are feelings treated as legitimate?

2. **Communication Quality**
   - Active listening demonstrated?
   - Non-defensive responses?
   - Constructive vs. destructive patterns?

3. **Power Dynamics**
   - Balance of speaking/listening?
   - Mutual respect evident?
   - Control or manipulation present?

4. **Conflict Management**
   - How is disagreement handled?
   - Focus on issues vs. personal attacks?
   - Repair attempts made?

### Emotional Climate Assessment:

**Rate the emotional climate (1-10 scale):**
- **Safety Level:** How emotionally safe is this interaction?
- **Positivity:** Overall emotional valence
- **Authenticity:** Genuineness of emotional expression
- **Growth Potential:** Opportunity for deepening connection

### Provide Analysis:

1. **Overall emotional climate assessment**
2. **Key patterns identified** (positive and concerning)
3. **Attachment dynamics** at play
4. **Communication strengths** to reinforce
5. **Areas needing attention** for relationship health
6. **Specific recommendations** for improvement
7. **Warning signs** to monitor

Focus on actionable insights that support healthy relationship development and emotional well-being."""

        @self.app.prompt()
        def generate_secure_response(
            scenario_description: str,
            personas: str,
            insecurity_triggers: str = "",
            growth_goals: str = ""
        ) -> str:
            """Create attachment-security-building responses for various scenarios."""
            return f"""# Secure Attachment Response Generation

## Scenario Context
**Situation:** {scenario_description}
**Personas Involved:** {personas}
**Insecurity Triggers:** {insecurity_triggers}
**Growth Goals:** {growth_goals}

## Secure Response Framework

### Core Principles for Secure Responses:

1. **Emotional Attunement**
   - Acknowledge and validate emotions
   - Demonstrate understanding without judgment
   - Mirror appropriate emotional tone

2. **Safe Communication**
   - Use "I" statements for personal feelings
   - Avoid blame, criticism, or defensiveness
   - Focus on collaboration vs. competition

3. **Consistent Availability**
   - Show reliable emotional presence
   - Maintain boundaries while being supportive
   - Balance autonomy with connection

4. **Growth-Oriented**
   - Encourage mutual development
   - Support individual goals within relationship
   - Model healthy vulnerability

### Generate Secure Responses:

**For each persona involved, create responses that:**

1. **Address the immediate situation** with emotional intelligence
2. **Neutralize insecurity triggers** through reassurance and validation
3. **Advance growth goals** while maintaining safety
4. **Model secure attachment behaviors**
5. **Strengthen relationship foundations**

### Response Guidelines:

- **Tone:** Warm, authentic, non-defensive
- **Content:** Validating, solution-focused, future-oriented
- **Emotional Quality:** Stable, reassuring, genuinely caring
- **Attachment Message:** "You matter, you're safe, we're in this together"

### Provide:

1. **Primary response options** for each persona
2. **Rationale** for why these responses build security
3. **Alternative approaches** for different comfort levels
4. **Expected outcomes** on relationship dynamics
5. **Follow-up strategies** to reinforce secure patterns

Focus on responses that create lasting positive change in relationship patterns while honoring each persona's authentic emotional expression."""

# FastMCP CLI discovery
mcp = SimpleLilaMCPServer().app

if __name__ == "__main__":
    # For testing purposes
    print("Simple Lila MCP Server ready for FastMCP Inspector")
    print("Run with: fastmcp dev simple_lila_mcp_server.py")