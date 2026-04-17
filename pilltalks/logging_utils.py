from __future__ import annotations

from datetime import datetime, UTC
import json
import logging


def build_logger(*, level: str, log_format: str) -> logging.Logger:
    logger = logging.getLogger("pilltalks")
    logger.handlers.clear()
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    logger.propagate = False

    handler = logging.StreamHandler()
    if log_format == "json":
        handler.setFormatter(logging.Formatter("%(message)s"))
    else:
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.addHandler(handler)
    return logger


def log_event(logger: logging.Logger, event: str, **fields: object) -> None:
    payload = {
        "ts": datetime.now(UTC).isoformat(),
        "event": event,
        **fields,
    }

    if any(getattr(handler.formatter, "_fmt", "") == "%(message)s" for handler in logger.handlers):
        logger.info(json.dumps(payload, separators=(",", ":"), sort_keys=True))
        return

    field_text = " ".join(f"{key}={value!r}" for key, value in sorted(fields.items()))
    message = event if not field_text else f"{event} {field_text}"
    logger.info(message)
