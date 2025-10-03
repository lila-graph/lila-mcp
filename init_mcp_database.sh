#!/bin/bash
# MCP Standalone Database Initialization Script
#
# This script automatically initializes the Neo4j database for MCP standalone
# by checking if data exists and importing seed data if needed.
#
# Usage: ./init_mcp_database.sh

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 MCP Standalone Database Initialization${NC}"

# Configuration
NEO4J_URI="${NEO4J_URI:-bolt://localhost:7687}"
NEO4J_USER="${NEO4J_USER:-neo4j}"
NEO4J_PASSWORD="${NEO4J_PASSWORD:-passw0rd}"
DATA_DIR="./data"
SEED_DATA_FILE="seed_data.cypher"
SCHEMA_FILE="../../graphs/lila-graph-schema-v8.json"

# Function to check if Neo4j is running
check_neo4j_ready() {
    local max_attempts=30
    local attempt=0

    echo -e "${BLUE}⏳ Waiting for Neo4j to be ready...${NC}"

    while [ $attempt -lt $max_attempts ]; do
        if python3 -c "
from neo4j import GraphDatabase
import sys
try:
    driver = GraphDatabase.driver('$NEO4J_URI', auth=('$NEO4J_USER', '$NEO4J_PASSWORD'))
    with driver.session() as session:
        session.run('RETURN 1')
    driver.close()
    print('✓ Neo4j is ready')
    sys.exit(0)
except:
    sys.exit(1)
" 2>/dev/null; then
            return 0
        fi

        attempt=$((attempt + 1))
        echo -e "${YELLOW}  Attempt $attempt/$max_attempts...${NC}"
        sleep 2
    done

    echo -e "${RED}❌ Neo4j failed to start after $max_attempts attempts${NC}"
    return 1
}

# Function to check if database has data
check_database_has_data() {
    echo -e "${BLUE}🔍 Checking if database has existing data...${NC}"

    local persona_count=$(python3 -c "
from neo4j import GraphDatabase
try:
    driver = GraphDatabase.driver('$NEO4J_URI', auth=('$NEO4J_USER', '$NEO4J_PASSWORD'))
    with driver.session() as session:
        result = session.run('MATCH (p:PersonaAgent) RETURN count(p) as count')
        count = result.single()['count']
    driver.close()
    print(count)
except Exception as e:
    print('0')
" 2>/dev/null)

    if [ "$persona_count" -gt 0 ]; then
        echo -e "${GREEN}✓ Database already has $persona_count personas${NC}"
        return 0
    else
        echo -e "${YELLOW}⚠️ Database is empty (persona count: $persona_count)${NC}"
        return 1
    fi
}

# Function to export data from main system
export_main_system_data() {
    echo -e "${BLUE}📤 Attempting to export data from main system...${NC}"

    # Check if main system Neo4j is accessible
    local main_neo4j_uri="bolt://localhost:7687"

    if python3 export_data.py --uri "$main_neo4j_uri" --output "$SEED_DATA_FILE" 2>/dev/null; then
        echo -e "${GREEN}✓ Successfully exported data from main system${NC}"
        return 0
    else
        echo -e "${YELLOW}⚠️ Could not export from main system (may not be running)${NC}"
        return 1
    fi
}

# Function to import data
import_database_data() {
    echo -e "${BLUE}📥 Importing data into MCP standalone database...${NC}"

    local import_args="--uri $NEO4J_URI --user $NEO4J_USER --password $NEO4J_PASSWORD"

    if [ -f "$SEED_DATA_FILE" ]; then
        echo -e "${BLUE}  Using seed data file: $SEED_DATA_FILE${NC}"
        python3 import_data.py $import_args --seed-data "$SEED_DATA_FILE" --schema "$SCHEMA_FILE"
    else
        echo -e "${YELLOW}  No seed data found, creating default personas${NC}"
        python3 import_data.py $import_args --create-defaults --schema "$SCHEMA_FILE"
    fi
}

# Function to start docker compose services
start_services() {
    echo -e "${BLUE}🐳 Starting MCP standalone infrastructure...${NC}"

    # Set UID/GID for proper permissions
    export UID=${UID:-$(id -u)}
    export GID=${GID:-$(id -g)}

    # Start services
    docker compose up -d

    # Wait for services to be healthy
    echo -e "${BLUE}⏳ Waiting for services to be healthy...${NC}"
    sleep 10
}

# Function to verify MCP server functionality
verify_mcp_server() {
    echo -e "${BLUE}🔧 Verifying MCP server functionality...${NC}"

    if command -v fastmcp >/dev/null 2>&1; then
        echo -e "${BLUE}  Testing FastMCP inspection...${NC}"
        fastmcp inspect

        echo -e "${BLUE}  MCP server is ready for development:${NC}"
        echo -e "${GREEN}    FastMCP Inspector: fastmcp dev${NC}"
        echo -e "${GREEN}    HTTP Server: fastmcp run${NC}"
    else
        echo -e "${YELLOW}⚠️ FastMCP not available, install with: pip install fastmcp${NC}"
    fi
}

# Main execution
main() {
    echo -e "${BLUE}Starting MCP Standalone initialization...${NC}"

    # Check if we're in the right directory
    if [ ! -f "fastmcp.json" ]; then
        echo -e "${RED}❌ Please run this script from the docker/mcp-standalone directory${NC}"
        exit 1
    fi

    # Start services
    start_services

    # Wait for Neo4j to be ready
    if ! check_neo4j_ready; then
        echo -e "${RED}❌ Neo4j failed to start${NC}"
        exit 1
    fi

    # Check if database needs initialization
    if check_database_has_data; then
        echo -e "${GREEN}✅ Database already initialized${NC}"
    else
        echo -e "${YELLOW}🔄 Initializing empty database...${NC}"

        # Try to export from main system first
        if ! export_main_system_data; then
            echo -e "${YELLOW}  Will create default personas instead${NC}"
        fi

        # Import data
        import_database_data

        # Verify import worked
        if check_database_has_data; then
            echo -e "${GREEN}✅ Database initialization successful${NC}"
        else
            echo -e "${RED}❌ Database initialization failed${NC}"
            exit 1
        fi
    fi

    # Verify MCP server
    verify_mcp_server

    echo -e "${GREEN}🎉 MCP Standalone is ready!${NC}"
    echo -e "${BLUE}Next steps:${NC}"
    echo -e "  ${GREEN}Development:${NC} fastmcp dev"
    echo -e "  ${GREEN}Production:${NC} fastmcp run"
    echo -e "  ${GREEN}Stop services:${NC} docker compose down"
}

# Run main function
main "$@"