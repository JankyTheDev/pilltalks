from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, UTC
import json
from secrets import token_hex
import time
from typing import Any
from urllib import request

from pilltalks.types import AgentReply, ChatMessage


class ChatTransport(ABC):
    name: str

    @abstractmethod
    def connect(self, on_message: callable) -> None:
        raise NotImplementedError

    @abstractmethod
    def send_message(self, reply: AgentReply) -> None:
        raise NotImplementedError


class StdinTransport(ChatTransport):
    name = "stdin"

    def connect(self, on_message: callable) -> None:
        print("PillTalks local simulation started. Use Ctrl+C to stop.")
        while True:
            try:
                line = input("user> ")
            except (EOFError, KeyboardInterrupt):
                print()
                return

            message = ChatMessage(
                id=token_hex(16),
                room_id="general",
                user_id="local-user",
                username="local-user",
                text=line,
                timestamp=datetime.now(UTC).isoformat(),
            )
            on_message(message)

    def send_message(self, reply: AgentReply) -> None:
        print(f"{reply.room_id}> pilltalks> {reply.text}")


class PumpfunLiveTransport(ChatTransport):
    name = "pumpfun-live"

    def __init__(
        self,
        *,
        stream_url: str | None,
        send_url: str | None,
        api_key: str | None,
        poll_interval_seconds: float,
        auth_header: str,
    ) -> None:
        self.stream_url = stream_url
        self.send_url = send_url
        self.api_key = api_key
        self.poll_interval_seconds = max(0.25, poll_interval_seconds)
        self.auth_header = auth_header
        self.seen_message_ids: set[str] = set()

    def connect(self, on_message: callable) -> None:
        if not self.stream_url:
            raise RuntimeError(
                "PUMPFUN_STREAM_URL is required for live mode."
            )

        while True:
            for message in self._fetch_messages():
                if message.id in self.seen_message_ids:
                    continue
                self.seen_message_ids.add(message.id)
                on_message(message)

            time.sleep(self.poll_interval_seconds)

    def send_message(self, reply: AgentReply) -> None:
        if not self.send_url or not self.api_key:
            raise RuntimeError(
                "PUMPFUN_SEND_URL and PUMPFUN_API_KEY are required for live replies."
            )

        payload = json.dumps(
            {
                "roomId": reply.room_id,
                "text": reply.text,
                "replyToMessageId": reply.reply_to_message_id,
            }
        ).encode("utf-8")

        headers = {
            "Content-Type": "application/json",
            self.auth_header: self.api_key,
        }
        http_request = request.Request(
            self.send_url,
            data=payload,
            headers=headers,
            method="POST",
        )

        with request.urlopen(http_request, timeout=15) as response:
            if response.status >= 400:
                raise RuntimeError(f"Bridge send failed with HTTP {response.status}.")

    def _fetch_messages(self) -> list[ChatMessage]:
        headers = {}
        if self.api_key:
            headers[self.auth_header] = self.api_key

        http_request = request.Request(self.stream_url, headers=headers, method="GET")
        with request.urlopen(http_request, timeout=15) as response:
            if response.status >= 400:
                raise RuntimeError(f"Bridge fetch failed with HTTP {response.status}.")
            payload = json.loads(response.read().decode("utf-8"))

        items = payload.get("messages", payload) if isinstance(payload, dict) else payload
        if not isinstance(items, list):
            raise RuntimeError("Bridge fetch must return a JSON array or an object with a 'messages' array.")

        return [self._coerce_message(item) for item in items]

    def _coerce_message(self, item: Any) -> ChatMessage:
        if not isinstance(item, dict):
            raise RuntimeError("Each bridge message must be a JSON object.")

        return ChatMessage(
            id=str(item["id"]),
            room_id=str(item["roomId"]),
            user_id=str(item["userId"]),
            username=str(item["username"]),
            text=str(item["text"]),
            timestamp=str(item.get("timestamp") or datetime.now(UTC).isoformat()),
        )
