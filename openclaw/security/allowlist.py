"""Telegram user allowlist check."""

from openclaw.config import settings


def is_allowed_user(user_id: int) -> bool:
    """Return True if the user is permitted. Empty allowlist = open to all."""
    if not settings.allowed_user_ids:
        return True
    return user_id in settings.allowed_user_ids
