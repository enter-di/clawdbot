"""Tests for the rate limiter."""

import pytest
from openclaw.security.rate_limiter import RateLimiter


@pytest.mark.asyncio
async def test_allows_within_limit(mock_redis):
    mock_redis.incr.return_value = 1
    limiter = RateLimiter(mock_redis)
    assert await limiter.is_allowed(12345) is True


@pytest.mark.asyncio
async def test_blocks_over_limit(mock_redis):
    mock_redis.incr.return_value = 999
    limiter = RateLimiter(mock_redis)
    assert await limiter.is_allowed(12345) is False
