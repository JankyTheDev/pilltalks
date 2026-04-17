# PillBot

PillBot is a GitHub-ready TypeScript scaffold for a disclosed `pump.fun` chat agent. It is built to answer common live-chat questions, share configured project links, and enforce basic safety reminders while keeping the real platform integration isolated behind a transport boundary.

## Features

- disclosed bot identity for public chat use
- FAQ-style responses for contract address, website, X, and Telegram
- safety replies for key-sharing, DM, and obvious scam prompts
- local terminal simulator for testing without touching a live room
- live transport scaffold for wiring your own compliant `pump.fun` websocket or API bridge

## Boundaries

- PillBot should not impersonate a human.
- PillBot should not spam rooms or evade platform rules.
- PillBot does not provide financial advice.
- The included live `pump.fun` transport is a scaffold only. You still need a real bridge you control.

## Stack

- TypeScript
- Node.js
- `tsx` for local execution
- `dotenv` for environment-based config

## Project Structure

```text
src/
  agent/
    pillBotAgent.ts
    types.ts
  transports/
    chatTransport.ts
    pumpfunLiveTransport.ts
    stdinTransport.ts
  config.ts
  index.ts
```

## Quick Start

```bash
npm install
copy .env.example .env
npm run simulate
```

Then edit `.env` with your real project values.

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

## Scripts

- `npm run dev`
- `npm run simulate`
- `npm run typecheck`
- `npm run build`

## Live Integration

The file `src/transports/pumpfunLiveTransport.ts` is the only place you need to wire a live bridge.

That bridge should:

- connect to the live chat feed
- normalize incoming events into the shared `ChatMessage` shape
- send replies back through your approved send path
- ignore PillBot's own messages
- respect platform rate limits and room rules

## Publish Checklist

- fill in `.env` locally
- keep `.env` out of git
- review bot disclosure text
- replace placeholder project links and contract data
- wire the live transport before claiming live support
