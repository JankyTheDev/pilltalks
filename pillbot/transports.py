from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, UTC
from secrets import token_hex

from pillbot.types import AgentReply, ChatMessage


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
        print("PillBot local simulation started. Use Ctrl+C to stop.")
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
        print(f"{reply.room_id}> pillbot> {reply.text}")


class PumpfunLiveTransport(ChatTransport):
    name = "pumpfun-live"

    def __init__(self, *, stream_url: str | None, send_url: str | None, api_key: str | None) -> None:
        self.stream_url = stream_url
        self.send_url = send_url
        self.api_key = api_key

    def connect(self, on_message: callable) -> None:
        del on_message
        if not self.stream_url:
            raise RuntimeError(
                "PUMPFUN_STREAM_URL is required for live mode. Replace connect() with your bridge implementation."
            )
        raise RuntimeError(
            "Pumpfun live transport is a Python integration point. Replace connect() with your websocket or event bridge."
        )

    def send_message(self, reply: AgentReply) -> None:
        del reply
        if not self.send_url or not self.api_key:
            raise RuntimeError(
                "PUMPFUN_SEND_URL and PUMPFUN_API_KEY are required for live replies. Replace send_message() with your bridge implementation."
            )
        raise RuntimeError(
            "Pumpfun live transport send_message() is not implemented yet. Connect it to your approved send path."
        )
