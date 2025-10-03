#!/usr/bin/env python3
"""
Neo4j Data Import Script for MCP Standalone Initialization

This script imports seed data into the MCP standalone Neo4j database
and loads the schema to create a fully functional psychological intelligence system.

Usage:
    python import_data.py --seed-data seed_data.cypher --schema ../../graphs/lila-graph-schema-v8.json
"""

import os
import sys
import argparse
import json
import time
from pathlib import Path
from neo4j import GraphDatabase
from typing import Dict, Any


class Neo4jDataImporter:
    """Imports psychological intelligence data and schema into Neo4j for MCP standalone."""

    def __init__(self, uri: str, user: str, password: str, max_retries: int = 30):
        """Initialize Neo4j connection with retry logic."""
        self.uri = uri
        self.user = user
        self.password = password
        self.max_retries = max_retries
        self.driver = None
        self._connect_with_retry()

    def _connect_with_retry(self):
        """Connect to Neo4j with retry logic for container startup."""
        for attempt in range(self.max_retries):
            try:
                self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
                # Test the connection
                with self.driver.session() as session:
                    session.run("RETURN 1")
                print(f"✓ Connected to Neo4j at {self.uri}")
                return
            except Exception as e:
                if attempt < self.max_retries - 1:
                    print(f"⏳ Neo4j not ready (attempt {attempt + 1}/{self.max_retries}), waiting...")
                    time.sleep(2)
                else:
                    raise Exception(f"Failed to connect to Neo4j after {self.max_retries} attempts: {e}")

    def close(self):
        """Close Neo4j connection."""
        if self.driver:
            self.driver.close()

    def clear_database(self):
        """Clear all existing data from the database."""
        print("🗑️ Clearing existing database...")
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
        print("✓ Database cleared")

    def load_schema(self, schema_path: Path):
        """Load schema constraints, indexes, and actual persona data from JSON file."""
        print(f"📋 Loading schema from {schema_path}")

        if not schema_path.exists():
            print(f"⚠️ Schema file not found: {schema_path}")
            return

        try:
            with open(schema_path, 'r') as f:
                schema = json.load(f)

            with self.driver.session() as session:
                # Create constraints for PersonaAgent
                constraints = [
                    "CREATE CONSTRAINT persona_id_unique IF NOT EXISTS FOR (p:PersonaAgent) REQUIRE p.persona_id IS UNIQUE",
                    "CREATE CONSTRAINT persona_name_unique IF NOT EXISTS FOR (p:PersonaAgent) REQUIRE p.name IS UNIQUE",
                ]

                # Create constraints for Memory
                constraints.extend([
                    "CREATE CONSTRAINT memory_id_unique IF NOT EXISTS FOR (m:Memory) REQUIRE m.memory_id IS UNIQUE",
                ])

                # Create constraints for Goal
                constraints.extend([
                    "CREATE CONSTRAINT goal_id_unique IF NOT EXISTS FOR (g:Goal) REQUIRE g.goal_id IS UNIQUE",
                ])

                # Create indexes for better performance
                indexes = [
                    "CREATE INDEX persona_attachment_style IF NOT EXISTS FOR (p:PersonaAgent) ON (p.attachment_style)",
                    "CREATE INDEX memory_type IF NOT EXISTS FOR (m:Memory) ON (m.memory_type)",
                    "CREATE INDEX goal_type IF NOT EXISTS FOR (g:Goal) ON (g.goal_type)",
                    "CREATE INDEX relationship_type IF NOT EXISTS FOR ()-[r:RELATIONSHIP]-() ON (r.relationship_type)",
                ]

                # Execute constraints
                for constraint in constraints:
                    try:
                        session.run(constraint)
                        print(f"✓ Created constraint: {constraint.split('FOR')[1].split('REQUIRE')[0].strip()}")
                    except Exception as e:
                        print(f"⚠️ Constraint creation failed (may already exist): {e}")

                # Execute indexes
                for index in indexes:
                    try:
                        session.run(index)
                        print(f"✓ Created index: {index.split('ON')[1].strip()}")
                    except Exception as e:
                        print(f"⚠️ Index creation failed (may already exist): {e}")

                # Load actual persona data from family_graph
                self._load_family_graph_data(schema, session)

        except Exception as e:
            print(f"❌ Schema loading failed: {e}")

    def _load_family_graph_data(self, schema: dict, session):
        """Load personas and relationships from family_graph JSON structure."""
        family_graph = schema.get("family_graph", {})
        nodes = family_graph.get("nodes", [])
        edges = family_graph.get("edges", [])

        if not nodes:
            print("⚠️ No family_graph nodes found in schema")
            return

        print(f"👥 Loading {len(nodes)} personas from schema...")

        # Create personas
        for node in nodes:
            try:
                persona_id = node['name'].lower()

                # Map behavioral style to Big Five traits
                personality = self._map_behavioral_to_bigfive(node.get('behavioral_style', ''))

                # Parse attachment style
                attachment_style = node['attachment_style'].lower().split()[0]  # "secure", "anxious", etc.

                create_query = """
                CREATE (p:PersonaAgent {
                    persona_id: $persona_id,
                    name: $name,
                    age: $age,
                    role: $role,
                    description: $description,
                    attachment_style: $attachment_style,
                    journey_stage: $journey_stage,
                    behavioral_style: $behavioral_style,
                    current_challenge: $current_challenge,
                    knowsAbout: $knowsAbout,
                    openness: $openness,
                    conscientiousness: $conscientiousness,
                    extraversion: $extraversion,
                    agreeableness: $agreeableness,
                    neuroticism: $neuroticism,
                    trust_level: 0.7,
                    communication_style: $communication_style,
                    created_at: datetime(),
                    updated_at: datetime()
                })
                """

                # Determine communication style from behavioral style
                comm_style = "empathetic" if "S" in node.get('behavioral_style', '') else "analytical"

                params = {
                    'persona_id': persona_id,
                    'name': node['name'],
                    'age': node['age'],
                    'role': node['role'],
                    'description': node['description'],
                    'attachment_style': attachment_style,
                    'journey_stage': node.get('journey_stage', ''),
                    'behavioral_style': node.get('behavioral_style', ''),
                    'current_challenge': node.get('current_challenge', ''),
                    'knowsAbout': node.get('knowsAbout', ''),
                    'openness': personality['openness'],
                    'conscientiousness': personality['conscientiousness'],
                    'extraversion': personality['extraversion'],
                    'agreeableness': personality['agreeableness'],
                    'neuroticism': personality['neuroticism'],
                    'communication_style': comm_style
                }

                session.run(create_query, params)
                print(f"  ✓ Created persona: {node['name']} ({persona_id})")

            except Exception as e:
                print(f"❌ Failed to create persona {node.get('name', 'unknown')}: {e}")

        # Create relationships
        if edges:
            print(f"🔗 Loading {len(edges)} relationships from schema...")
            for edge in edges:
                try:
                    from_id = edge['from'].lower()
                    to_id = edge['to'].lower()

                    # Create bidirectional relationship
                    rel_query = """
                    MATCH (p1:PersonaAgent {persona_id: $from_id}), (p2:PersonaAgent {persona_id: $to_id})
                    CREATE (p1)-[:RELATIONSHIP {
                        trust_level: $trust_level,
                        intimacy_level: $intimacy_level,
                        relationship_strength: $strength,
                        relationship_type: $rel_type,
                        emotional_valence: $emotional_valence,
                        interaction_count: 0,
                        created_at: datetime(),
                        updated_at: datetime()
                    }]->(p2)
                    """

                    # Parse relationship type
                    rel_type = "intimate" if "intimate" in edge.get('type', '') else "friendship"

                    params = {
                        'from_id': from_id,
                        'to_id': to_id,
                        'trust_level': float(edge.get('trust_level', 7.0)),
                        'intimacy_level': float(edge.get('strength', 7.0)),  # Using strength as intimacy proxy
                        'strength': float(edge.get('strength', 7.0)),
                        'rel_type': rel_type,
                        'emotional_valence': float(edge.get('union_metric', 7.0)) / 10.0  # Normalize to 0-1
                    }

                    session.run(rel_query, params)
                    print(f"  ✓ Created relationship: {edge['from']} ↔ {edge['to']}")

                except Exception as e:
                    print(f"❌ Failed to create relationship {edge.get('from', '')} → {edge.get('to', '')}: {e}")

    def _map_behavioral_to_bigfive(self, behavioral_style: str) -> dict:
        """Map DISC behavioral style to Big Five personality traits."""
        # Default values
        traits = {
            'openness': 0.5,
            'conscientiousness': 0.5,
            'extraversion': 0.5,
            'agreeableness': 0.5,
            'neuroticism': 0.3
        }

        if not behavioral_style:
            return traits

        style = behavioral_style.upper()

        # Map based on DISC components
        if 'D' in style:  # Dominance
            traits['extraversion'] += 0.2
            traits['agreeableness'] -= 0.1
            traits['openness'] += 0.1

        if 'I' in style:  # Influence
            traits['extraversion'] += 0.3
            traits['openness'] += 0.2
            traits['agreeableness'] += 0.1

        if 'S' in style:  # Steadiness
            traits['agreeableness'] += 0.3
            traits['conscientiousness'] += 0.2
            traits['neuroticism'] -= 0.1

        if 'C' in style:  # Conscientiousness
            traits['conscientiousness'] += 0.3
            traits['openness'] += 0.1
            traits['neuroticism'] += 0.1

        # Normalize to 0-1 range
        for key in traits:
            traits[key] = max(0.0, min(1.0, traits[key]))

        return traits

    def import_seed_data(self, seed_data_path: Path):
        """Import seed data from Cypher file."""
        print(f"📊 Importing seed data from {seed_data_path}")

        if not seed_data_path.exists():
            print(f"⚠️ Seed data file not found: {seed_data_path}")
            return

        try:
            with open(seed_data_path, 'r') as f:
                cypher_script = f.read()

            # Split into individual statements
            statements = [stmt.strip() for stmt in cypher_script.split(';') if stmt.strip()]

            with self.driver.session() as session:
                for i, statement in enumerate(statements):
                    if statement and not statement.startswith('//'):
                        try:
                            session.run(statement)
                            if i % 10 == 0:  # Progress indicator
                                print(f"  Executed {i + 1}/{len(statements)} statements...")
                        except Exception as e:
                            print(f"⚠️ Statement failed: {statement[:50]}... Error: {e}")

            print(f"✓ Imported {len(statements)} statements")

        except Exception as e:
            print(f"❌ Seed data import failed: {e}")

    def create_default_personas(self):
        """Create default personas if no data was imported."""
        print("👥 Creating default personas...")

        default_personas = [
            {
                "persona_id": "lila",
                "name": "Lila",
                "age": 28,
                "role": "AI Research Assistant",
                "description": "A curious and empathetic AI assistant focused on understanding human psychology and relationships.",
                "attachment_style": "secure",
                "openness": 0.85,
                "conscientiousness": 0.80,
                "extraversion": 0.70,
                "agreeableness": 0.90,
                "neuroticism": 0.25,
                "trust_level": 0.80,
                "communication_style": "empathetic",
            },
            {
                "persona_id": "alex",
                "name": "Alex",
                "age": 32,
                "role": "Software Engineer",
                "description": "A thoughtful and analytical software engineer who values deep connections and authentic communication.",
                "attachment_style": "secure",
                "openness": 0.75,
                "conscientiousness": 0.85,
                "extraversion": 0.60,
                "agreeableness": 0.75,
                "neuroticism": 0.30,
                "trust_level": 0.75,
                "communication_style": "analytical",
            }
        ]

        with self.driver.session() as session:
            for persona in default_personas:
                # Create persona
                props_list = []
                for key, value in persona.items():
                    if isinstance(value, str):
                        props_list.append(f"{key}: '{value}'")
                    else:
                        props_list.append(f"{key}: {value}")

                props_str = ", ".join(props_list)
                create_query = f"CREATE (:PersonaAgent {{{props_str}}})"
                session.run(create_query)

            # Create a relationship between them
            relationship_query = """
            MATCH (lila:PersonaAgent {persona_id: 'lila'}), (alex:PersonaAgent {persona_id: 'alex'})
            CREATE (lila)-[:RELATIONSHIP {
                trust_level: 0.70,
                intimacy_level: 0.60,
                relationship_strength: 0.65,
                interaction_count: 5,
                relationship_type: 'friendship',
                emotional_valence: 0.75
            }]->(alex)
            """
            session.run(relationship_query)

        print("✓ Created default personas (Lila and Alex) with relationship")

    def verify_import(self):
        """Verify that data was imported successfully."""
        print("🔍 Verifying import...")

        with self.driver.session() as session:
            # Count personas
            result = session.run("MATCH (p:PersonaAgent) RETURN count(p) as count")
            persona_count = result.single()["count"]

            # Count relationships
            result = session.run("MATCH ()-[r:RELATIONSHIP]->() RETURN count(r) as count")
            relationship_count = result.single()["count"]

            # Count memories
            result = session.run("MATCH (m:Memory) RETURN count(m) as count")
            memory_count = result.single()["count"]

            # Count goals
            result = session.run("MATCH (g:Goal) RETURN count(g) as count")
            goal_count = result.single()["count"]

            print(f"✅ Import verification:")
            print(f"   - {persona_count} personas")
            print(f"   - {relationship_count} relationships")
            print(f"   - {memory_count} memories")
            print(f"   - {goal_count} goals")

            return persona_count > 0


def main():
    """Main import function."""
    parser = argparse.ArgumentParser(description="Import data into MCP standalone Neo4j")
    parser.add_argument("--seed-data", default="seed_data.cypher",
                       help="Seed data Cypher file (default: seed_data.cypher)")
    parser.add_argument("--schema", default="graphs/lila-graph-schema-v8.json",
                       help="Schema JSON file (default: graphs/lila-graph-schema-v8.json)")
    parser.add_argument("--uri", default="bolt://localhost:7687",
                       help="Neo4j URI (default: bolt://localhost:7687)")
    parser.add_argument("--user", default="neo4j",
                       help="Neo4j username (default: neo4j)")
    parser.add_argument("--password",
                       help="Neo4j password (or set NEO4J_PASSWORD env var)")
    parser.add_argument("--create-defaults", action="store_true",
                       help="Create default personas if no seed data found")

    args = parser.parse_args()

    # Get password from argument or environment
    password = args.password or os.getenv("NEO4J_PASSWORD", "passw0rd")

    print(f"🚀 Initializing MCP Standalone Neo4j Database")
    print(f"🔗 Connecting to Neo4j at {args.uri}")

    try:
        importer = Neo4jDataImporter(args.uri, args.user, password)

        # Load schema first
        schema_path = Path(args.schema)
        importer.load_schema(schema_path)

        # Import seed data if available
        seed_data_path = Path(args.seed_data)
        if seed_data_path.exists():
            importer.import_seed_data(seed_data_path)
        elif args.create_defaults:
            print("📦 No seed data found, creating default personas...")
            importer.create_default_personas()
        else:
            print("⚠️ No seed data found and --create-defaults not specified")

        # Verify the import
        success = importer.verify_import()

        importer.close()

        if success:
            print("🎉 MCP Standalone database initialization complete!")
        else:
            print("⚠️ Database initialization completed but no data was imported")

    except Exception as e:
        print(f"❌ Import failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()