from http.server import BaseHTTPRequestHandler
from services.fetch import fetch
from services.shared.constants import NEW_NORFOLK_BOUNDING_BOX
from services.fetch import BoundingBox


bounding_box = BoundingBox(name="NewNorfolk", shape=NEW_NORFOLK_BOUNDING_BOX)


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            fetch(bounding_box)
            self.send_response(200)
            self.wfile.write(f"Success".encode("utf-8"))
        except Exception as e:
            self.send_response(500)
            self.wfile.write(str(e).encode("utf-8"))
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        return
