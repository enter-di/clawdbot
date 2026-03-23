"""Tests for the n8n webhook URL map."""

from openclaw.agent.tool_registry import TOOLS
from openclaw.n8n.webhook_map import WEBHOOK_MAP


def test_all_tools_have_webhook():
    """Every tool in the registry must have a corresponding webhook URL."""
    tool_names = {t["name"] for t in TOOLS}
    missing = tool_names - set(WEBHOOK_MAP.keys())
    assert not missing, f"Tools missing webhook URLs: {missing}"


def test_no_orphan_webhooks():
    """Every webhook URL must correspond to a known tool."""
    tool_names = {t["name"] for t in TOOLS}
    orphans = set(WEBHOOK_MAP.keys()) - tool_names
    assert not orphans, f"Webhook URLs with no matching tool: {orphans}"


def test_github_issue_webhook_registered():
    assert "create_github_issue" in WEBHOOK_MAP
    assert WEBHOOK_MAP["create_github_issue"].endswith("/webhook/github-issue-create")


def test_github_search_webhook_registered():
    assert "search_github" in WEBHOOK_MAP
    assert WEBHOOK_MAP["search_github"].endswith("/webhook/github-search")


def test_webhook_urls_are_non_empty_strings():
    for tool_name, url in WEBHOOK_MAP.items():
        assert isinstance(url, str) and url, f"Empty URL for tool '{tool_name}'"
