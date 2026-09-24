"""API endpoint for saving notes"""
import json
import os
from datetime import datetime
from http.server import BaseHTTPRequestHandler


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Read request body
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        # Load existing notes
        notes_file = 'notes.json'
        notes = []
        if os.path.exists(notes_file):
            try:
                with open(notes_file, 'r') as f:
                    notes = json.load(f)
            except:
                notes = []
        
        # Create new note
        note_id = max([n['id'] for n in notes], default=0) + 1
        new_note = {
            "id": note_id,
            "content": data.get("content", ""),
            "tags": data.get("tags", []),
            "timestamp": datetime.now().isoformat()
        }
        
        notes.append(new_note)
        
        # Save notes
        with open(notes_file, 'w') as f:
            json.dump(notes, f, indent=2)
        
        # Send response
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            "success": True,
            "message": f"Note saved with ID {note_id}",
            "note": new_note
        }
        self.wfile.write(json.dumps(response).encode())
