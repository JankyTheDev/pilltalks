# Demo Walkthrough

## Local Agent Demo

1. Copy `.env.example` to `.env`
2. Run:

```bash
python -m pilltalks.main --transport=stdin
```

3. Example prompts:

- `pilltalks what is this?`
- `contract?`
- `website?`
- `seed phrase`

## Example Bridge Demo

1. Start the example bridge:

```bash
python examples/bridge_server.py
```

2. Set live bridge values in `.env`
3. Start PillTalks with:

```bash
python -m pilltalks.main --transport=pumpfun-live
```

4. Inject a test message into the bridge:

```bash
curl -X POST http://127.0.0.1:8777/inject ^
  -H "Content-Type: application/json" ^
  -d "{\"roomId\":\"general\",\"userId\":\"user-2\",\"username\":\"alice\",\"text\":\"website?\"}"
```

5. Watch PillTalks poll the bridge and submit the reply payload.

## Expected Behavior

- ignores its own messages when `PUMPFUN_BOT_USER_ID` is configured
- answers project FAQ prompts with configured values
- sends safety replies when messages mention sensitive topics like seed phrases
- keeps live-transport logic separated from the reply logic
