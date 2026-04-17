from __future__ import annotations

from collections import deque
from datetime import datetime, UTC
import json
from secrets import token_hex
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


MESSAGES = deque(
    [
        {
            "id": token_hex(8),
            "roomId": "general",
            "userId": "demo-user",
            "username": "demo-user",
            "text": "pilltalks what is this?",
            "timestamp": datetime.now(UTC).isoformat(),
        }
    ]
)

SENT_REPLIES: list[dict[str, object]] = []


class BridgeHandler(BaseHTTPRequestHandler):
    server_version = "PillTalksBridge/1.0"

    def do_GET(self) -> None:  # noqa: N802
        if self.path != "/messages":
            self.send_error(HTTPStatus.NOT_FOUND, "Unknown endpoint")
            return

        self._send_json({"messages": list(MESSAGES)})

    def do_POST(self) -> None:  # noqa: N802
        if self.path == "/send":
            body = self._read_json_body()
            SENT_REPLIES.append(body)
            self._send_json({"ok": True, "accepted": body}, status=HTTPStatus.CREATED)
            return

        if self.path == "/inject":
            body = self._read_json_body()
            message = {
                "id": str(body.get("id") or token_hex(8)),
                "roomId": str(body.get("roomId") or "general"),
                "userId": str(body.get("userId") or "demo-user"),
                "username": str(body.get("username") or "demo-user"),
                "text": str(body.get("text") or ""),
                "timestamp": str(body.get("timestamp") or datetime.now(UTC).isoformat()),
            }
            MESSAGES.append(message)
            self._send_json({"ok": True, "queued": message}, status=HTTPStatus.CREATED)
            return

        self.send_error(HTTPStatus.NOT_FOUND, "Unknown endpoint")

    def log_message(self, format: str, *args: object) -> None:
        return

    def _read_json_body(self) -> dict[str, object]:
        content_length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(content_length).decode("utf-8") if content_length else "{}"
        payload = json.loads(raw or "{}")
        if not isinstance(payload, dict):
            raise ValueError("JSON body must be an object.")
        return payload

    def _send_json(self, payload: dict[str, object], *, status: HTTPStatus = HTTPStatus.OK) -> None:
        encoded = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


def main() -> None:
    server = ThreadingHTTPServer(("127.0.0.1", 8777), BridgeHandler)
    print("PillTalks example bridge listening on http://127.0.0.1:8777")
    print("GET  /messages")
    print("POST /send")
    print("POST /inject")
    server.serve_forever()


if __name__ == "__main__":
    main()
