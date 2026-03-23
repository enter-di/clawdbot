"""Tests for Telegram bot command handlers."""

import sys
import types
from unittest.mock import AsyncMock, MagicMock

import pytest

# ---------------------------------------------------------------------------
# Stub out the telegram package so tests run without the full library
# ---------------------------------------------------------------------------
_telegram = types.ModuleType("telegram")
_telegram.Update = MagicMock
_telegram_ext = types.ModuleType("telegram.ext")
_telegram_ext.ContextTypes = MagicMock()
_telegram_constants = types.ModuleType("telegram.constants")
_telegram_constants.ChatAction = MagicMock()
sys.modules.setdefault("telegram", _telegram)
sys.modules.setdefault("telegram.ext", _telegram_ext)
sys.modules.setdefault("telegram.constants", _telegram_constants)

# Now safe to import handlers
from openclaw.bot.handlers import status_command, WELCOME  # noqa: E402
from openclaw.agent.tool_registry import TOOLS  # noqa: E402


@pytest.mark.asyncio
async def test_status_command_replies_with_tool_count():
    update = MagicMock()
    update.message.reply_text = AsyncMock()
    context = MagicMock()

    await status_command(update, context)

    update.message.reply_text.assert_awaited_once()
    reply_text = update.message.reply_text.call_args[0][0]

    assert "OpenClaw Status" in reply_text
    assert f"Available tools ({len(TOOLS)})" in reply_text
    assert "Uptime:" in reply_text


@pytest.mark.asyncio
async def test_status_command_lists_github_tools():
    update = MagicMock()
    update.message.reply_text = AsyncMock()
    context = MagicMock()

    await status_command(update, context)

    reply_text = update.message.reply_text.call_args[0][0]
    assert "create_github_issue" in reply_text
    assert "search_github" in reply_text


def test_welcome_message_mentions_github():
    assert "GitHub" in WELCOME


def test_welcome_message_mentions_status_command():
    assert "/status" in WELCOME
