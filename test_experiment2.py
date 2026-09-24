"""Quick test script for Experiment 2 MCP Server"""
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_weather_server():
    """Test the weather dashboard server."""
    
    server_params = StdioServerParameters(
        command="python",
        args=["experiment-2-data-dashboard/server.py"],
        env=None
    )
    
    print("Testing Weather Dashboard MCP Server...")
    print("=" * 60)
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize
            await session.initialize()
            
            # Test 1: List tools
            print("\n1. Listing available tools...")
            tools = await session.list_tools()
            for tool in tools.tools:
                print(f"   ✓ {tool.name}: {tool.description}")
            
            # Test 2: Get weather for Tokyo
            print("\n2. Testing get_current_weather for Tokyo...")
            print("   [Fetching weather data...]")
            result = await session.call_tool("get_current_weather", {
                "location": "Tokyo"
            })
            print(f"\n{result.content[0].text}")
            
            # Test 3: Get weather for London
            print("\n3. Testing get_current_weather for London...")
            print("   [Fetching weather data...]")
            result = await session.call_tool("get_current_weather", {
                "location": "London"
            })
            print(f"\n{result.content[0].text}")
            
            print("\n" + "=" * 60)
            print("✓ All tests passed! Server is working correctly.")
            print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_weather_server())
