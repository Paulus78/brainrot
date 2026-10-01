"""Mini-Server mit CORS, damit der Browser lokale Referenzbilder in Web-Apps einfuegen kann.
Nimmt per POST /save?name=x.png auch Dateien entgegen (Bild-Download aus der Seite)."""
import http.server, os, sys, urllib.parse
ROOT = sys.argv[1]; PORT = int(sys.argv[2])
class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=ROOT, **k)
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Access-Control-Allow-Private-Network', 'true')
        super().end_headers()
    def do_OPTIONS(self):
        self.send_response(204); self.end_headers()
    def do_POST(self):
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        name = os.path.basename(q.get('name', ['upload.bin'])[0])
        n = int(self.headers.get('Content-Length', 0)); data = self.rfile.read(n)
        os.makedirs(os.path.join(ROOT, 'inbox'), exist_ok=True)
        with open(os.path.join(ROOT, 'inbox', name), 'wb') as f: f.write(data)
        self.send_response(200); self.end_headers(); self.wfile.write(b'ok')
    def log_message(self, *a): pass
http.server.ThreadingHTTPServer(('127.0.0.1', PORT), H).serve_forever()
