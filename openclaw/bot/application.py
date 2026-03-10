"""Build and configure the PTB Application."""

import redis.asyncio as aioredis
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from openclaw.agent.claude_agent import ClaudeAgent
from openclaw.agent.conversation import ConversationManager
from openclaw.bot.handlers import clear_command, handle_message, help_command, start
from openclaw.config import settings
from openclaw.security.rate_limiter import RateLimiter


def build_application() -> Application:
    redis_client = aioredis.from_url(settings.redis_url, decode_responses=True)
    conv_manager = ConversationManager(redis_client)
    rate_limiter = RateLimiter(redis_client)
    agent = ClaudeAgent(conv_manager)

    app = Application.builder().token(settings.telegram_bot_token).build()

    app.bot_data["redis"] = redis_client
    app.bot_data["conv_manager"] = conv_manager
    app.bot_data["rate_limiter"] = rate_limiter
    app.bot_data["agent"] = agent

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("clear", clear_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    return app
