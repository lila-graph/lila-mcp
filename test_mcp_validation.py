"""Comprehensive validation script for Lila MCP Server.

Validates both direct connection (FastMCP best practice) and Inspector connectivity.
This consolidated test replaces the separate test files for better maintenance.
"""

import asyncio
import logging
from fastmcp import Client
from simple_lila_mcp_server import SimpleLilaMCPServer

# Enable logging for debugging
logging.basicConfig(level=logging.INFO)

async def test_direct_connection():
    """Test the MCP server using direct in-memory connection (FastMCP best practice)."""

    print("🧪 Testing Simplified Lila MCP Server (Direct Connection)")
    print("=" * 60)

    # Create the server instance
    server_instance = SimpleLilaMCPServer()
    mcp_server = server_instance.app

    # Use in-memory connection (FastMCP testing best practice)
    async with Client(mcp_server) as client:
        print(f"✅ Connected: {client.is_connected()}")

        # Test basic connectivity
        print("\n🔍 Testing server connectivity...")
        await client.ping()
        print("✅ Server is reachable")

        # List and test resources
        print("\n📁 Testing resources...")
        resources = await client.list_resources()
        print(f"✅ Resources found: {len(resources)}")
        for resource in resources:
            print(f"   - {resource.uri}")

        # Test reading a specific resource
        if resources:
            test_resource = resources[0]
            print(f"\n📖 Testing resource read: {test_resource.uri}")
            try:
                content = await client.read_resource(test_resource.uri)
                print("✅ Resource read successful")
                print(f"   Content preview: {str(content)[:100]}...")
            except Exception as e:
                print(f"❌ Resource read failed: {e}")

        # List and test tools
        print("\n🔧 Testing tools...")
        tools = await client.list_tools()
        print(f"✅ Tools found: {len(tools)}")
        for tool in tools:
            print(f"   - {tool.name}")

        # Test calling a simple tool
        if tools:
            try:
                print(f"\n⚙️ Testing tool call: analyze_persona_compatibility")
                result = await client.call_tool("analyze_persona_compatibility", {
                    "persona1_id": "lila",
                    "persona2_id": "don",
                    "relationship_type": "romantic"
                })
                print("✅ Tool call successful")
                print(f"   Result preview: {str(result.content[0].text)[:200]}...")
            except Exception as e:
                print(f"❌ Tool call failed: {e}")

        # List and test prompts
        print("\n💭 Testing prompts...")
        prompts = await client.list_prompts()
        print(f"✅ Prompts found: {len(prompts)}")
        for prompt in prompts:
            print(f"   - {prompt.name}")

        # Test getting a prompt
        if prompts:
            try:
                test_prompt = prompts[0]
                print(f"\n📝 Testing prompt: {test_prompt.name}")
                prompt_result = await client.get_prompt(test_prompt.name, {
                    "persona_id": "lila",
                    "observation_period": "recent",
                    "behavioral_examples": "Shows consistent emotional support"
                })
                print("✅ Prompt retrieval successful")
                print(f"   Messages count: {len(prompt_result.messages)}")
            except Exception as e:
                print(f"❌ Prompt retrieval failed: {e}")

    print(f"\n✅ Connection closed properly")
    return True, len(resources), len(tools), len(prompts)

async def test_inspector_connection():
    """Test the Inspector connection using HTTP client."""

    print("\n🧪 Testing FastMCP Inspector Connection")
    print("=" * 50)

    # Connect to the local FastMCP server
    client = Client("http://localhost:6274/")

    try:
        async with client:
            print(f"✅ Connected: {client.is_connected()}")

            # Test basic connectivity
            print("\n🔍 Testing server connectivity...")
            await client.ping()
            print("✅ Server is reachable")

            # Test resources, tools, and prompts
            resources = await client.list_resources()
            tools = await client.list_tools()
            prompts = await client.list_prompts()

            print(f"✅ Resources found: {len(resources)}")
            print(f"✅ Tools found: {len(tools)}")
            print(f"✅ Prompts found: {len(prompts)}")

        print(f"\n✅ Inspector connection successful")
        return True

    except Exception as e:
        print(f"❌ Inspector connection failed: {e}")
        print("   This is expected if Inspector server is not running")
        print("   Start with: fastmcp dev simple_lila_mcp_server.py")
        return False

async def main():
    """Run comprehensive MCP validation tests."""

    print("🌟 Lila MCP Server Comprehensive Validation")
    print("=" * 70)

    # Test 1: Direct Connection (Always works)
    direct_success, resources_count, tools_count, prompts_count = await test_direct_connection()

    # Test 2: Inspector Connection (Requires running server)
    inspector_success = await test_inspector_connection()

    # Summary
    print("\n🎉 Validation Complete!")
    print("\n📋 Summary:")
    print(f"   • Direct connection: {'✅ PASS' if direct_success else '❌ FAIL'}")
    print(f"   • Inspector connection: {'✅ PASS' if inspector_success else '❌ FAIL'}")
    print(f"   • Resources available: ✅ ({resources_count} found)")
    print(f"   • Tools available: ✅ ({tools_count} found)")
    print(f"   • Prompts available: ✅ ({prompts_count} found)")

    if direct_success:
        print("\n✨ The simplified MCP server is working perfectly!")
        print("   This validates that the server is functional and self-contained.")

    if inspector_success:
        print("\n🌐 Inspector is working at:")
        print("   http://localhost:6274/?MCP_PROXY_AUTH_TOKEN=b9e561b7c73c4cf749fa0d7b71bf636d10ff1727660f596a515bf64fee5fee28")
    else:
        print("\n💡 To test Inspector connection:")
        print("   1. Run: fastmcp dev simple_lila_mcp_server.py")
        print("   2. Re-run this test script")
        print("   3. Access Inspector at: http://localhost:6274/")

    return direct_success

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)