import socketserver
import http.server
import threading
from hyperiontf import getLogger

logger = getLogger("SimpleLocalHttpServer")


class SimpleHTTPServer:
    def __init__(self, path_to_serve, port=8000):
        self.path_to_serve = path_to_serve
        self.port = port
        self.httpd = None
        self.thread = None

    def start(self):
        Handler = http.server.SimpleHTTPRequestHandler
        Handler.directory = self.path_to_serve
        self.httpd = socketserver.TCPServer(("", self.port), Handler)
        self.thread = threading.Thread(target=self.httpd.serve_forever)
        self.thread.start()
        logger.info(f"Serving at http://localhost:{self.port}")

    def stop(self):
        if self.httpd:
            self.httpd.shutdown()
            self.thread.join()
            logger.info("Server stopped")
