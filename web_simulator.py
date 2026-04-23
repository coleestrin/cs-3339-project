import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from CPU import CPU

ROOT = Path(__file__).resolve().parent
HTML_FILE = ROOT / "mips_pipeline_simulator.html"


def list_asm_files():
    return sorted(path.name for path in ROOT.glob("*.asm"))


class SimulatorHandler(BaseHTTPRequestHandler):
    def _send_json(self, payload, status=200):
        encoded = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def _send_html(self):
        body = HTML_FILE.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in ("/", "/mips_pipeline_simulator.html"):
            self._send_html()
            return

        if self.path == "/api/files":
            self._send_json({"files": list_asm_files()})
            return

        requested = ROOT / self.path.lstrip("/")
        if requested.is_file() and requested.suffix == ".asm":
            body = requested.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        self._send_json({"error": "Not found"}, status=404)

    def do_POST(self):
        if self.path != "/api/simulate":
            self._send_json({"error": "Not found"}, status=404)
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(content_length)

        try:
            payload = json.loads(raw_body.decode("utf-8"))
            program_text = payload.get("program", "")
            debug = bool(payload.get("debug", False))

            if not program_text.strip():
                raise ValueError("Program text cannot be empty.")

            cpu = CPU(debug=debug, program_text=program_text)
            report = cpu.run()
            report["sourceFiles"] = list_asm_files()
            self._send_json(report)
        except Exception as exc:
            self._send_json({"error": str(exc)}, status=400)


def main():
    server = ThreadingHTTPServer(("0.0.0.0", 8000), SimulatorHandler)
    print("MIPS simulator UI available at http://localhost:8000 or http://0.0.0.0:8000")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
