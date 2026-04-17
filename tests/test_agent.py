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
        reply_cooldown_seconds=8.0,
        room_rate_limit_count=4,
        room_rate_limit_window_seconds=30.0,
        message_history_size=6,
        clock=lambda: 100.0,
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

    def test_follow_up_uses_recent_topic_history(self) -> None:
        clock_values = iter((100.0, 110.0, 120.0, 130.0))
        agent = build_agent()
        agent.clock = lambda: next(clock_values)

        first_reply = agent.handle_message(
            ChatMessage(
                id="4",
                room_id="general",
                user_id="user-4",
                username="dana",
                text="website?",
                timestamp="2026-04-17T00:00:00Z",
            )
        )
        follow_up = agent.handle_message(
            ChatMessage(
                id="5",
                room_id="general",
                user_id="user-5",
                username="erin",
                text="link?",
                timestamp="2026-04-17T00:00:01Z",
            )
        )

        self.assertIsNotNone(first_reply)
        self.assertIsNotNone(follow_up)
        self.assertIn("https://example.com", follow_up.text)

    def test_reply_cooldown_skips_repeat_user_prompt(self) -> None:
        clock_values = iter((100.0, 104.0))
        agent = build_agent()
        agent.clock = lambda: next(clock_values)

        first_reply = agent.handle_message(
            ChatMessage(
                id="6",
                room_id="general",
                user_id="user-6",
                username="frank",
                text="contract?",
                timestamp="2026-04-17T00:00:00Z",
            )
        )
        second_reply = agent.handle_message(
            ChatMessage(
                id="7",
                room_id="general",
                user_id="user-6",
                username="frank",
                text="website?",
                timestamp="2026-04-17T00:00:01Z",
            )
        )

        self.assertIsNotNone(first_reply)
        self.assertIsNone(second_reply)

    def test_room_rate_limit_caps_reply_volume(self) -> None:
        clock_values = iter((100.0, 105.0, 110.0))
        agent = PillTalksAgent(
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
            reply_cooldown_seconds=0.0,
            room_rate_limit_count=2,
            room_rate_limit_window_seconds=30.0,
            message_history_size=6,
            clock=lambda: next(clock_values),
        )

        reply_one = agent.handle_message(
            ChatMessage(
                id="8",
                room_id="general",
                user_id="user-8",
                username="gabe",
                text="contract?",
                timestamp="2026-04-17T00:00:00Z",
            )
        )
        reply_two = agent.handle_message(
            ChatMessage(
                id="9",
                room_id="general",
                user_id="user-9",
                username="hana",
                text="website?",
                timestamp="2026-04-17T00:00:01Z",
            )
        )
        reply_three = agent.handle_message(
            ChatMessage(
                id="10",
                room_id="general",
                user_id="user-10",
                username="ivan",
                text="telegram?",
                timestamp="2026-04-17T00:00:02Z",
            )
        )

        self.assertIsNotNone(reply_one)
        self.assertIsNotNone(reply_two)
        self.assertIsNone(reply_three)


if __name__ == "__main__":
    unittest.main()
