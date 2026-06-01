"""Caching utilities for API responses."""
import time
from typing import Any, Optional, Callable
from functools import wraps
from cachetools import TTLCache
import logging

logger = logging.getLogger(__name__)


class CacheManager:
    """Manage caching for API responses with TTL support."""
    
    def __init__(self, maxsize: int = 100, ttl: int = 3600):
        """
        Initialize cache manager.
        
        Args:
            maxsize: Maximum number of items in cache
            ttl: Time to live in seconds
        """
        self.cache = TTLCache(maxsize=maxsize, ttl=ttl)
        self.enabled = True
        self.hits = 0
        self.misses = 0
        logger.info(f"Cache initialized: maxsize={maxsize}, ttl={ttl}s")
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found
        """
        if not self.enabled:
            return None
            
        try:
            value = self.cache.get(key)
            if value is not None:
                self.hits += 1
                logger.debug(f"Cache HIT: {key}")
            else:
                self.misses += 1
                logger.debug(f"Cache MISS: {key}")
            return value
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None
    
    def set(self, key: str, value: Any) -> None:
        """
        Set value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
        """
        if not self.enabled:
            return
            
        try:
            self.cache[key] = value
            logger.debug(f"Cache SET: {key}")
        except Exception as e:
            logger.error(f"Cache set error: {e}")
    
    def clear(self) -> None:
        """Clear all cached items."""
        self.cache.clear()
        self.hits = 0
        self.misses = 0
        logger.info("Cache cleared")
    
    def get_stats(self) -> dict:
        """
        Get cache statistics.
        
        Returns:
            Dictionary with cache stats
        """
        total_requests = self.hits + self.misses
        hit_rate = (self.hits / total_requests * 100) if total_requests > 0 else 0
        
        return {
            "enabled": self.enabled,
            "size": len(self.cache),
            "maxsize": self.cache.maxsize,
            "ttl": self.cache.ttl,
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": f"{hit_rate:.2f}%"
        }
    
    def enable(self) -> None:
        """Enable caching."""
        self.enabled = True
        logger.info("Cache enabled")
    
    def disable(self) -> None:
        """Disable caching."""
        self.enabled = False
        logger.info("Cache disabled")


def cached(cache_manager: CacheManager, key_func: Optional[Callable] = None):
    """
    Decorator to cache function results.
    
    Args:
        cache_manager: CacheManager instance
        key_func: Optional function to generate cache key from args
        
    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                # Default key generation
                cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # Try to get from cache
            cached_value = cache_manager.get(cache_key)
            if cached_value is not None:
                return cached_value
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            cache_manager.set(cache_key, result)
            return result
        
        return wrapper
    return decorator


class RateLimiter:
    """Simple rate limiter for API calls."""
    
    def __init__(self, max_calls: int, period: int):
        """
        Initialize rate limiter.
        
        Args:
            max_calls: Maximum number of calls allowed
            period: Time period in seconds
        """
        self.max_calls = max_calls
        self.period = period
        self.calls = []
        logger.info(f"Rate limiter initialized: {max_calls} calls per {period}s")
    
    def is_allowed(self) -> bool:
        """
        Check if a call is allowed under rate limit.
        
        Returns:
            True if call is allowed, False otherwise
        """
        now = time.time()
        
        # Remove old calls outside the period
        self.calls = [call_time for call_time in self.calls 
                     if now - call_time < self.period]
        
        # Check if we're under the limit
        if len(self.calls) < self.max_calls:
            self.calls.append(now)
            return True
        
        logger.warning(f"Rate limit exceeded: {len(self.calls)}/{self.max_calls}")
        return False
    
    def wait_time(self) -> float:
        """
        Get time to wait before next call is allowed.
        
        Returns:
            Seconds to wait
        """
        if len(self.calls) < self.max_calls:
            return 0.0
        
        now = time.time()
        oldest_call = min(self.calls)
        wait = self.period - (now - oldest_call)
        return max(0.0, wait)
    
    def reset(self) -> None:
        """Reset rate limiter."""
        self.calls = []
        logger.info("Rate limiter reset")

# Made with Bob
