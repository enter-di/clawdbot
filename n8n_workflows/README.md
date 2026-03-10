# n8n Workflows

Pre-built workflow JSON files for OpenClaw. Import these into your n8n instance to enable each tool.

## How to import

1. Open your n8n instance at `http://localhost:5678`
2. Go to **Workflows** → **Import from file**
3. Select the `.json` file for the workflow you want
4. Configure the credentials (Slack OAuth, Gmail OAuth, Jira API key, etc.)
5. Activate the workflow

## Workflows

| File | Tool | Webhook path |
|------|------|-------------|
| `slack_send_message.json` | `send_slack_message` | `/webhook/slack-send` |
| `gmail_summarize_inbox.json` | `summarize_emails` | `/webhook/gmail-summarize` |
| `jira_create_ticket.json` | `create_jira_ticket` | `/webhook/jira-create` |
| `reminder_set.json` | `set_reminder` | `/webhook/reminder-set` |
| `generic_http_request.json` | `http_request` | `/webhook/generic-http` |

## Security

Each workflow validates the `X-OpenClaw-Signature` header (HMAC-SHA256) using the shared `N8N_WEBHOOK_SECRET` from your `.env`.
Add a **Function** node at the start of each workflow to verify the signature before processing.
