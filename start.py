"""
VisionLens - Local Server + API Proxy
Run: python start.py
"""
import http.server
import socketserver
import webbrowser
import os
import json
import urllib.request
import urllib.error

PORT = 8000
DIR  = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIR, **kwargs)

    def log_message(self, format, *args):
        pass  # silence logs

    def send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, x-api-key, anthropic-version')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()

    def do_POST(self):
        if self.path == '/proxy':
            try:
                length = int(self.headers.get('Content-Length', 0))
                body   = self.rfile.read(length)
                data   = json.loads(body)

                api_key = data.get('apiKey', '')
                payload = data.get('payload', {})

                req = urllib.request.Request(
                    'https://api.anthropic.com/v1/messages',
                    data=json.dumps(payload).encode(),
                    headers={
                        'Content-Type': 'application/json',
                        'x-api-key': api_key,
                        'anthropic-version': '2023-06-01',
                    },
                    method='POST'
                )

                with urllib.request.urlopen(req) as resp:
                    result = resp.read()

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(result)

            except urllib.error.HTTPError as e:
                error_body = e.read()
                self.send_response(e.code)
                self.send_header('Content-Type', 'application/json')
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(error_body)

            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({'error': {'message': str(e)}}).encode())
        else:
            self.send_response(404)
            self.end_headers()

print("=" * 50)
print("  VisionLens — Multimodal LLM Demo")
print("=" * 50)
print(f"\n  Server running at: http://localhost:{PORT}")
print("  Opening browser...")
print("\n  Press Ctrl+C to stop.\n")

webbrowser.open(f'http://localhost:{PORT}')

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n  Server stopped.")
