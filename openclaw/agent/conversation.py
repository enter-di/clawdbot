"""Redis-backed per-user conversation history manager."""

import json
from typing import Any

import redis.asyncio as aioredis

from openclaw.config import settings
from openclaw.utils.logging import get_logger

logger = get_logger(__name__)


class ConversationManager:
    def __init__(self, redis_client: aioredis.Redis) -> None:
        self._redis = redis_client
        self._max = settings.max_messages_per_history
        self._ttl = 60 * 60 * 24  # 24 hours

    def _key(self, chat_id: int) -> str:
        return f"conv:{chat_id}"

    async def load(self, chat_id: int) -> list[dict[str, Any]]:
        raw = await self._redis.get(self._key(chat_id))
        if not raw:
            return []
        return json.loads(raw)

    async def append(self, chat_id: int, role: str, content: Any) -> None:
        history = await self.load(chat_id)
        history.append({"role": role, "content": content})
        # Trim to max, always keeping pairs to avoid orphaned tool_results
        if len(history) > self._max:
            history = history[-self._max :]
        await self._redis.set(self._key(chat_id), json.dumps(history), ex=self._ttl)

    async def clear(self, chat_id: int) -> None:
        await self._redis.delete(self._key(chat_id))
        logger.info("conversation_cleared", chat_id=chat_id)
