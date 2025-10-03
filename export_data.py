#!/usr/bin/env python3
"""
Neo4j Data Export Script for MCP Standalone Initialization

This script exports persona and relationship data from the main Lila system's Neo4j
database and creates seed data for MCP standalone deployment.

Usage:
    python export_data.py --output seed_data.cypher
"""

import os
import sys
import argparse
from pathlib import Path
from neo4j import GraphDatabase
from typing import List, Dict, Any
import json


class Neo4jDataExporter:
    """Exports psychological intelligence data from Neo4j for MCP standalone seeding."""

    def __init__(self, uri: str, user: str, password: str):
        """Initialize Neo4j connection."""
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        """Close Neo4j connection."""
        self.driver.close()

    def export_personas(self) -> List[Dict[str, Any]]:
        """Export all PersonaAgent nodes with their psychological profiles."""
        query = """
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
        """

        with self.driver.session() as session:
            result = session.run(query)
            personas = []
            for record in result:
                persona = dict(record)
                personas.append(persona)

        print(f"✓ Exported {len(personas)} personas")
        return personas

    def export_relationships(self) -> List[Dict[str, Any]]:
        """Export all relationships between personas."""
        query = """
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
        """

        with self.driver.session() as session:
            result = session.run(query)
            relationships = []
            for record in result:
                relationship = dict(record)
                relationships.append(relationship)

        print(f"✓ Exported {len(relationships)} relationships")
        return relationships

    def export_memories(self) -> List[Dict[str, Any]]:
        """Export memory nodes associated with personas."""
        query = """
        MATCH (p:PersonaAgent)-[:HAS_MEMORY]->(m:Memory)
        RETURN p.persona_id as persona_id,
               m.memory_id as memory_id,
               m.content as content,
               m.memory_type as memory_type,
               m.importance_score as importance_score,
               m.emotional_valence as emotional_valence,
               m.participants as participants,
               m.created_at as created_at
        """

        with self.driver.session() as session:
            result = session.run(query)
            memories = []
            for record in result:
                memory = dict(record)
                memories.append(memory)

        print(f"✓ Exported {len(memories)} memories")
        return memories

    def export_goals(self) -> List[Dict[str, Any]]:
        """Export goal nodes associated with personas."""
        query = """
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
        """

        with self.driver.session() as session:
            result = session.run(query)
            goals = []
            for record in result:
                goal = dict(record)
                goals.append(goal)

        print(f"✓ Exported {len(goals)} goals")
        return goals

    def generate_cypher_script(self, personas: List[Dict], relationships: List[Dict],
                             memories: List[Dict], goals: List[Dict]) -> str:
        """Generate Cypher script for importing data into MCP standalone."""

        script_lines = [
            "// Lila Psychological Intelligence System - Seed Data for MCP Standalone",
            "// Generated from main system export",
            "",
            "// Clear existing data",
            "MATCH (n) DETACH DELETE n;",
            "",
            "// Create Personas",
        ]

        for persona in personas:
            # Handle None values and create Cypher-safe strings
            properties = []
            for key, value in persona.items():
                if value is not None:
                    if isinstance(value, str):
                        # Escape quotes and newlines
                        safe_value = value.replace("'", "\\'").replace("\n", "\\n")
                        properties.append(f"{key}: '{safe_value}'")
                    elif isinstance(value, (int, float)):
                        properties.append(f"{key}: {value}")
                    elif isinstance(value, bool):
                        properties.append(f"{key}: {str(value).lower()}")

            props_str = ", ".join(properties)
            script_lines.append(f"CREATE (:PersonaAgent {{{props_str}}});")

        script_lines.extend(["", "// Create Relationships"])

        for rel in relationships:
            persona1_id = rel['persona1_id']
            persona2_id = rel['persona2_id']

            properties = []
            for key, value in rel.items():
                if key not in ['persona1_id', 'persona2_id'] and value is not None:
                    if isinstance(value, str):
                        safe_value = value.replace("'", "\\'").replace("\n", "\\n")
                        properties.append(f"{key}: '{safe_value}'")
                    elif isinstance(value, (int, float)):
                        properties.append(f"{key}: {value}")
                    elif isinstance(value, bool):
                        properties.append(f"{key}: {str(value).lower()}")

            props_str = ", ".join(properties)
            script_lines.append(
                f"MATCH (p1:PersonaAgent {{persona_id: '{persona1_id}'}}), "
                f"(p2:PersonaAgent {{persona_id: '{persona2_id}'}}) "
                f"CREATE (p1)-[:RELATIONSHIP {{{props_str}}}]->(p2);"
            )

        # Add memories if any
        if memories:
            script_lines.extend(["", "// Create Memories"])
            for memory in memories:
                persona_id = memory['persona_id']

                properties = []
                for key, value in memory.items():
                    if key != 'persona_id' and value is not None:
                        if isinstance(value, str):
                            safe_value = value.replace("'", "\\'").replace("\n", "\\n")
                            properties.append(f"{key}: '{safe_value}'")
                        elif isinstance(value, (int, float)):
                            properties.append(f"{key}: {value}")
                        elif isinstance(value, bool):
                            properties.append(f"{key}: {str(value).lower()}")

                props_str = ", ".join(properties)
                script_lines.extend([
                    f"MATCH (p:PersonaAgent {{persona_id: '{persona_id}'}}) "
                    f"CREATE (p)-[:HAS_MEMORY]->(:Memory {{{props_str}}});"
                ])

        # Add goals if any
        if goals:
            script_lines.extend(["", "// Create Goals"])
            for goal in goals:
                persona_id = goal['persona_id']

                properties = []
                for key, value in goal.items():
                    if key != 'persona_id' and value is not None:
                        if isinstance(value, str):
                            safe_value = value.replace("'", "\\'").replace("\n", "\\n")
                            properties.append(f"{key}: '{safe_value}'")
                        elif isinstance(value, (int, float)):
                            properties.append(f"{key}: {value}")
                        elif isinstance(value, bool):
                            properties.append(f"{key}: {str(value).lower()}")

                props_str = ", ".join(properties)
                script_lines.append(
                    f"MATCH (p:PersonaAgent {{persona_id: '{persona_id}'}}) "
                    f"CREATE (p)-[:HAS_GOAL]->(:Goal {{{props_str}}});"
                )

        return "\n".join(script_lines)


def main():
    """Main export function."""
    parser = argparse.ArgumentParser(description="Export Neo4j data for MCP standalone")
    parser.add_argument("--output", default="seed_data.cypher",
                       help="Output Cypher file (default: seed_data.cypher)")
    parser.add_argument("--uri", default="bolt://localhost:7687",
                       help="Neo4j URI (default: bolt://localhost:7687)")
    parser.add_argument("--user", default="neo4j",
                       help="Neo4j username (default: neo4j)")
    parser.add_argument("--password",
                       help="Neo4j password (or set NEO4J_PASSWORD env var)")

    args = parser.parse_args()

    # Get password from argument or environment
    password = args.password or os.getenv("NEO4J_PASSWORD", "passw0rd")

    print(f"🔗 Connecting to Neo4j at {args.uri}")

    try:
        exporter = Neo4jDataExporter(args.uri, args.user, password)

        print("📊 Exporting data from main system...")
        personas = exporter.export_personas()
        relationships = exporter.export_relationships()
        memories = exporter.export_memories()
        goals = exporter.export_goals()

        print("📝 Generating Cypher import script...")
        cypher_script = exporter.generate_cypher_script(personas, relationships, memories, goals)

        # Write to output file
        output_path = Path(args.output)
        with open(output_path, 'w') as f:
            f.write(cypher_script)

        print(f"✅ Export complete: {output_path}")
        print(f"   - {len(personas)} personas")
        print(f"   - {len(relationships)} relationships")
        print(f"   - {len(memories)} memories")
        print(f"   - {len(goals)} goals")

        exporter.close()

    except Exception as e:
        print(f"❌ Export failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()