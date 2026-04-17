import json
import unittest
from unittest.mock import patch

from pilltalks.transports import PumpfunLiveTransport
from pilltalks.types import AgentReply


class MockResponse:
    def __init__(self, payload: object, status: int = 200) -> None:
        self._payload = payload
        self.status = status

    def read(self) -> bytes:
        return json.dumps(self._payload).encode("utf-8")

    def __enter__(self) -> "MockResponse":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        return None


class PumpfunLiveTransportTests(unittest.TestCase):
    def test_fetch_messages_accepts_messages_wrapper(self) -> None:
        transport = PumpfunLiveTransport(
            stream_url="https://bridge.example/messages",
            send_url="https://bridge.example/send",
            api_key="token",
            poll_interval_seconds=2.0,
            auth_header="Authorization",
        )

        with patch("pilltalks.transports.request.urlopen", return_value=MockResponse({"messages": [
            {
                "id": "1",
                "roomId": "general",
                "userId": "user-1",
                "username": "alice",
                "text": "help",
                "timestamp": "2026-04-17T00:00:00Z",
            }
        ]})):
            messages = transport._fetch_messages()

        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].username, "alice")

    def test_send_message_posts_expected_payload(self) -> None:
        transport = PumpfunLiveTransport(
            stream_url="https://bridge.example/messages",
            send_url="https://bridge.example/send",
            api_key="token",
            poll_interval_seconds=2.0,
            auth_header="Authorization",
        )
        captured = {}

        def fake_urlopen(req, timeout=0):
            captured["url"] = req.full_url
            captured["body"] = req.data.decode("utf-8")
            captured["auth"] = req.headers.get("Authorization")
            return MockResponse({"ok": True})

        with patch("pilltalks.transports.request.urlopen", side_effect=fake_urlopen):
            transport.send_message(AgentReply(room_id="general", text="hello", reply_to_message_id="1"))

        self.assertEqual(captured["url"], "https://bridge.example/send")
        self.assertEqual(captured["auth"], "token")
        self.assertIn('"roomId": "general"', captured["body"])

    def test_fetch_messages_rejects_invalid_payload_shape(self) -> None:
        transport = PumpfunLiveTransport(
            stream_url="https://bridge.example/messages",
            send_url="https://bridge.example/send",
            api_key="token",
            poll_interval_seconds=2.0,
            auth_header="Authorization",
        )

        with patch("pilltalks.transports.request.urlopen", return_value=MockResponse({"messages": {}})):
            with self.assertRaises(RuntimeError):
                transport._fetch_messages()


if __name__ == "__main__":
    unittest.main()
