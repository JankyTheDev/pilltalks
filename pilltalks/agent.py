from __future__ import annotations

import re

from pilltalks.types import AgentReply, ChatMessage


MAX_REPLY_LENGTH = 280
SAFETY_PATTERNS = [
    re.compile(r"private key", re.IGNORECASE),
    re.compile(r"seed phrase", re.IGNORECASE),
    re.compile(r"send (me|us) sol", re.IGNORECASE),
    re.compile(r"guaranteed profit", re.IGNORECASE),
]


class PillTalksAgent:
    def __init__(
        self,
        *,
        bot_name: str,
        bot_disclosure: str,
        bot_system_prompt: str,
        project_name: str,
        project_website: str | None,
        project_x: str | None,
        project_telegram: str | None,
        contract_address: str | None,
        allowed_rooms: list[str],
        ai_mode: str,
        bot_user_id: str | None,
    ) -> None:
        self.bot_name = bot_name
        self.bot_disclosure = bot_disclosure
        self.bot_system_prompt = bot_system_prompt
        self.project_name = project_name
        self.project_website = project_website
        self.project_x = project_x
        self.project_telegram = project_telegram
        self.contract_address = contract_address
        self.allowed_rooms = set(allowed_rooms)
        self.ai_mode = ai_mode
        self.bot_user_id = bot_user_id

    def describe(self) -> str:
        return f"{self.bot_name}: {self.bot_system_prompt}"

    def handle_message(self, message: ChatMessage) -> AgentReply | None:
        if message.room_id not in self.allowed_rooms:
            return None
        if self.bot_user_id and message.user_id == self.bot_user_id:
            return None

        text = message.text.strip()
        if not text:
            return None

        safety_reply = self._check_safety(text)
        if safety_reply:
            return AgentReply(
                room_id=message.room_id,
                text=safety_reply,
                reply_to_message_id=message.id,
            )

        lowered = text.lower()
        if not self._should_respond(lowered):
            return None

        return AgentReply(
            room_id=message.room_id,
            text=self._compose_reply(message.username, text, lowered),
            reply_to_message_id=message.id,
        )

    def _check_safety(self, text: str) -> str | None:
        if any(pattern.search(text) for pattern in SAFETY_PATTERNS):
            return (
                f"{self.bot_disclosure} Never share keys, seed phrases, or funds in chat or DMs. "
                "Use only official public links."
            )
        return None

    def _should_respond(self, lowered: str) -> bool:
        return any(
            token in lowered
            for token in (
                "pilltalks",
                "help",
                "what is this",
                "contract",
                "website",
                "twitter",
                "x.com",
                "telegram",
                "tg",
                "buy",
                "launch",
                "where",
                "how",
            )
        ) or lowered == "ca"

    def _compose_reply(self, username: str, original: str, lowered: str) -> str:
        if "what is this" in lowered:
            return f"{self.bot_disclosure} I answer basic {self.project_name} questions and public info in live chat."

        if "contract" in lowered or lowered == "ca":
            return (
                f"{self.bot_disclosure} {self.project_name} contract address: {self.contract_address}"
                if self.contract_address
                else f"{self.bot_disclosure} Contract address is not configured yet."
            )

        if "website" in lowered:
            return (
                f"{self.bot_disclosure} Website: {self.project_website}"
                if self.project_website
                else f"{self.bot_disclosure} Website is not configured yet."
            )

        if "twitter" in lowered or "x.com" in lowered:
            return (
                f"{self.bot_disclosure} X/Twitter: {self.project_x}"
                if self.project_x
                else f"{self.bot_disclosure} X/Twitter link is not configured yet."
            )

        if "telegram" in lowered or "tg" in lowered:
            return (
                f"{self.bot_disclosure} Telegram: {self.project_telegram}"
                if self.project_telegram
                else f"{self.bot_disclosure} Telegram link is not configured yet."
            )

        if "buy" in lowered:
            return f"{self.bot_disclosure} I can point to public project links and contract info, but I do not give buy or sell advice."

        if self.ai_mode == "template":
            reply = (
                f'{self.bot_disclosure} {username}, I can help with {self.project_name} links, '
                f'contract lookup, launch basics, and chat safety. You asked: "{original}"'
            )
            if len(reply) <= MAX_REPLY_LENGTH:
                return reply

        return (
            f"{self.bot_disclosure} {username}, I can help with {self.project_name} links, "
            "contract lookup, launch basics, and chat safety."
        )
