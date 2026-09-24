"""API endpoint for getting weather data"""
import json
import urllib.request
import urllib.error
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse query parameters
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        location = params.get('location', [''])[0]
        
        if not location:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Location parameter required"}).encode())
            return
        
        # Fetch weather data
        try:
            url = f"https://wttr.in/{urllib.parse.quote(location)}?format=j1"
            with urllib.request.urlopen(url, timeout=10) as response:
                data = json.loads(response.read().decode())
            
            current = data['current_condition'][0]
            
            weather_data = {
                "success": True,
                "location": location,
                "temperature": f"{current['temp_C']}°C",
                "condition": current['weatherDesc'][0]['value'],
                "humidity": f"{current['humidity']}%",
                "wind": f"{current['windspeedKmph']} km/h",
                "feels_like": f"{current['FeelsLikeC']}°C"
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(weather_data).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
