#!/usr/bin/env python3
"""Serve the live PRD tracker for a PRD.md file.

The page polls PRD.md every 2 seconds, so checkboxes ticked by a build agent
(or by hand in an editor) appear on their own. Clicking a checkbox in the page
writes the change back to PRD.md.

Usage: serve_tracker.py [PRD.md] [--port 4747] [--open]
"""
import argparse
import html
import json
import re
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Lock

TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "prd-viewer.html"
TASK_RE = re.compile(r"^(\s*(?:[-*+]|\d+\.)\s+\[)([ xX])(\]\s*)(.*)$")
write_lock = Lock()


def make_handler(prd: Path):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_):
            pass

        def send(self, code, body, ctype="text/plain; charset=utf-8", headers=None):
            data = body.encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "no-store")
            for k, v in (headers or {}).items():
                self.send_header(k, v)
            self.end_headers()
            self.wfile.write(data)

        def version(self):
            st = prd.stat()
            return f"{st.st_mtime_ns}-{st.st_size}"

        def do_GET(self):
            path = self.path.split("?")[0]
            if path == "/api/prd":
                return self.send(200, prd.read_text(encoding="utf-8"), "text/markdown; charset=utf-8",
                                 {"X-PRD-Version": self.version()})
            if path in ("/", "/index.html"):
                md = prd.read_text(encoding="utf-8")
                m = re.search(r"^#\s+(.+)$", md, re.M)
                page = TEMPLATE.read_text(encoding="utf-8")
                page = page.replace("{{PRD_TITLE}}", html.escape(m.group(1).strip() if m else prd.stem))
                page = page.replace("{{PRD_MARKDOWN}}", re.sub(r"</(script)", r"<\\/\1", md, flags=re.I))
                return self.send(200, page, "text/html; charset=utf-8")
            self.send(404, "not found")

        def do_POST(self):
            if self.path != "/api/toggle":
                return self.send(404, "not found")
            # Only accept requests from this page, not from other sites open in the browser.
            origin = self.headers.get("Origin")
            if origin and origin != f"http://{self.headers.get('Host')}":
                return self.send(403, "forbidden origin")
            try:
                req = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
                line, text, checked = int(req["line"]), str(req["text"]), bool(req["checked"])
            except (ValueError, KeyError, TypeError):
                return self.send(400, "bad request")
            with write_lock:
                lines = prd.read_text(encoding="utf-8").split("\n")
                # The file may have changed since the page loaded; find the task by text near its old line.
                candidates = sorted(range(len(lines)), key=lambda i: abs(i - line))
                for i in candidates:
                    m = TASK_RE.match(lines[i])
                    if m and m.group(4).strip() == text:
                        lines[i] = m.group(1) + ("x" if checked else " ") + m.group(3) + m.group(4)
                        prd.write_text("\n".join(lines), encoding="utf-8")
                        return self.send(200, "ok")
            self.send(409, "task not found in PRD.md")

    return Handler


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("prd", nargs="?", default="PRD.md")
    ap.add_argument("--port", type=int, default=4747)
    ap.add_argument("--open", action="store_true", help="open the tracker in the default browser")
    args = ap.parse_args()
    prd = Path(args.prd).resolve()
    if not prd.is_file():
        raise SystemExit(f"{prd} not found")
    server = ThreadingHTTPServer(("127.0.0.1", args.port), make_handler(prd))
    url = f"http://127.0.0.1:{args.port}/"
    print(f"PRD tracker for {prd} at {url} (Ctrl+C to stop)")
    if args.open:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
