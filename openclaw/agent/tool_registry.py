"""Claude tool definitions — each tool maps to an n8n webhook workflow."""

from typing import Any

TOOLS: list[dict[str, Any]] = [
    {
        "name": "send_slack_message",
        "description": "Send a Slack message to a channel or user.",
        "input_schema": {
            "type": "object",
            "properties": {
                "recipient": {
                    "type": "string",
                    "description": "Channel name (e.g. #general) or @username",
                },
                "message": {
                    "type": "string",
                    "description": "The message text to send",
                },
            },
            "required": ["recipient", "message"],
        },
    },
    {
        "name": "summarize_emails",
        "description": (
            "Fetch unread emails from Gmail and return their details. "
            "You will then summarise them for the user."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "max_count": {
                    "type": "integer",
                    "description": "Maximum number of emails to fetch",
                    "default": 5,
                },
                "label": {
                    "type": "string",
                    "description": "Gmail label to filter by",
                    "default": "INBOX",
                },
            },
            "required": [],
        },
    },
    {
        "name": "create_jira_ticket",
        "description": "Create a new issue in a Jira project.",
        "input_schema": {
            "type": "object",
            "properties": {
                "project_key": {
                    "type": "string",
                    "description": "Jira project key, e.g. PROJ",
                },
                "summary": {
                    "type": "string",
                    "description": "One-line ticket title",
                },
                "description": {
                    "type": "string",
                    "description": "Detailed description of the issue",
                },
                "issue_type": {
                    "type": "string",
                    "enum": ["Task", "Bug", "Story"],
                    "default": "Task",
                },
                "priority": {
                    "type": "string",
                    "enum": ["Low", "Medium", "High"],
                    "default": "Medium",
                },
            },
            "required": ["project_key", "summary"],
        },
    },
    {
        "name": "set_reminder",
        "description": "Schedule a reminder message to be delivered at a specific date and time.",
        "input_schema": {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "What to remind the user about",
                },
                "remind_at": {
                    "type": "string",
                    "description": "ISO 8601 datetime, e.g. 2025-03-15T09:00:00",
                },
                "timezone": {
                    "type": "string",
                    "description": "IANA timezone, e.g. Asia/Singapore",
                    "default": "UTC",
                },
            },
            "required": ["message", "remind_at"],
        },
    },
    {
        "name": "http_request",
        "description": (
            "Make an HTTP GET or POST request to an external public API. "
            "Do NOT use this for private IPs or localhost."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The full URL to request",
                },
                "method": {
                    "type": "string",
                    "enum": ["GET", "POST"],
                    "default": "GET",
                },
                "headers": {
                    "type": "object",
                    "description": "Optional HTTP headers as key-value pairs",
                },
                "body": {
                    "type": "object",
                    "description": "Optional JSON body for POST requests",
                },
            },
            "required": ["url"],
        },
    },
]
