"""Tests for cache utilities."""

import time
from src.utils.cache import CacheManager, RateLimiter


class TestCacheManager:
    """Test cases for CacheManager class."""

    def test_cache_initialization(self):
        """Test cache manager initialization."""
        cache = CacheManager(maxsize=10, ttl=60)
        assert cache.enabled is True
        assert cache.hits == 0
        assert cache.misses == 0

    def test_cache_set_and_get(self):
        """Test setting and getting cache values."""
        cache = CacheManager(maxsize=10, ttl=60)

        cache.set("key1", "value1")
        result = cache.get("key1")

        assert result == "value1"
        assert cache.hits == 1
        assert cache.misses == 0

    def test_cache_miss(self):
        """Test cache miss."""
        cache = CacheManager(maxsize=10, ttl=60)

        result = cache.get("nonexistent")

        assert result is None
        assert cache.hits == 0
        assert cache.misses == 1

    def test_cache_ttl_expiration(self):
        """Test cache TTL expiration."""
        cache = CacheManager(maxsize=10, ttl=1)  # 1 second TTL

        cache.set("key1", "value1")
        assert cache.get("key1") == "value1"

        # Wait for TTL to expire
        time.sleep(1.5)

        result = cache.get("key1")
        assert result is None

    def test_cache_clear(self):
        """Test clearing cache."""
        cache = CacheManager(maxsize=10, ttl=60)

        cache.set("key1", "value1")
        cache.set("key2", "value2")
        cache.get("key1")  # Generate a hit

        cache.clear()

        # After clear, stats are reset
        assert cache.hits == 0
        assert cache.misses == 0
        
        # Verify cache is empty (this will increment misses)
        result = cache.get("key1")
        assert result is None
        assert cache.misses == 1  # One miss from the get after clear

    def test_cache_disable(self):
        """Test disabling cache."""
        cache = CacheManager(maxsize=10, ttl=60)

        cache.set("key1", "value1")
        cache.disable()

        result = cache.get("key1")
        assert result is None

    def test_cache_enable(self):
        """Test enabling cache."""
        cache = CacheManager(maxsize=10, ttl=60)

        cache.disable()
        cache.set("key1", "value1")
        assert cache.get("key1") is None

        cache.enable()
        cache.set("key2", "value2")
        assert cache.get("key2") == "value2"

    def test_cache_stats(self):
        """Test cache statistics."""
        cache = CacheManager(maxsize=10, ttl=60)

        cache.set("key1", "value1")
        cache.get("key1")  # Hit
        cache.get("key2")  # Miss

        stats = cache.get_stats()

        assert stats["enabled"] is True
        assert stats["size"] == 1
        assert stats["maxsize"] == 10
        assert stats["ttl"] == 60
        assert stats["hits"] == 1
        assert stats["misses"] == 1
        assert "50.00%" in stats["hit_rate"]

    def test_cache_maxsize(self):
        """Test cache max size limit."""
        cache = CacheManager(maxsize=2, ttl=60)

        cache.set("key1", "value1")
        cache.set("key2", "value2")
        cache.set("key3", "value3")  # Should evict oldest

        stats = cache.get_stats()
        assert stats["size"] <= 2


class TestRateLimiter:
    """Test cases for RateLimiter class."""

    def test_rate_limiter_initialization(self):
        """Test rate limiter initialization."""
        limiter = RateLimiter(max_calls=5, period=10)
        assert limiter.max_calls == 5
        assert limiter.period == 10
        assert len(limiter.calls) == 0

    def test_rate_limiter_allows_calls(self):
        """Test rate limiter allows calls under limit."""
        limiter = RateLimiter(max_calls=3, period=10)

        assert limiter.is_allowed() is True
        assert limiter.is_allowed() is True
        assert limiter.is_allowed() is True

    def test_rate_limiter_blocks_excess_calls(self):
        """Test rate limiter blocks calls over limit."""
        limiter = RateLimiter(max_calls=2, period=10)

        assert limiter.is_allowed() is True
        assert limiter.is_allowed() is True
        assert limiter.is_allowed() is False

    def test_rate_limiter_wait_time(self):
        """Test rate limiter wait time calculation."""
        limiter = RateLimiter(max_calls=2, period=5)

        limiter.is_allowed()
        limiter.is_allowed()

        wait_time = limiter.wait_time()
        assert wait_time > 0
        assert wait_time <= 5

    def test_rate_limiter_reset(self):
        """Test rate limiter reset."""
        limiter = RateLimiter(max_calls=2, period=10)

        limiter.is_allowed()
        limiter.is_allowed()
        assert limiter.is_allowed() is False

        limiter.reset()
        assert limiter.is_allowed() is True

    def test_rate_limiter_period_expiration(self):
        """Test rate limiter allows calls after period expires."""
        limiter = RateLimiter(max_calls=2, period=1)

        assert limiter.is_allowed() is True
        assert limiter.is_allowed() is True
        assert limiter.is_allowed() is False

        # Wait for period to expire
        time.sleep(1.5)

        assert limiter.is_allowed() is True

    def test_rate_limiter_no_wait_when_allowed(self):
        """Test rate limiter returns 0 wait time when calls allowed."""
        limiter = RateLimiter(max_calls=5, period=10)

        limiter.is_allowed()
        wait_time = limiter.wait_time()

        assert wait_time == 0.0


# Made with Bob
