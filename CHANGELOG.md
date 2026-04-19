# Changelog

## 1.0.2 - 2026-04-18

- bumped package version to 1.0.2
- refreshed release metadata for the next patch release

## 1.0.1 - 2026-04-17

- added configurable per-user cooldowns and per-room reply rate limiting
- added recent message history context for short follow-up questions like `link?`
- expanded moderation patterns for DM scams, wallet approval bait, and urgency tactics
- added structured logging with plain-text or JSON output modes
- added optional auth scheme support for bridges using headers like `Authorization: Bearer <token>`
- documented the new environment settings and common bridge authentication setups

## 1.0.0 - 2026-04-17

- created the initial PillTalks chat agent scaffold
- converted the runtime from TypeScript to Python
- renamed the project from PillBot to PillTalks
- added a performance-focused static landing page
- implemented a bridge-backed live transport contract
- added unit tests for agent and transport behavior
- added CI, security policy, contributing guide, and deployment documentation
