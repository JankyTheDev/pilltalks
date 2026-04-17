from __future__ import annotations

from collections import defaultdict, deque
import logging
import re
import time

from pilltalks.types import AgentReply, ChatMessage


MAX_REPLY_LENGTH = 280
SAFETY_PATTERNS = [
    re.compile(r"private key", re.IGNORECASE),
    re.compile(r"seed phrase", re.IGNORECASE),
    re.compile(r"recovery phrase", re.IGNORECASE),
    re.compile(r"\bmnemonic\b", re.IGNORECASE),
    re.compile(r"send (me|us) sol", re.IGNORECASE),
    re.compile(r"send.*wallet", re.IGNORECASE),
    re.compile(r"guaranteed profit", re.IGNORECASE),
    re.compile(r"double your", re.IGNORECASE),
    re.compile(r"dev (dm|message) me", re.IGNORECASE),
    re.compile(r"dm (me|admin|team)", re.IGNORECASE),
    re.compile(r"connect.*wallet", re.IGNORECASE),
]
TOPIC_PATTERNS = {
    "contract": ("contract", "ca"),
    "website": ("website", "site", "link"),
    "x": ("twitter", "x.com", "x ", "x?", "social"),
    "telegram": ("telegram", "tg"),
    "buy": ("buy", "entry", "ape"),
}
FOLLOW_UP_PATTERNS = (
    "what about",
    "how about",
    "and that",
    "same for",
    "link?",
    "where?",
    "again",
    "repeat",
)


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
        reply_cooldown_seconds: float = 8.0,
        room_rate_limit_count: int = 4,
        room_rate_limit_window_seconds: float = 30.0,
        message_history_size: int = 6,
        logger: logging.Logger | None = None,
        clock: callable | None = None,
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
        self.reply_cooldown_seconds = max(0.0, reply_cooldown_seconds)
        self.room_rate_limit_count = max(1, room_rate_limit_count)
        self.room_rate_limit_window_seconds = max(1.0, room_rate_limit_window_seconds)
        self.message_history_size = max(1, message_history_size)
        self.logger = logger or logging.getLogger("pilltalks")
        self.clock = clock or time.monotonic
        self.recent_room_messages: dict[str, deque[ChatMessage]] = defaultdict(
            lambda: deque(maxlen=self.message_history_size)
        )
        self.room_reply_times: dict[str, deque[float]] = defaultdict(deque)
        self.user_reply_times: dict[tuple[str, str], float] = {}

    def describe(self) -> str:
        return f"{self.bot_name}: {self.bot_system_prompt}"

    def handle_message(self, message: ChatMessage) -> AgentReply | None:
        now = self.clock()
        if message.room_id not in self.allowed_rooms:
            return None
        if self.bot_user_id and message.user_id == self.bot_user_id:
            return None

        text = message.text.strip()
        if not text:
            return None
        self._remember_message(message)

        safety_reply = self._check_safety(text)
        if safety_reply:
            reply = AgentReply(
                room_id=message.room_id,
                text=safety_reply,
                reply_to_message_id=message.id,
            )
            self._record_reply(message, now)
            return reply

        lowered = text.lower()
        if not self._should_respond(lowered):
            return None
        if not self._can_reply(message, now):
            return None

        reply = AgentReply(
            room_id=message.room_id,
            text=self._compose_reply(message.username, text, lowered, message.room_id),
            reply_to_message_id=message.id,
        )
        self._record_reply(message, now)
        return reply

    def _check_safety(self, text: str) -> str | None:
        if any(pattern.search(text) for pattern in SAFETY_PATTERNS):
            return (
                f"{self.bot_disclosure} Never share keys, seed phrases, wallet approvals, or funds in chat or DMs. "
                "Use only official public links and ignore urgency tactics."
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
                "link",
                "again",
                "repeat",
            )
        ) or lowered in {"ca", "link?"}

    def _compose_reply(self, username: str, original: str, lowered: str, room_id: str) -> str:
        topic = self._detect_topic(lowered) or self._topic_from_history(room_id, lowered)

        if "what is this" in lowered:
            return f"{self.bot_disclosure} I answer basic {self.project_name} questions and public info in live chat."

        if topic == "contract":
            return (
                f"{self.bot_disclosure} {self.project_name} contract address: {self.contract_address}"
                if self.contract_address
                else f"{self.bot_disclosure} Contract address is not configured yet."
            )

        if topic == "website":
            return (
                f"{self.bot_disclosure} Website: {self.project_website}"
                if self.project_website
                else f"{self.bot_disclosure} Website is not configured yet."
            )

        if topic == "x":
            return (
                f"{self.bot_disclosure} X/Twitter: {self.project_x}"
                if self.project_x
                else f"{self.bot_disclosure} X/Twitter link is not configured yet."
            )

        if topic == "telegram":
            return (
                f"{self.bot_disclosure} Telegram: {self.project_telegram}"
                if self.project_telegram
                else f"{self.bot_disclosure} Telegram link is not configured yet."
            )

        if topic == "buy":
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

    def _remember_message(self, message: ChatMessage) -> None:
        history = self.recent_room_messages[message.room_id]
        if history.maxlen != self.message_history_size:
            history = deque(history, maxlen=self.message_history_size)
            self.recent_room_messages[message.room_id] = history
        history.append(message)

    def _can_reply(self, message: ChatMessage, now: float) -> bool:
        user_key = (message.room_id, message.user_id)
        last_reply_at = self.user_reply_times.get(user_key)
        if last_reply_at is not None and now - last_reply_at < self.reply_cooldown_seconds:
            return False

        room_times = self.room_reply_times[message.room_id]
        while room_times and now - room_times[0] > self.room_rate_limit_window_seconds:
            room_times.popleft()
        return len(room_times) < self.room_rate_limit_count

    def _record_reply(self, message: ChatMessage, now: float) -> None:
        self.user_reply_times[(message.room_id, message.user_id)] = now
        self.room_reply_times[message.room_id].append(now)

    def _detect_topic(self, lowered: str) -> str | None:
        for topic, tokens in TOPIC_PATTERNS.items():
            if any(token in lowered for token in tokens):
                return topic
        return None

    def _topic_from_history(self, room_id: str, lowered: str) -> str | None:
        if not any(token in lowered for token in FOLLOW_UP_PATTERNS):
            return None

        history = self.recent_room_messages.get(room_id, ())
        for message in reversed(list(history)[:-1]):
            topic = self._detect_topic(message.text.lower())
            if topic:
                return topic
        return None
