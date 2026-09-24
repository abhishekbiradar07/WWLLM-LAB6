"""API endpoint for searching notes"""
import json
import os
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse query parameters
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        query = params.get('query', [''])[0].lower()
        
        # Load notes
        notes_file = 'notes.json'
        notes = []
        if os.path.exists(notes_file):
            try:
                with open(notes_file, 'r') as f:
                    notes = json.load(f)
            except:
                notes = []
        
        # Search notes
        matching_notes = []
        for note in notes:
            if query in note["content"].lower() or any(query in tag.lower() for tag in note["tags"]):
                matching_notes.append(note)
        
        # Send response
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            "success": True,
            "count": len(matching_notes),
            "notes": matching_notes
        }
        self.wfile.write(json.dumps(response).encode())
