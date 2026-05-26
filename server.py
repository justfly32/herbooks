#!/usr/bin/env python3
"""헤르 도서관 - Gutenberg proxy + data persistence + static file server"""
import http.server
import urllib.request
import json
import os
import io

PORT = 8080
DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(DIR, 'library_data.json')

def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"mybooks": [], "reviews": [], "favpoems": []}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIR, **kwargs)

    def _cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_OPTIONS(self):
        if self.path == '/data':
            self.send_response(204)
            self._cors_headers()
            self.end_headers()
            return
        return super().do_OPTIONS()

    def do_GET(self):
        if self.path == '/data':
            data = load_data()
            self.send_response(200)
            self._cors_headers()
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
            return

        if self.path.startswith('/proxy/gutenberg/'):
            gid = self.path.split('/proxy/gutenberg/')[1].split('/')[0]
            if not gid.isdigit():
                self.send_error(400, 'Invalid Gutenberg ID')
                return
            url = f'https://www.gutenberg.org/cache/epub/{gid}/pg{gid}.txt'
            try:
                req = urllib.request.Request(url, headers={
                    'User-Agent': 'HermesLibrary/1.0',
                    'Accept': 'text/plain, */*'
                })
                with urllib.request.urlopen(req, timeout=30) as resp:
                    text = resp.read().decode('utf-8', errors='replace')
                    start = text.find('*** START OF THE PROJECT GUTENBERG EBOOK')
                    end = text.find('*** END OF THE PROJECT GUTENBERG EBOOK')
                    if start >= 0:
                        start = text.index('***', text.index('***', start) + 3) + 4
                        text = text[start:]
                    if end >= 0:
                        text = text[:end]
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/plain; charset=utf-8')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header('Cache-Control', 'public, max-age=86400')
                    self.end_headers()
                    self.wfile.write(text.strip().encode('utf-8'))
            except Exception as e:
                self.send_response(502)
                self.send_header('Content-Type', 'text/plain; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(f'Proxy error: {e}'.encode('utf-8'))
            return

        return super().do_GET()

    def do_POST(self):
        if self.path == '/data':
            content_len = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_len)
            try:
                new_data = json.loads(body.decode('utf-8'))
                current = load_data()
                # Merge: preserve keys, merge arrays
                for key in ['mybooks', 'reviews', 'favpoems']:
                    if key in new_data:
                        current[key] = new_data[key]
                save_data(current)
                self.send_response(200)
                self._cors_headers()
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ok"}).encode('utf-8'))
            except Exception as e:
                self.send_response(400)
                self._cors_headers()
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
            return

        self.send_error(404)

if __name__ == '__main__':
    print(f'🚀 헤르 도서관 서버 시작 http://localhost:{PORT}')
    http.server.HTTPServer(('', PORT), Handler).serve_forever()