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


if __name__ == "__main__":
    unittest.main()
