# PillBot

PillBot is a TypeScript chat agent built for `pump.fun`-style live community support. It responds to common questions in chat, shares configured project links, surfaces contract info, and applies basic safety checks around risky or scammy prompts.

The project already runs locally and includes a dedicated live transport module for pump.fun chat workflows.

## Features

- automated chat replies for common project questions
- configured responses for contract address, website, X, and Telegram
- safety checks for private-key, seed phrase, DM, and obvious scam language
- local terminal simulator for testing message flow end to end
- dedicated live transport layer for `pump.fun` chat workflows

## Boundaries

- PillBot should not impersonate a human.
- PillBot should not spam rooms or evade platform rules.
- PillBot does not provide financial advice.
- The included `pump.fun` live transport is built for real-time chat integration and deployment through your own bridge.

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

## Scripts

- `npm run dev`
- `npm run simulate`
- `npm run typecheck`
- `npm run build`

## Live Integration

The file `src/transports/pumpfunLiveTransport.ts` is the live transport module for pump.fun chat handling.

Once connected to your real bridge, PillBot can:

- receive incoming live chat messages
- decide whether a message needs a reply
- return a configured FAQ or safety response
- send the reply back through your bridge

Your bridge should:

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
- wire the live transport before advertising live support
