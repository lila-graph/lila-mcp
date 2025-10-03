#!/usr/bin/env python3
"""Validation tests for multi-domain orchestrator system.

Tests all components without requiring actual Claude API calls.
"""

def test_imports():
    """Test that all modules can be imported."""
    print("=== Testing Imports ===")

    try:
        from orchestrators.base_orchestrator import BaseOrchestrator
        print("✅ BaseOrchestrator")

        from orchestrators.architecture_orchestrator import ArchitectureOrchestrator
        print("✅ ArchitectureOrchestrator")

        from orchestrators.ux_orchestrator import UXOrchestrator
        print("✅ UXOrchestrator")

        from agents.registry import AgentRegistry
        print("✅ AgentRegistry")

        from tools.mcp_registry import MCPRegistry
        print("✅ MCPRegistry")

        from tools.figma_integration import FigmaIntegration
        print("✅ FigmaIntegration")

        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False


def test_agent_registry():
    """Test agent registry functionality."""
    print("\n=== Testing Agent Registry ===")

    try:
        from agents.registry import AgentRegistry

        registry = AgentRegistry()
        print(f"✅ Registry created")

        # Discover agents
        all_agents = registry.discover_agents()
        print(f"✅ Discovered {len(all_agents)} agents")

        expected_agents = {
            'ux_researcher', 'ia_architect', 'ui_designer', 'prototype_developer',
            'analyzer', 'doc_writer'
        }

        found_agents = set(all_agents.keys())
        if found_agents == expected_agents:
            print(f"✅ All expected agents found: {', '.join(sorted(found_agents))}")
        else:
            missing = expected_agents - found_agents
            extra = found_agents - expected_agents
            if missing:
                print(f"⚠️ Missing agents: {missing}")
            if extra:
                print(f"⚠️ Extra agents: {extra}")

        # Test loading an agent
        ux_researcher = registry.load_agent('ux_researcher', domain='ux')
        if ux_researcher:
            print(f"✅ Successfully loaded ux_researcher")
            print(f"   Tools: {ux_researcher.tools}")
        else:
            print("❌ Failed to load ux_researcher")
            return False

        return True
    except Exception as e:
        print(f"❌ Agent registry test failed: {e}")
        return False


def test_mcp_registry():
    """Test MCP registry functionality."""
    print("\n=== Testing MCP Registry ===")

    try:
        from tools.mcp_registry import MCPRegistry

        registry = MCPRegistry()
        print(f"✅ MCP Registry created")

        servers = list(registry.available_servers.keys())
        print(f"✅ Found {len(servers)} MCP servers: {', '.join(servers)}")

        # Check expected servers
        expected = {'figma', 'v0', 'sequential-thinking', 'playwright'}
        found = set(servers)

        if found == expected:
            print(f"✅ All expected MCP servers registered")
        else:
            print(f"⚠️ Server mismatch - Expected: {expected}, Found: {found}")

        # Test availability check
        available = registry.is_server_available('sequential-thinking')
        print(f"✅ Availability check works (sequential-thinking: {available})")

        return True
    except Exception as e:
        print(f"❌ MCP registry test failed: {e}")
        return False


def test_orchestrator_instantiation():
    """Test that orchestrators can be instantiated."""
    print("\n=== Testing Orchestrator Instantiation ===")

    try:
        from orchestrators.architecture_orchestrator import ArchitectureOrchestrator
        from orchestrators.ux_orchestrator import UXOrchestrator

        # Architecture Orchestrator
        arch = ArchitectureOrchestrator()
        print(f"✅ ArchitectureOrchestrator created")
        print(f"   Domain: {arch.domain_name}")
        print(f"   Agents: {list(arch.get_agent_definitions().keys())}")
        print(f"   Tools: {arch.get_allowed_tools()}")

        # UX Orchestrator
        ux = UXOrchestrator(project_name="Test Project")
        print(f"✅ UXOrchestrator created")
        print(f"   Domain: {ux.domain_name}")
        print(f"   Project: {ux.project_name}")
        print(f"   Agents: {list(ux.get_agent_definitions().keys())}")
        print(f"   Tools: {ux.get_allowed_tools()}")

        return True
    except Exception as e:
        print(f"❌ Orchestrator instantiation failed: {e}")
        return False


def test_figma_integration():
    """Test Figma integration setup."""
    print("\n=== Testing Figma Integration ===")

    try:
        from tools.figma_integration import FigmaIntegration

        figma = FigmaIntegration()
        print(f"✅ FigmaIntegration created")
        print(f"   Available: {figma.is_available()}")

        # Get setup instructions
        instructions = figma.get_setup_instructions()
        if len(instructions) > 0:
            print(f"✅ Setup instructions available ({len(instructions)} chars)")
        else:
            print("❌ No setup instructions found")
            return False

        return True
    except Exception as e:
        print(f"❌ Figma integration test failed: {e}")
        return False


def main():
    """Run all validation tests."""
    print("=" * 70)
    print("Multi-Domain Orchestrator System - Validation Tests")
    print("=" * 70)

    tests = [
        ("Imports", test_imports),
        ("Agent Registry", test_agent_registry),
        ("MCP Registry", test_mcp_registry),
        ("Orchestrator Instantiation", test_orchestrator_instantiation),
        ("Figma Integration", test_figma_integration),
    ]

    results = []
    for name, test_func in tests:
        result = test_func()
        results.append((name, result))

    # Summary
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")

    print("=" * 70)
    print(f"Results: {passed}/{total} tests passed")

    if passed == total:
        print("✅ All tests passed! System is ready to use.")
        return 0
    else:
        print("❌ Some tests failed. Please review the output above.")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
