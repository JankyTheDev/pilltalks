# Deployment Guide

## Local Simulation

```bash
copy .env.example .env
python -m pilltalks.main --transport=stdin
```

## Example Bridge

Run the included bridge:

```bash
python examples/bridge_server.py
```

Then set these values in `.env`:

```text
TRANSPORT=pumpfun-live
PUMPFUN_STREAM_URL=http://127.0.0.1:8777/messages
PUMPFUN_SEND_URL=http://127.0.0.1:8777/send
PUMPFUN_API_KEY=demo-token
PUMPFUN_AUTH_HEADER=Authorization
PUMPFUN_AUTH_SCHEME=Bearer
PUMPFUN_POLL_INTERVAL_SECONDS=2.0
REPLY_COOLDOWN_SECONDS=8.0
ROOM_RATE_LIMIT_COUNT=4
ROOM_RATE_LIMIT_WINDOW_SECONDS=30.0
MESSAGE_HISTORY_SIZE=6
LOG_FORMAT=json
```

Start PillTalks:

```bash
python -m pilltalks.main --transport=pumpfun-live
```

Inject a demo message into the bridge:

```bash
curl -X POST http://127.0.0.1:8777/inject ^
  -H "Content-Type: application/json" ^
  -d "{\"roomId\":\"general\",\"userId\":\"user-2\",\"username\":\"alice\",\"text\":\"contract?\"}"
```

## Production Notes

- place a real authenticated bridge in front of any live platform integration
- keep API keys in environment variables only
- rate-limit outbound message posting
- preserve bot disclosure in production
- log bridge failures and monitor message backlog

## Bridge Auth Examples

Use the auth settings that match your bridge:

```text
# Standard bearer token
PUMPFUN_AUTH_HEADER=Authorization
PUMPFUN_AUTH_SCHEME=Bearer
PUMPFUN_API_KEY=your-token
```

```text
# Raw API key header
PUMPFUN_AUTH_HEADER=X-API-Key
PUMPFUN_AUTH_SCHEME=
PUMPFUN_API_KEY=your-token
```
