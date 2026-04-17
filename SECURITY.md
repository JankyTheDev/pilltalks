# Security Policy

## Scope

PillTalks is a disclosed chat agent for pump.fun-style community support. The repository includes:

- agent reply logic
- safety guardrails for obvious scam and secret-sharing prompts
- a bridge-backed live transport contract
- local simulation tooling

## Supported Versions

Only the current `main` branch is supported.

## Reporting a Vulnerability

Do not open public issues for suspected vulnerabilities that could expose users, secrets, bridge credentials, or deployment details.

Report security issues privately to:

- `security@pilltalks.example.invalid`

Include:

- affected file or module
- reproduction steps
- impact
- any proof-of-concept details needed to verify the issue

## Security Notes

- Never commit live credentials or `.env` files.
- Treat bridge endpoints and auth headers as secrets.
- Validate and rate-limit any live bridge you place in front of PillTalks.
- Keep bot disclosure enabled in production.
