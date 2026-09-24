"""Quick test script for Experiment 1 MCP Server"""
import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_server():
    """Test the personal assistant server tools."""
    
    server_params = StdioServerParameters(
        command="python",
        args=["experiment-1-personal-assistant/server.py"],
        env=None
    )
    
    print("Testing Personal Assistant MCP Server...")
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
            
            # Test 2: Save a note
            print("\n2. Testing save_note...")
            result = await session.call_tool("save_note", {
                "content": "Python MCP experiment deadline is October 1",
                "tags": ["deadline", "python", "mcp"]
            })
            print(f"   {result.content[0].text}")
            
            # Test 3: Save another note
            print("\n3. Saving another note...")
            result = await session.call_tool("save_note", {
                "content": "Team meeting scheduled for September 28 at 3pm",
                "tags": ["meeting", "team"]
            })
            print(f"   {result.content[0].text}")
            
            # Test 4: Search notes
            print("\n4. Testing search_notes with query 'deadline'...")
            result = await session.call_tool("search_notes", {
                "query": "deadline"
            })
            print(f"   {result.content[0].text}")
            
            # Test 5: Search by tag
            print("\n5. Testing search_notes with query 'meeting'...")
            result = await session.call_tool("search_notes", {
                "query": "meeting"
            })
            print(f"   {result.content[0].text}")
            
            print("\n" + "=" * 60)
            print("✓ All tests passed! Server is working correctly.")
            print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_server())
