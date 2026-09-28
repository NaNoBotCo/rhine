#!/usr/bin/env python3
"""serve.py — docs/ at http://localhost:<port>/rhine/, as GitHub Pages serves it."""
import functools
import http.server
import os
import sys
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"
os.chdir(DOCS)


class H(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        if path.startswith("/rhine"):
            path = path[len("/rhine"):] or "/"
        return super().translate_path(path)


port = int(sys.argv[1]) if len(sys.argv) > 1 else 8951
http.server.ThreadingHTTPServer(("127.0.0.1", port), functools.partial(H, directory=str(DOCS))).serve_forever()
