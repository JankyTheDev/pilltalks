import unittest

from pilltalks.agent import PillTalksAgent
from pilltalks.types import ChatMessage


def build_agent() -> PillTalksAgent:
    return PillTalksAgent(
        bot_name="PillTalks",
        bot_disclosure="PillTalks is an automated account.",
        bot_system_prompt="Be concise.",
        project_name="Pill Project",
        project_website="https://example.com",
        project_x="https://x.com/example",
        project_telegram="https://t.me/example",
        contract_address="ABC123",
        allowed_rooms=["general"],
        ai_mode="template",
        bot_user_id="bot-user",
    )


class PillTalksAgentTests(unittest.TestCase):
    def test_safety_reply_blocks_seed_phrase(self) -> None:
        agent = build_agent()
        reply = agent.handle_message(
            ChatMessage(
                id="1",
                room_id="general",
                user_id="user-1",
                username="alice",
                text="here is my seed phrase",
                timestamp="2026-04-17T00:00:00Z",
            )
        )
        self.assertIsNotNone(reply)
        self.assertIn("Never share keys", reply.text)

    def test_contract_reply_uses_configured_value(self) -> None:
        agent = build_agent()
        reply = agent.handle_message(
            ChatMessage(
                id="2",
                room_id="general",
                user_id="user-2",
                username="bob",
                text="contract?",
                timestamp="2026-04-17T00:00:00Z",
            )
        )
        self.assertIsNotNone(reply)
        self.assertIn("ABC123", reply.text)

    def test_ignores_bot_messages(self) -> None:
        agent = build_agent()
        reply = agent.handle_message(
            ChatMessage(
                id="3",
                room_id="general",
                user_id="bot-user",
                username="pilltalks",
                text="help",
                timestamp="2026-04-17T00:00:00Z",
            )
        )
        self.assertIsNone(reply)


if __name__ == "__main__":
    unittest.main()
