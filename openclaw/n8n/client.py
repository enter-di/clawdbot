"""Async HTTP client for calling n8n webhook URLs."""

import json

import httpx

from openclaw.config import settings
from openclaw.n8n.response_parser import parse_n8n_response
from openclaw.n8n.webhook_map import WEBHOOK_MAP
from openclaw.security.signature import sign_payload
from openclaw.utils.logging import get_logger
from openclaw.utils.retry import n8n_retry

logger = get_logger(__name__)

_client: httpx.AsyncClient | None = None


def get_http_client() -> httpx.AsyncClient:
    global _client
    if _client is None or _client.is_closed:
        _client = httpx.AsyncClient(timeout=30.0)
    return _client


async def close_http_client() -> None:
    global _client
    if _client and not _client.is_closed:
        await _client.aclose()


@n8n_retry
async def invoke_tool(tool_name: str, payload: dict) -> str:  # type: ignore[type-arg]
    """
    POST a tool invocation to the corresponding n8n webhook.
    Returns a string result suitable for feeding back to Claude as a tool_result.
    """
    url = WEBHOOK_MAP.get(tool_name)
    if not url:
        raise ValueError(f"No webhook URL registered for tool '{tool_name}'")

    body = json.dumps(payload).encode()
    signature = sign_payload(settings.n8n_webhook_secret, body)

    headers = {
        "Content-Type": "application/json",
        "X-OpenClaw-Signature": signature,
        "X-OpenClaw-Tool": tool_name,
    }

    logger.info("invoking_n8n_tool", tool=tool_name, url=url)

    client = get_http_client()
    response = await client.post(url, content=body, headers=headers)
    response.raise_for_status()

    result = response.json()
    logger.info("n8n_tool_response", tool=tool_name, status=response.status_code)

    return parse_n8n_response(tool_name, result)
