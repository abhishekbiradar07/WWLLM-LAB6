"""
Personal Assistant Memory Server - MCP Server Implementation
Provides tools for storing and searching personal notes.
"""

import json
import os
from datetime import datetime
from typing import Any
from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio

# File to store notes
NOTES_FILE = "notes.json"

# Initialize the MCP server
app = Server("personal-assistant")


def load_notes() -> list[dict[str, Any]]:
    """Load notes from JSON file."""
    if not os.path.exists(NOTES_FILE):
        return []
    try:
        with open(NOTES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_notes(notes: list[dict[str, Any]]) -> None:
    """Save notes to JSON file."""
    with open(NOTES_FILE, 'w', encoding='utf-8') as f:
        json.dump(notes, f, indent=2, ensure_ascii=False)


def get_next_id(notes: list[dict[str, Any]]) -> int:
    """Generate next note ID."""
    if not notes:
        return 1
    return max(note['id'] for note in notes) + 1


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="save_note",
            description="Save a new note with content and tags",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "The content of the note"
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of tags for categorizing the note"
                    }
                },
                "required": ["content", "tags"]
            }
        ),
        Tool(
            name="search_notes",
            description="Search notes by query string (searches content and tags)",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query to find matching notes"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_note",
            description="Get a specific note by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "note_id": {
                        "type": "integer",
                        "description": "The ID of the note to retrieve"
                    }
                },
                "required": ["note_id"]
            }
        ),
        Tool(
            name="delete_note",
            description="Delete a note by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "note_id": {
                        "type": "integer",
                        "description": "The ID of the note to delete"
                    }
                },
                "required": ["note_id"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls."""
    
    if name == "save_note":
        # Load existing notes
        notes = load_notes()
        
        # Create new note
        new_note = {
            "id": get_next_id(notes),
            "content": arguments["content"],
            "tags": arguments["tags"],
            "timestamp": datetime.now().isoformat()
        }
        
        # Add and save
        notes.append(new_note)
        save_notes(notes)
        
        return [TextContent(
            type="text",
            text=f"✓ Note saved successfully with ID {new_note['id']}"
        )]
    
    elif name == "search_notes":
        # Load notes
        notes = load_notes()
        query = arguments["query"].lower()
        
        # Simple case-insensitive search
        matching_notes = []
        for note in notes:
            # Search in content
            if query in note["content"].lower():
                matching_notes.append(note)
                continue
            
            # Search in tags
            if any(query in tag.lower() for tag in note["tags"]):
                matching_notes.append(note)
        
        if not matching_notes:
            return [TextContent(
                type="text",
                text="No notes found matching your query."
            )]
        
        # Format results
        result = f"Found {len(matching_notes)} note(s):\n\n"
        for note in matching_notes:
            result += f"ID: {note['id']}\n"
            result += f"Content: {note['content']}\n"
            result += f"Tags: {', '.join(note['tags'])}\n"
            result += f"Date: {note['timestamp']}\n"
            result += "-" * 50 + "\n"
        
        return [TextContent(type="text", text=result)]
    
    elif name == "get_note":
        notes = load_notes()
        note_id = arguments["note_id"]
        
        # Find note by ID
        note = next((n for n in notes if n["id"] == note_id), None)
        
        if not note:
            return [TextContent(
                type="text",
                text=f"Note with ID {note_id} not found."
            )]
        
        result = f"ID: {note['id']}\n"
        result += f"Content: {note['content']}\n"
        result += f"Tags: {', '.join(note['tags'])}\n"
        result += f"Date: {note['timestamp']}"
        
        return [TextContent(type="text", text=result)]
    
    elif name == "delete_note":
        notes = load_notes()
        note_id = arguments["note_id"]
        
        # Find and remove note
        original_count = len(notes)
        notes = [n for n in notes if n["id"] != note_id]
        
        if len(notes) == original_count:
            return [TextContent(
                type="text",
                text=f"Note with ID {note_id} not found."
            )]
        
        save_notes(notes)
        return [TextContent(
            type="text",
            text=f"✓ Note {note_id} deleted successfully."
        )]
    
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
