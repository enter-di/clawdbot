"""Telegram bot command and message handlers."""

import time

from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

from openclaw.agent.claude_agent import ClaudeAgent
from openclaw.agent.conversation import ConversationManager
from openclaw.agent.tool_registry import TOOLS
from openclaw.bot.middleware import check_access
from openclaw.security.rate_limiter import RateLimiter
from openclaw.utils.logging import get_logger

logger = get_logger(__name__)

_START_TIME = time.time()

WELCOME = """
Hey! I'm *OpenClaw* — your personal AI automation assistant.

Tell me what you want to do in plain English and I'll handle it:

• Send a Slack message to #general
• Summarise my unread emails
• Create a Jira ticket for...
• Remind me tomorrow at 9am to...
• Search GitHub for a repo
• Create a GitHub issue in owner/repo
• Make an HTTP request to...

*Commands:*
/help — show this message
/status — show bot status and available tools
/clear — reset our conversation
""".strip()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(WELCOME, parse_mode="Markdown")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(WELCOME, parse_mode="Markdown")


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    uptime_seconds = int(time.time() - _START_TIME)
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    uptime_str = f"{hours}h {minutes}m {seconds}s"

    tool_list = "\n".join(f"• `{t['name']}`" for t in TOOLS)
    text = (
        f"*OpenClaw Status*\n\n"
        f"Uptime: {uptime_str}\n\n"
        f"*Available tools ({len(TOOLS)}):*\n{tool_list}"
    )
    await update.message.reply_text(text, parse_mode="Markdown")


async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    conv_manager: ConversationManager = context.bot_data["conv_manager"]
    chat_id = update.effective_chat.id
    await conv_manager.clear(chat_id)
    await update.message.reply_text("Conversation history cleared.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    rate_limiter: RateLimiter = context.bot_data["rate_limiter"]
    agent: ClaudeAgent = context.bot_data["agent"]

    if not await check_access(update, rate_limiter):
        return

    await update.message.chat.send_action(ChatAction.TYPING)

    chat_id = update.effective_chat.id
    user_message = update.message.text

    logger.info("message_received", chat_id=chat_id, length=len(user_message))

    try:
        reply = await agent.run(user_message, chat_id)
    except Exception as exc:
        logger.error("agent_error", error=str(exc), chat_id=chat_id)
        reply = "Something went wrong on my end. Please try again."

    await update.message.reply_text(reply)
