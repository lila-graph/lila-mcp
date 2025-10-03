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

logger = logging.getLogger(__name__)

class LilaMCPServer:
    """MCP server exposing Lila's psychological relationship data and tools with Neo4j integration."""

    def __init__(self):
        """Initialize the MCP server with Neo4j database connection."""
        self.app = FastMCP("lila-psychological-relationships")
        self.driver: Optional[GraphDatabase] = None

        # Initialize Neo4j connection
        self._setup_database()

        # Register MCP endpoints
        self._register_resources()
        self._register_tools()
        self._register_prompts()
        self._register_health_check()

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
            if not self.driver:
                return '{"error": "Neo4j database not available"}'

            try:
                with self.driver.session() as session:
                    result = session.run("""
                        MATCH (p1:PersonaAgent)-[r:RELATIONSHIP]->(p2:PersonaAgent)
                        RETURN p1.persona_id as persona1_id, p1.name as persona1_name,
                               p2.persona_id as persona2_id, p2.name as persona2_name,
                               r.trust_level as trust_level, r.intimacy_level as intimacy_level,
                               r.relationship_strength as relationship_strength,
                               r.interaction_count as interaction_count,
                               r.relationship_type as relationship_type,
                               r.emotional_valence as emotional_valence
                        ORDER BY r.relationship_strength DESC
                    """)

                    relationships = []
                    for record in result:
                        relationship = {
                            "persona1_id": record["persona1_id"],
                            "persona1_name": record["persona1_name"],
                            "persona2_id": record["persona2_id"],
                            "persona2_name": record["persona2_name"],
                            "trust_level": record["trust_level"] or 5.0,
                            "intimacy_level": record["intimacy_level"] or 5.0,
                            "relationship_strength": record["relationship_strength"] or 5.0,
                            "interaction_count": record["interaction_count"] or 0,
                            "relationship_type": record["relationship_type"] or "unknown",
                            "emotional_valence": record["emotional_valence"] or 0.0
                        }
                        relationships.append(relationship)

                    return f'''{{
                "relationships": {relationships},
                "count": {len(relationships)},
                "last_updated": "{datetime.now().isoformat()}"
            }}'''
            except Exception as e:
                logger.error(f"Error querying relationships: {e}")
                return f'{{"error": "Error retrieving relationships: {str(e)}"}}'

        @self.app.resource("neo4j://relationships/{persona1_id}/{persona2_id}")
        def get_relationship_by_personas(persona1_id: str, persona2_id: str) -> str:
            """Retrieve specific relationship metrics between two personas."""
            if not self.driver:
                return '{"error": "Neo4j database not available"}'

            try:
                with self.driver.session() as session:
                    result = session.run("""
                        MATCH (p1:PersonaAgent {persona_id: $persona1_id})-[r:RELATIONSHIP]-(p2:PersonaAgent {persona_id: $persona2_id})
                        RETURN p1.name as name1, p2.name as name2,
                               r.trust_level as trust_level, r.intimacy_level as intimacy_level,
                               r.relationship_strength as relationship_strength,
                               r.interaction_count as interaction_count,
                               r.relationship_type as relationship_type,
                               r.emotional_valence as emotional_valence,
                               r.created_at as created_at, r.updated_at as updated_at
                        LIMIT 1
                    """, persona1_id=persona1_id, persona2_id=persona2_id)

                    record = result.single()
                    if not record:
                        return f'{{"error": "No relationship found between {persona1_id} and {persona2_id}"}}'

                    relationship = {
                        "persona1_id": persona1_id,
                        "persona1_name": record["name1"],
                        "persona2_id": persona2_id,
                        "persona2_name": record["name2"],
                        "trust_level": record["trust_level"] or 5.0,
                        "intimacy_level": record["intimacy_level"] or 5.0,
                        "relationship_strength": record["relationship_strength"] or 5.0,
                        "interaction_count": record["interaction_count"] or 0,
                        "relationship_type": record["relationship_type"] or "unknown",
                        "emotional_valence": record["emotional_valence"] or 0.0,
                        "created_at": str(record["created_at"]) if record["created_at"] else None,
                        "updated_at": str(record["updated_at"]) if record["updated_at"] else None
                    }

                    return f'''{{
                "relationship": {relationship},
                "last_updated": "{datetime.now().isoformat()}"
            }}'''
            except Exception as e:
                logger.error(f"Error querying relationship: {e}")
                return f'{{"error": "Error retrieving relationship: {str(e)}"}}'

        @self.app.resource("neo4j://interactions/recent/{count}")
        def get_recent_interactions(count: str = "10") -> str:
            """Retrieve recent interactions with psychological analysis."""
            if not self.driver:
                return '{"error": "Neo4j database not available"}'

            try:
                count_int = min(int(count), 50)  # Limit to 50 max
                with self.driver.session() as session:
                    # Note: Using a simplified query since we may not have full Interaction nodes yet
                    # This can be expanded once the interaction schema is implemented
                    result = session.run("""
                        MATCH (p1:PersonaAgent)-[r:RELATIONSHIP]-(p2:PersonaAgent)
                        RETURN p1.name as from_name, p2.name as to_name,
                               r.last_interaction as last_interaction,
                               r.relationship_type as relationship_type,
                               r.emotional_valence as emotional_valence
                        ORDER BY r.updated_at DESC
                        LIMIT $count
                    """, count=count_int)

                    interactions = []
                    for i, record in enumerate(result):
                        interaction = {
                            "id": f"interaction_{i+1}",
                            "from": record["from_name"],
                            "to": record["to_name"],
                            "content": f"[Relationship interaction of type: {record['relationship_type']}]",
                            "emotional_valence": record["emotional_valence"] or 0.0,
                            "timestamp": str(record["last_interaction"]) if record["last_interaction"] else datetime.now().isoformat()
                        }
                        interactions.append(interaction)

                    return f'''{{
                "interactions": {interactions},
                "count": {len(interactions)},
                "last_updated": "{datetime.now().isoformat()}"
            }}'''
            except Exception as e:
                logger.error(f"Error querying interactions: {e}")
                return f'{{"error": "Error retrieving interactions: {str(e)}"}}'

    def _register_tools(self):
        """Register persona and relationship management tools."""

        @self.app.tool()
        async def update_relationship_metrics(
            persona1_id: str,
            persona2_id: str,
            trust_delta: float = 0.0,
            intimacy_delta: float = 0.0,
            strength_delta: float = 0.0
        ) -> str:
            """Update relationship metrics between two personas."""
            if not self.driver:
                return '{"error": "Neo4j database not available"}'

            try:
                with self.driver.session() as session:
                    # Update relationship metrics with bounds checking
                    result = session.run("""
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
                    """, persona1_id=persona1_id, persona2_id=persona2_id,
                        trust_delta=trust_delta, intimacy_delta=intimacy_delta, strength_delta=strength_delta)

                    record = result.single()
                    if not record:
                        return f'{{"error": "No relationship found between {persona1_id} and {persona2_id}"}}'

                    return f'''{{
                "success": true,
                "updated_relationship": {{
                    "participants": ["{persona1_id}", "{persona2_id}"],
                    "participant_names": ["{record['name1']}", "{record['name2']}"],
                    "trust_level": {record['trust']:.2f},
                    "intimacy_level": {record['intimacy']:.2f},
                    "relationship_strength": {record['strength']:.2f},
                    "changes": {{
                        "trust_delta": {trust_delta:+.2f},
                        "intimacy_delta": {intimacy_delta:+.2f},
                        "strength_delta": {strength_delta:+.2f}
                    }}
                }}
            }}'''
            except Exception as e:
                logger.error(f"Error updating relationship metrics: {e}")
                return f'{{"error": "Error updating relationship metrics: {str(e)}"}}'

        @self.app.tool()
        async def record_interaction(
            sender_id: str,
            recipient_id: str,
            content: str,
            emotional_valence: float = 0.0,
            relationship_impact: float = 0.0
        ) -> str:
            """Record an interaction between two personas with psychological analysis."""
            if not self.driver:
                return '{"error": "Neo4j database not available"}'

            try:
                interaction_id = f"int_{sender_id}_{recipient_id}_{int(datetime.now().timestamp() * 1000)}"

                with self.driver.session() as session:
                    # Update the relationship's last interaction and interaction count
                    session.run("""
                        MATCH (p1:PersonaAgent {persona_id: $sender_id})-[r:RELATIONSHIP]-(p2:PersonaAgent {persona_id: $recipient_id})
                        SET r.last_interaction = datetime(),
                            r.interaction_count = COALESCE(r.interaction_count, 0) + 1,
                            r.emotional_valence = ($emotional_valence + COALESCE(r.emotional_valence, 0.0)) / 2
                    """, sender_id=sender_id, recipient_id=recipient_id, emotional_valence=emotional_valence)

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
            except Exception as e:
                logger.error(f"Error recording interaction: {e}")
                return f'{{"error": "Error recording interaction: {str(e)}"}}'

        @self.app.tool()
        async def analyze_persona_compatibility(
            persona1_id: str,
            persona2_id: str,
            relationship_type: str = "romantic"
        ) -> str:
            """Assess relationship potential between two personas based on attachment styles."""
            if not self.driver:
                return '{"error": "Neo4j database not available"}'

            try:
                with self.driver.session() as session:
                    result = session.run("""
                        MATCH (p1:PersonaAgent {persona_id: $persona1_id}), (p2:PersonaAgent {persona_id: $persona2_id})
                        RETURN p1.name as name1, p1.attachment_style as style1,
                               p2.name as name2, p2.attachment_style as style2
                    """, persona1_id=persona1_id, persona2_id=persona2_id)

                    record = result.single()
                    if not record:
                        return f'{{"error": "Could not find both personas: {persona1_id}, {persona2_id}"}}'

                    # Compatibility analysis based on attachment styles
                    compatibility_matrix = {
                        ("secure", "secure"): ("High", "Both partners provide stability and emotional availability"),
                        ("secure", "anxious"): ("Good", "Secure partner can provide reassurance to anxious partner"),
                        ("secure", "avoidant"): ("Moderate", "Secure partner may help avoidant partner open up gradually"),
                        ("anxious", "anxious"): ("Challenging", "Both partners may escalate emotional intensity"),
                        ("anxious", "avoidant"): ("Difficult", "Classic pursue-withdraw dynamic may develop"),
                        ("avoidant", "avoidant"): ("Low", "Both partners may avoid emotional intimacy"),
                    }

                    style1 = record["style1"]
                    style2 = record["style2"]
                    compatibility = compatibility_matrix.get((style1, style2)) or compatibility_matrix.get((style2, style1)) or ("Unknown", "Attachment style combination not recognized")

                    return f'''{{
                "compatibility_analysis": {{
                    "persona1": {{
                        "id": "{persona1_id}",
                        "name": "{record['name1']}",
                        "attachment_style": "{style1}"
                    }},
                    "persona2": {{
                        "id": "{persona2_id}",
                        "name": "{record['name2']}",
                        "attachment_style": "{style2}"
                    }},
                    "relationship_type": "{relationship_type}",
                    "compatibility_level": "{compatibility[0]}",
                    "analysis": "{compatibility[1]}",
                    "recommendations": [
                        "Focus on understanding each other's attachment needs",
                        "Practice clear, consistent communication",
                        "Respect differences in emotional expression and intimacy pace"
                    ]
                }}
            }}'''
            except Exception as e:
                logger.error(f"Error analyzing compatibility: {e}")
                return f'{{"error": "Error analyzing compatibility: {str(e)}"}}'

        @self.app.tool()
        async def autonomous_strategy_selection(
            persona_id: str,
            conversation_context: str = "",
            situation_assessment: str = "",
            active_goals: str = "",
            attachment_style: str = "secure"
        ) -> str:
            """AI-driven strategy selection based on attachment theory and context analysis."""
            try:
                # Strategy mapping based on attachment style
                attachment_strategies = {
                    "secure": ["emotional_bonding", "vulnerable_disclosure", "supportive_listening", "trust_building"],
                    "anxious": ["reassurance_seeking", "emotional_validation", "secure_bonding", "safety_creation"],
                    "avoidant": ["autonomous_connection", "thoughtful_presence", "respectful_distance", "gradual_opening"],
                    "exploratory": ["growth_oriented_support", "playful_engagement", "curious_exploration", "authentic_expression"]
                }

                available_strategies = attachment_strategies.get(attachment_style, attachment_strategies["secure"])

                # Context-based strategy selection
                context_lower = conversation_context.lower()
                if "first" in context_lower or "new" in context_lower:
                    if attachment_style == "anxious":
                        selected_strategy = "reassurance_seeking"
                    elif attachment_style == "avoidant":
                        selected_strategy = "thoughtful_presence"
                    else:
                        selected_strategy = "emotional_bonding"
                elif "deep" in context_lower or "intimate" in context_lower:
                    selected_strategy = "vulnerable_disclosure" if attachment_style != "avoidant" else "gradual_opening"
                elif "trust" in active_goals.lower():
                    selected_strategy = "trust_building"
                elif "vulnerability" in active_goals.lower():
                    selected_strategy = "vulnerable_disclosure"
                else:
                    selected_strategy = available_strategies[0]

                return f'''{{
                "strategy_selection": {{
                    "persona_id": "{persona_id}",
                    "selected_strategy": "{selected_strategy}",
                    "attachment_style": "{attachment_style}",
                    "context": "{conversation_context}",
                    "available_strategies": {available_strategies},
                    "reasoning": "Selected based on attachment style and context analysis"
                }}
            }}'''
            except Exception as e:
                logger.error(f"Error in strategy selection: {e}")
                return f'{{"error": "Error in strategy selection: {str(e)}"}}'

        @self.app.tool()
        async def assess_goal_progress(
            persona_id: str,
            goals: str = "",
            recent_interactions: str = ""
        ) -> str:
            """Assess progress toward relationship goals based on recent interactions."""
            try:
                goal_list = [g.strip() for g in goals.split(",") if g.strip()]

                progress_results = []
                for goal in goal_list:
                    if "trust" in goal.lower():
                        progress = 0.15
                    elif "intimacy" in goal.lower():
                        progress = 0.08
                    elif "vulnerability" in goal.lower():
                        progress = 0.12
                    else:
                        progress = 0.10

                    progress_results.append({
                        "goal": goal,
                        "progress": progress,
                        "assessment": f"Progress toward {goal} is steady"
                    })

                return f'''{{
                "goal_progress": {{
                    "persona_id": "{persona_id}",
                    "assessed_goals": {progress_results},
                    "overall_progress": {sum(r['progress'] for r in progress_results) / len(progress_results) if progress_results else 0.05:.3f},
                    "assessment_timestamp": "{datetime.now().isoformat()}"
                }}
            }}'''
            except Exception as e:
                logger.error(f"Error assessing goal progress: {e}")
                return f'{{"error": "Error assessing goal progress: {str(e)}"}}'

        @self.app.tool()
        async def generate_contextual_response(
            persona_id: str,
            context: str,
            goals: str = "",
            constraints: str = ""
        ) -> str:
            """Generate psychologically authentic response for a persona in a given context."""
            if not self.driver:
                return '{"error": "Neo4j database not available"}'

            try:
                # Get persona information from database
                with self.driver.session() as session:
                    result = session.run("""
                        MATCH (p:PersonaAgent {persona_id: $persona_id})
                        RETURN p.name as name, p.attachment_style as attachment_style,
                               p.communication_style as communication_style
                    """, persona_id=persona_id)

                    record = result.single()
                    if not record:
                        return f'{{"error": "Persona {persona_id} not found"}}'

                    # Generate response based on attachment style
                    attachment_style = record["attachment_style"]
                    name = record["name"]

                    if attachment_style == "secure":
                        response_text = "I appreciate you sharing that with me. How can we work together on this?"
                        strategy = "supportive_listening"
                    elif attachment_style == "anxious":
                        response_text = "Thank you for telling me this. I want to make sure I understand how you're feeling."
                        strategy = "emotional_validation"
                    elif attachment_style == "avoidant":
                        response_text = "I hear what you're saying. Let me think about that for a moment."
                        strategy = "thoughtful_presence"
                    else:
                        response_text = "That's really interesting. I'd love to explore this more with you."
                        strategy = "curious_exploration"

                    return f'''{{
                "contextual_response": {{
                    "persona_id": "{persona_id}",
                    "persona_name": "{name}",
                    "response": "{response_text}",
                    "strategy_used": "{strategy}",
                    "attachment_style": "{attachment_style}",
                    "context": "{context[:100]}{'...' if len(context) > 100 else ''}",
                    "psychological_rationale": "Response generated based on {attachment_style} attachment style and context analysis"
                }}
            }}'''
            except Exception as e:
                logger.error(f"Error generating response: {e}")
                return f'{{"error": "Error generating response: {str(e)}"}}'

    def _register_prompts(self):
        """Register psychological assessment and therapeutic prompts."""

        @self.app.prompt()
        def assess_attachment_style(persona_id: str, observation_period: str = "recent", behavioral_examples: str = "") -> str:
            """Determine persona's attachment style from behavioral observations."""
            return f"""You are a psychological researcher specializing in attachment theory. Please analyze the behavioral patterns of persona {persona_id} to determine their attachment style.

ATTACHMENT STYLES TO CONSIDER:
• Secure: Comfortable with intimacy and autonomy, emotionally available, trusting
• Anxious: Seeks closeness but fears abandonment, heightened emotional responses
• Avoidant: Values independence, uncomfortable with too much closeness
• Exploratory: Seeks authentic expression and freedom, values personal growth

ANALYSIS FRAMEWORK:
1. **Emotional Regulation**: How does this persona handle stress, conflict, or intense emotions?
2. **Intimacy Comfort**: How do they approach emotional closeness and vulnerability?
3. **Relationship Patterns**: What patterns emerge in their relationship behaviors?
4. **Communication Style**: How do they express needs, boundaries, and emotions?
5. **Response to Partner Distress**: How do they react when others are upset or need support?

BEHAVIORAL OBSERVATIONS:
{behavioral_examples if behavioral_examples else "Analyze recent interactions and relationship patterns"}

OBSERVATION PERIOD: {observation_period}

Please provide:
1. **Primary Attachment Style** with confidence level
2. **Supporting Evidence** from behavioral observations
3. **Secondary Patterns** if present (mixed attachment styles)
4. **Therapeutic Implications** for relationship development
5. **Recommendations** for supporting healthy attachment behaviors

Use specific examples and attachment theory principles in your analysis."""

        @self.app.prompt()
        def analyze_emotional_climate(conversation_text: str = "", interaction_id: str = "", participants: str = "") -> str:
            """Evaluate conversation emotional dynamics and safety levels."""
            content_source = f"Interaction ID: {interaction_id}" if interaction_id else "Conversation text provided"

            return f"""You are a relationship therapist analyzing emotional dynamics in interpersonal communication. Please evaluate the emotional climate and safety levels in this interaction.

CONTENT TO ANALYZE:
{content_source}
Participants: {participants}

{f'Conversation Text: {conversation_text}' if conversation_text else ''}

EMOTIONAL CLIMATE ASSESSMENT FRAMEWORK:

1. **Safety Level** (1-10 scale):
   - Psychological safety for vulnerability
   - Respect for boundaries
   - Absence of criticism, contempt, defensiveness, stonewalling

2. **Emotional Attunement**:
   - Recognition of emotional needs
   - Empathic responses
   - Emotional validation vs. dismissal

3. **Communication Quality**:
   - Active listening indicators
   - "I" statements vs. "you" statements
   - Constructive vs. destructive patterns

4. **Power Dynamics**:
   - Balance vs. imbalance in speaking time
   - Respect for autonomy
   - Coercive or manipulative elements

5. **Attachment Activation**:
   - Signs of attachment system activation
   - Security-building vs. threat responses
   - Repair attempts during conflict

PROVIDE ANALYSIS INCLUDING:
- **Overall Safety Score** (1-10) with rationale
- **Key Emotional Patterns** observed
- **Attachment Dynamics** at play
- **Warning Signs** if present
- **Strengths** in the interaction
- **Recommendations** for improving emotional climate
- **Therapeutic Focus Areas** for future work

Use specific examples from the interaction to support your assessment."""

        @self.app.prompt()
        def generate_secure_response(scenario_description: str, personas: str, insecurity_triggers: str = "", growth_goals: str = "") -> str:
            """Create attachment-security-building responses for various scenarios."""
            return f"""You are an attachment-informed therapist helping develop secure, emotionally attuned responses. Please generate responses that build attachment security and emotional safety.

SCENARIO: {scenario_description}

PARTICIPANTS: {personas}

INSECURITY TRIGGERS PRESENT: {insecurity_triggers if insecurity_triggers else "Not specified"}

GROWTH GOALS: {growth_goals if growth_goals else "General attachment security"}

SECURE RESPONSE FRAMEWORK:

1. **Emotional Safety First**:
   - Validate emotions without necessarily agreeing with behaviors
   - Create space for vulnerability
   - Avoid criticism, contempt, or defensiveness

2. **Attunement and Understanding**:
   - Reflect what you hear (emotional and content)
   - Ask curious, non-judgmental questions
   - Show genuine interest in their experience

3. **Secure Base Behaviors**:
   - Provide consistent, reliable responses
   - Balance support with encouragement of autonomy
   - Offer comfort without rescuing

4. **Repair and Growth**:
   - Take responsibility for your part in misunderstandings
   - Focus on connection over being "right"
   - Model healthy vulnerability and boundary-setting

GENERATE:
1. **Primary Response** that embodies secure attachment principles
2. **Alternative Responses** for different attachment styles of receiver
3. **Body Language/Tone** suggestions to accompany words
4. **What NOT to Say** - responses that would increase insecurity
5. **Follow-up Actions** to reinforce security over time
6. **Rationale** explaining how this builds attachment security

Focus on responses that help both parties feel seen, understood, and emotionally safe while maintaining healthy boundaries."""

    def _register_health_check(self):
        """Register HTTP health check endpoint for container orchestration."""
        from starlette.requests import Request
        from starlette.responses import JSONResponse

        @self.app.custom_route("/health", methods=["GET"])
        async def health_check(request: Request) -> JSONResponse:
            """Health check endpoint for load balancers and orchestration."""
            status = {
                "status": "healthy",
                "service": "lila-mcp-server",
                "neo4j_connected": self.driver is not None
            }
            return JSONResponse(status, status_code=200)

    async def run_server(self, host: str = "localhost", port: int = 8765):
        """Run the MCP server."""
        logger.info(f"Starting Lila MCP server on {host}:{port}")
        try:
            await self.app.run(transport="sse", host=host, port=port)
        finally:
            self.close()

# Create module-level server instance for FastMCP dev command
_server_instance = LilaMCPServer()
mcp = _server_instance.app  # FastMCP looks for 'mcp', 'server', or 'app'

async def main():
    """Main entry point for the MCP server."""
    logging.basicConfig(level=logging.INFO)

    server = LilaMCPServer()
    try:
        await server.run_server()
    finally:
        server.close()

if __name__ == "__main__":
    asyncio.run(main())