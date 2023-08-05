from http.server import BaseHTTPRequestHandler
from services.fetch import fetch


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        message = fetch()
        self.wfile.write(f"Hello, world! ${message}".encode("utf-8"))
        return
