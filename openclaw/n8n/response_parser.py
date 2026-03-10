"""Normalises n8n JSON payloads into agent-readable strings."""

import json

MAX_RESPONSE_CHARS = 4000


def parse_n8n_response(tool_name: str, payload: dict) -> str:  # type: ignore[type-arg]
    """Convert an n8n webhook response into a concise string for Claude."""
    serialised = json.dumps(payload, ensure_ascii=False)

    if len(serialised) > MAX_RESPONSE_CHARS:
        serialised = serialised[:MAX_RESPONSE_CHARS] + "... [truncated]"

    return serialised
