from __future__ import annotations

import sys

from pilltalks.agent import PillTalksAgent
from pilltalks.config import load_config
from pilltalks.transports import ChatTransport, PumpfunLiveTransport, StdinTransport


def main() -> None:
    config = load_config(sys.argv[1:])
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
    )

    transport: ChatTransport
    if config.transport == "pumpfun-live":
        transport = PumpfunLiveTransport(
            stream_url=config.pumpfun_stream_url,
            send_url=config.pumpfun_send_url,
            api_key=config.pumpfun_api_key,
        )
    else:
        transport = StdinTransport()

    print(f'Starting {agent.describe()} on transport "{transport.name}"')

    def on_message(message) -> None:
        reply = agent.handle_message(message)
        if reply is not None:
            transport.send_message(reply)

    transport.connect(on_message)


if __name__ == "__main__":
    main()
