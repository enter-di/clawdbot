"""Maps Claude tool names to their n8n webhook URLs."""

from openclaw.config import settings

WEBHOOK_MAP: dict[str, str] = {
    "send_slack_message": f"{settings.n8n_base_url}/webhook/slack-send",
    "summarize_emails": f"{settings.n8n_base_url}/webhook/gmail-summarize",
    "create_jira_ticket": f"{settings.n8n_base_url}/webhook/jira-create",
    "set_reminder": f"{settings.n8n_base_url}/webhook/reminder-set",
    "http_request": f"{settings.n8n_base_url}/webhook/generic-http",
    "create_github_issue": f"{settings.n8n_base_url}/webhook/github-issue-create",
    "search_github": f"{settings.n8n_base_url}/webhook/github-search",
}
