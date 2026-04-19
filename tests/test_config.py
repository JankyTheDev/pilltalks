import os
import unittest
from unittest.mock import patch

from pilltalks.config import load_config


class ConfigTests(unittest.TestCase):
    def test_cli_transport_overrides_env(self) -> None:
        with patch.dict(os.environ, {"TRANSPORT": "stdin"}, clear=True):
            config = load_config(["--transport=pumpfun-live"])
        self.assertEqual(config.transport, "pumpfun-live")

    def test_defaults_are_applied(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            config = load_config([])
        self.assertEqual(config.bot_name, "PillTalks")
        self.assertEqual(config.pumpfun_poll_interval_seconds, 2.0)
        self.assertEqual(config.pumpfun_auth_header, "Authorization")
        self.assertEqual(config.reply_cooldown_seconds, 8.0)
        self.assertEqual(config.room_rate_limit_count, 4)
        self.assertEqual(config.message_history_size, 6)
        self.assertEqual(config.log_format, "plain")

    def test_extended_settings_are_loaded(self) -> None:
        with patch.dict(
            os.environ,
            {
                "PUMPFUN_AUTH_SCHEME": "Bearer",
                "REPLY_COOLDOWN_SECONDS": "3.5",
                "ROOM_RATE_LIMIT_COUNT": "2",
                "ROOM_RATE_LIMIT_WINDOW_SECONDS": "10",
                "MESSAGE_HISTORY_SIZE": "9",
                "LOG_LEVEL": "debug",
                "LOG_FORMAT": "json",
            },
            clear=True,
        ):
            config = load_config([])

        self.assertEqual(config.pumpfun_auth_scheme, "Bearer")
        self.assertEqual(config.reply_cooldown_seconds, 3.5)
        self.assertEqual(config.room_rate_limit_count, 2)
        self.assertEqual(config.room_rate_limit_window_seconds, 10.0)
        self.assertEqual(config.message_history_size, 9)
        self.assertEqual(config.log_level, "DEBUG")
        self.assertEqual(config.log_format, "json")

    def test_allowed_rooms_wildcard_is_loaded(self) -> None:
        with patch.dict(os.environ, {"ALLOWED_ROOMS": "*"}, clear=True):
            config = load_config([])

        self.assertEqual(config.allowed_rooms, ["*"])


if __name__ == "__main__":
    unittest.main()
