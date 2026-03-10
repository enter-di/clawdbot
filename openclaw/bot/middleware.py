"""Access control middleware: allowlist + rate limiting."""

from telegram import Update

from openclaw.security.allowlist import is_allowed_user
from openclaw.security.rate_limiter import RateLimiter
from openclaw.utils.logging import get_logger

logger = get_logger(__name__)


async def check_access(update: Update, rate_limiter: RateLimiter) -> bool:
    """Return True if the request should be processed."""
    user = update.effective_user
    chat = update.effective_chat

    if user is None or chat is None:
        return False

    if not is_allowed_user(user.id):
        logger.warning("unauthorised_user", user_id=user.id)
        await update.message.reply_text("Sorry, you are not authorised to use this bot.")
        return False

    if not await rate_limiter.is_allowed(chat.id):
        logger.warning("rate_limited", chat_id=chat.id)
        await update.message.reply_text(
            "You are sending messages too fast. Please wait a moment."
        )
        return False

    return True
