from __future__ import annotations

import sys

from pilltalks.agent import PillTalksAgent
from pilltalks.config import load_config
from pilltalks.logging_utils import build_logger, log_event
from pilltalks.transports import ChatTransport, PumpfunLiveTransport, StdinTransport


def main() -> None:
    config = load_config(sys.argv[1:])
    logger = build_logger(level=config.log_level, log_format=config.log_format)
    agent = PillTalksAgent(
        bot_name=config.bot_name,
        bot_disclosure=config.bot_disclosure,
        bot_system_prompt=config.bot_system_prompt,
        project_name=config.project_name,
        project_website=config.project_website,
        project_x=config.project_x,
        project_telegram=config.project_telegram,
        contract_address=config.contract_address,
        allowed_rooms=config.allowed_rooms,
        ai_mode=config.ai_mode,
        bot_user_id=config.pumpfun_bot_user_id,
        reply_cooldown_seconds=config.reply_cooldown_seconds,
        room_rate_limit_count=config.room_rate_limit_count,
        room_rate_limit_window_seconds=config.room_rate_limit_window_seconds,
        message_history_size=config.message_history_size,
        logger=logger,
    )

    transport: ChatTransport
    if config.transport == "pumpfun-live":
        transport = PumpfunLiveTransport(
            stream_url=config.pumpfun_stream_url,
            send_url=config.pumpfun_send_url,
            api_key=config.pumpfun_api_key,
            poll_interval_seconds=config.pumpfun_poll_interval_seconds,
            auth_header=config.pumpfun_auth_header,
            auth_scheme=config.pumpfun_auth_scheme,
            logger=logger,
        )
    else:
        transport = StdinTransport()

    print(f'Starting {agent.describe()} on transport "{transport.name}"')

    def on_message(message) -> None:
        log_event(
            logger,
            "message.received",
            room_id=message.room_id,
            user_id=message.user_id,
            message_id=message.id,
        )
        reply = agent.handle_message(message)
        if reply is not None:
            log_event(
                logger,
                "message.replying",
                room_id=reply.room_id,
                reply_to_message_id=reply.reply_to_message_id,
            )
            transport.send_message(reply)
        else:
            log_event(
                logger,
                "message.ignored",
                room_id=message.room_id,
                user_id=message.user_id,
                message_id=message.id,
            )

    transport.connect(on_message)


if __name__ == "__main__":
    main()
