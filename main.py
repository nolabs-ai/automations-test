#!/usr/bin/env python3
"""Simple webserver using only the Python standard library.

Usage:
    python3 server.py            # serves on port 8080
    python3 server.py 3000       # serves on port 3000
"""

import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self._send(200, "text/html", "<h1>Hello from Python!</h1>")
        elif self.path == "/health":
            self._send(200, "application/json", json.dumps({"status": "ok"}))
        else:
            self._send(404, "text/plain", "Not found")

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8")
        self._send(200, "application/json", json.dumps({"received": body}))

    def _send(self, status, content_type, body):
        data = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    print(f"Serving on http://localhost:{port} (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
        server.server_close()


if __name__ == "__main__":
    main()
