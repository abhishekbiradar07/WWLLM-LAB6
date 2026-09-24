"""
Data Dashboard Connector - MCP Server Implementation
Provides tools for retrieving real-time weather information.
"""

import urllib.request
import urllib.error
import json
from typing import Any
from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio

# Initialize the MCP server
app = Server("data-dashboard")


def get_weather_data(location: str) -> dict[str, str]:
    """
    Fetch weather data from wttr.in API.
    Returns a dictionary with weather information.
    """
    try:
        # Use wttr.in API with format parameter for JSON output
        url = f"https://wttr.in/{urllib.parse.quote(location)}?format=j1"
        
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
        
        # Extract current conditions
        current = data['current_condition'][0]
        
        return {
            "location": location,
            "temperature": f"{current['temp_C']}°C",
            "condition": current['weatherDesc'][0]['value'],
            "humidity": f"{current['humidity']}%",
            "wind": f"{current['windspeedKmph']} km/h",
            "feels_like": f"{current['FeelsLikeC']}°C"
        }
    
    except urllib.error.HTTPError as e:
        return {
            "error": f"Location not found: {location}",
            "status": str(e.code)
        }
    except urllib.error.URLError:
        return {
            "error": "Network error: Unable to connect to weather service",
            "status": "connection_failed"
        }
    except (KeyError, json.JSONDecodeError) as e:
        return {
            "error": f"Failed to parse weather data: {str(e)}",
            "status": "parse_error"
        }
    except Exception as e:
        return {
            "error": f"Unexpected error: {str(e)}",
            "status": "unknown_error"
        }


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="get_current_weather",
            description="Get current weather information for a specific location",
            inputSchema={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City or location name (e.g., 'Tokyo', 'New York', 'London')"
                    }
                },
                "required": ["location"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls."""
    
    if name == "get_current_weather":
        location = arguments["location"]
        
        print(f"[MCP] Fetching weather for {location}...")
        
        # Get weather data
        weather = get_weather_data(location)
        
        # Check for errors
        if "error" in weather:
            return [TextContent(
                type="text",
                text=f"Error: {weather['error']}"
            )]
        
        # Format response
        result = f"Location: {weather['location']}\n"
        result += f"Temperature: {weather['temperature']}\n"
        result += f"Feels Like: {weather['feels_like']}\n"
        result += f"Condition: {weather['condition']}\n"
        result += f"Humidity: {weather['humidity']}\n"
        result += f"Wind Speed: {weather['wind']}"
        
        print("[MCP] Tool result received.")
        
        return [TextContent(type="text", text=result)]
    
    else:
        return [TextContent(
            type="text",
            text=f"Unknown tool: {name}"
        )]


async def main():
    """Run the MCP server."""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
