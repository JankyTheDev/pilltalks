from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os


@dataclass(slots=True)
class AppConfig:
    bot_name: str
    bot_disclosure: str
    bot_system_prompt: str
    project_name: str
    project_website: str | None
    project_x: str | None
    project_telegram: str | None
    contract_address: str | None
    allowed_rooms: list[str]
    ai_mode: str
    transport: str
    pumpfun_stream_url: str | None
    pumpfun_send_url: str | None
    pumpfun_api_key: str | None
    pumpfun_bot_user_id: str | None


def _load_dotenv() -> None:
    env_path = Path(".env")
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


def _get_env(name: str) -> str | None:
    value = os.environ.get(name)
    if value is None:
        return None
    value = value.strip()
    return value or None


def load_config(argv: list[str]) -> AppConfig:
    _load_dotenv()

    transport_arg = next((arg for arg in argv if arg.startswith("--transport=")), None)
    transport = transport_arg.split("=", 1)[1] if transport_arg else (_get_env("TRANSPORT") or "stdin")

    if transport not in {"stdin", "pumpfun-live"}:
        raise ValueError(f'Unsupported transport "{transport}". Use "stdin" or "pumpfun-live".')

    allowed_rooms = [room.strip() for room in (_get_env("ALLOWED_ROOMS") or "general").split(",") if room.strip()]

    return AppConfig(
        bot_name=_get_env("BOT_NAME") or "PillBot",
        bot_disclosure=_get_env("BOT_DISCLOSURE")
        or "PillBot is an automated account for public pump.fun chat support. Not financial advice.",
        bot_system_prompt=_get_env("BOT_SYSTEM_PROMPT")
        or "You are PillBot. You are a disclosed automated account. Be concise, useful, and never pretend to be human.",
        project_name=_get_env("PROJECT_NAME") or "Pill Project",
        project_website=_get_env("PROJECT_WEBSITE"),
        project_x=_get_env("PROJECT_X"),
        project_telegram=_get_env("PROJECT_TELEGRAM"),
        contract_address=_get_env("CONTRACT_ADDRESS"),
        allowed_rooms=allowed_rooms,
        ai_mode=_get_env("AI_MODE") or "template",
        transport=transport,
        pumpfun_stream_url=_get_env("PUMPFUN_STREAM_URL"),
        pumpfun_send_url=_get_env("PUMPFUN_SEND_URL"),
        pumpfun_api_key=_get_env("PUMPFUN_API_KEY"),
        pumpfun_bot_user_id=_get_env("PUMPFUN_BOT_USER_ID"),
    )
