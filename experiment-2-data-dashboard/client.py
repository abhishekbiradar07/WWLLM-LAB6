"""
Data Dashboard Client
Connects to the MCP server and allows natural language weather queries.
"""

import os
import asyncio
from dotenv import load_dotenv
from openai import OpenAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def run_weather_assistant():
    """Main weather assistant loop."""
    
    # Connect to MCP server
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()
            
            # Get available tools
            tools_list = await session.list_tools()
            
            # Convert MCP tools to OpenAI function format
            openai_tools = []
            for tool in tools_list.tools:
                openai_tools.append({
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.inputSchema
                    }
                })
            
            print("=" * 60)
            print("Weather Data Dashboard")
            print("=" * 60)
            print("Ask me about the weather in any city!")
            print("Type 'quit' or 'exit' to stop.\n")
            
            # Conversation loop
            messages = []
            
            while True:
                # Get user input
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['quit', 'exit']:
                    print("Goodbye!")
                    break
                
                if not user_input:
                    continue
                
                # Add user message
                messages.append({
                    "role": "user",
                    "content": user_input
                })
                
                print("\n[LLM] Determining required tool...")
                
                # Call OpenAI with function calling
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    tools=openai_tools,
                    tool_choice="auto"
                )
                
                assistant_message = response.choices[0].message
                
                # Check if tool calls are needed
                if assistant_message.tool_calls:
                    # Add assistant message with tool calls
                    messages.append({
                        "role": "assistant",
                        "content": assistant_message.content,
                        "tool_calls": [
                            {
                                "id": tc.id,
                                "type": "function",
                                "function": {
                                    "name": tc.function.name,
                                    "arguments": tc.function.arguments
                                }
                            }
                            for tc in assistant_message.tool_calls
                        ]
                    })
                    
                    # Execute each tool call
                    for tool_call in assistant_message.tool_calls:
                        import json
                        function_name = tool_call.function.name
                        function_args = json.loads(tool_call.function.arguments)
                        
                        print(f"[LLM] Calling MCP tool: {function_name}")
                        
                        # Call MCP tool
                        result = await session.call_tool(function_name, function_args)
                        
                        # Add tool result to messages
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": result.content[0].text
                        })
                    
                    print("[LLM] Generating final response...")
                    
                    # Get final response from OpenAI
                    final_response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=messages
                    )
                    
                    final_message = final_response.choices[0].message.content
                    messages.append({
                        "role": "assistant",
                        "content": final_message
                    })
                    
                    print(f"\nAssistant: {final_message}\n")
                else:
                    # Direct response without tool calls
                    messages.append({
                        "role": "assistant",
                        "content": assistant_message.content
                    })
                    print(f"\nAssistant: {assistant_message.content}\n")


if __name__ == "__main__":
    asyncio.run(run_weather_assistant())
