"""Shared pytest fixtures."""

import pytest
from unittest.mock import AsyncMock, MagicMock


@pytest.fixture
def mock_redis():
    client = AsyncMock()
    client.get = AsyncMock(return_value=None)
    client.set = AsyncMock()
    client.delete = AsyncMock()
    client.incr = AsyncMock(return_value=1)
    client.expire = AsyncMock()
    return client


@pytest.fixture
def mock_anthropic_client():
    return MagicMock()
