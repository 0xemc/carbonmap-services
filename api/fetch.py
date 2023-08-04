from http.server import BaseHTTPRequestHandler
from services.fetch import fetch
from services.shared.constants import NEW_NORFOLK_BOUNDING_BOX


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        message = fetch(NEW_NORFOLK_BOUNDING_BOX)
        self.wfile.write(f"Hello, world! ${message}".encode("utf-8"))
        return
