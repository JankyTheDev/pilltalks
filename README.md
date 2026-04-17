# PillTalks

PillTalks is a Python chat agent built for `pump.fun`-style live community support. It responds to common questions in chat, shares configured project links, surfaces contract info, and applies basic safety checks around risky or scammy prompts.

The project already runs locally and includes a dedicated live transport module for pump.fun chat workflows.

## At a Glance

- [Deployment guide](DEPLOYMENT.md)
- [Demo walkthrough](docs/demo.md)
- [Roadmap](ROADMAP.md)
- [Changelog](CHANGELOG.md)
- [Security policy](SECURITY.md)
- [Contributing guide](CONTRIBUTING.md)

## Features

- automated chat replies for common project questions
- configured responses for contract address, website, X, and Telegram
- safety checks for private-key, seed phrase, DM, and obvious scam language
- local terminal simulator for testing message flow end to end
- dedicated live transport layer for `pump.fun` chat workflows
- bridge-backed polling transport for live integration without framework lock-in
- unit tests for core reply and transport behavior
- GitHub Actions CI for every push and pull request

## Boundaries

- PillTalks should not impersonate a human.
- PillTalks should not spam rooms or evade platform rules.
- PillTalks does not provide financial advice.
- The included `pump.fun` live transport is built for real-time chat integration and deployment through your own bridge.

## Stack

- Python
- standard library runtime
- local `.env` loading without third-party config packages

## Project Structure

```text
pilltalks/
  agent.py
  config.py
  main.py
  transports.py
  types.py
examples/
  bridge_server.py
tests/
  test_agent.py
  test_transports.py
```

## Quick Start

```bash
copy .env.example .env
python -m pilltalks.main --transport=stdin
```

Then edit `.env` with your real project values and test the bot in the terminal before enabling live transport settings.

## Environment

- `BOT_NAME`
- `BOT_DISCLOSURE`
- `BOT_SYSTEM_PROMPT`
- `PROJECT_NAME`
- `PROJECT_WEBSITE`
- `PROJECT_X`
- `PROJECT_TELEGRAM`
- `CONTRACT_ADDRESS`
- `ALLOWED_ROOMS`
- `AI_MODE=off|template`
- `TRANSPORT=stdin|pumpfun-live`
- `PUMPFUN_STREAM_URL`
- `PUMPFUN_SEND_URL`
- `PUMPFUN_API_KEY`
- `PUMPFUN_BOT_USER_ID`
- `PUMPFUN_POLL_INTERVAL_SECONDS`
- `PUMPFUN_AUTH_HEADER`

## Run Modes

- `python -m pilltalks.main --transport=stdin`
- `python -m pilltalks.main --transport=pumpfun-live`
- `python -m unittest discover -s tests -v`
- `python examples/bridge_server.py`

## Live Integration

The file `pilltalks/transports.py` contains the live transport module for pump.fun chat handling.

Once connected to your real bridge, PillTalks can:

- receive incoming live chat messages
- decide whether a message needs a reply
- return a configured FAQ or safety response
- send the reply back through your bridge

The included bridge contract now supports:

- `GET PUMPFUN_STREAM_URL` returning either a JSON array of messages or `{ "messages": [...] }`
- `POST PUMPFUN_SEND_URL` with `roomId`, `text`, and optional `replyToMessageId`
- configurable auth header name and polling interval

Your bridge should:

- connect to the live chat feed
- normalize incoming events into the shared `ChatMessage` shape
- send replies back through your approved send path
- ignore PillTalks' own messages
- respect platform rate limits and room rules

## Repo Trust Signals

- MIT licensed
- explicit `SECURITY.md`
- explicit `CONTRIBUTING.md`
- explicit `DEPLOYMENT.md`
- explicit `ROADMAP.md`
- explicit `docs/demo.md`
- explicit `CHANGELOG.md`
- CI workflow in `.github/workflows/ci.yml`
- issue templates in `.github/ISSUE_TEMPLATE/`
- unit tests in `tests/`
- no hardcoded secrets; environment-driven configuration only

## Release Notes

Current release focus:

- stable Python runtime
- documented bridge contract
- test-covered core reply logic
- example bridge for local development
- fast static landing page for public project presentation

## Publish Checklist

- fill in `.env` locally
- keep `.env` out of git
- review bot disclosure text
- replace placeholder project links and contract data
- wire the live transport before advertising live support
