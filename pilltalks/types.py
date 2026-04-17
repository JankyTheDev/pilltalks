from dataclasses import dataclass


@dataclass(slots=True)
class ChatMessage:
    id: str
    room_id: str
    user_id: str
    username: str
    text: str
    timestamp: str


@dataclass(slots=True)
class AgentReply:
    room_id: str
    text: str
    reply_to_message_id: str | None = None
