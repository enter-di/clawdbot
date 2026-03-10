# OpenClaw

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Docker](https://img.shields.io/badge/docker-compose-blue.svg)

Control your tools from Telegram using plain English. OpenClaw connects Claude AI to your workflows via n8n — send Slack messages, summarise emails, create Jira tickets, set reminders, and more by just typing what you want.

---

## Architecture

```
  You (Telegram)
       │
       ▼
 ┌─────────────┐     rate limit     ┌─────────┐
 │  Telegram   │◄──────────────────►│  Redis  │
 │     Bot     │   conversation     │(history)│
 └──────┬──────┘                    └─────────┘
        │
        ▼
 ┌──────────────────────────┐
 │      Claude Agent        │
 │   (Anthropic tool use)   │
 │                          │
 │  - send_slack_message    │
 │  - summarize_emails      │
 │  - create_jira_ticket    │
 │  - set_reminder          │
 │  - http_request          │
 └──────────────┬───────────┘
                │ HMAC-signed POST
                ▼
 ┌──────────────────────────┐
 │   n8n  (self-hosted)     │
 │   webhook workflows      │
 └──┬──────┬──────┬─────────┘
    │      │      │
  Slack  Gmail  Jira / ...
```

---

## Features

- **Natural language control** — just tell it what to do, Claude figures out the rest
- **Extensible** — add a new tool in 3 steps: tool schema + webhook map entry + n8n workflow
- **Secure** — HMAC-SHA256 signed webhook calls, per-user rate limiting, optional allowlist
- **Conversation memory** — Redis-backed history so Claude remembers context across messages
- **Docker-first** — single `docker compose up` to run everything

---

## Quick start

```bash
git clone https://github.com/yourusername/openclaw.git
cd openclaw
cp .env.example .env
# Fill in your tokens in .env
docker compose up --build -d
```

Then message your bot on Telegram.

---

## Example commands

```
Send a Slack message to #deployments saying v2.3.1 is live
Summarise my last 5 unread emails
Create a high priority bug in project BACKEND: login page crashes on mobile
Remind me at 9am tomorrow to review the pull requests
```

---

## Tech stack

| Layer | Technology |
|-------|-----------|
| Bot interface | python-telegram-bot 21 |
| AI agent | Anthropic Claude (tool use) |
| Workflow engine | n8n (self-hosted) |
| Conversation store | Redis |
| HTTP client | httpx + tenacity |
| Config validation | pydantic-settings |
| Logging | structlog (JSON) |
| Packaging | Docker + docker compose |

---

## Project structure

```
openclaw/
├── openclaw/
│   ├── agent/          # Claude agentic loop, tools, conversation history
│   ├── bot/            # Telegram handlers, middleware, keyboards
│   ├── n8n/            # Webhook client, tool→URL map, response parser
│   ├── security/       # HMAC signing, rate limiter, allowlist
│   └── utils/          # Logging, retry helpers
├── tests/              # Unit and integration tests
├── n8n_workflows/      # Importable n8n workflow JSON files
├── docker-compose.yml
├── Dockerfile
└── .env.example
```

---

## Configuration

Copy `.env.example` to `.env` and set:

| Variable | Description |
|----------|-------------|
| `TELEGRAM_BOT_TOKEN` | From [@BotFather](https://t.me/BotFather) |
| `ANTHROPIC_API_KEY` | From [console.anthropic.com](https://console.anthropic.com) |
| `N8N_WEBHOOK_SECRET` | Any random string — shared with n8n for request signing |
| `ALLOWED_USER_IDS` | Comma-separated Telegram user IDs (leave empty = open) |

---

## Adding a new tool

1. Add a tool definition to `openclaw/agent/tool_registry.py`
2. Add the webhook URL to `openclaw/n8n/webhook_map.py`
3. Build and activate the workflow in n8n, import from `n8n_workflows/`

---

## License

MIT
