"""Twitter API client with error handling and rate limiting."""

import tweepy
import logging
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime

from ..utils.cache import CacheManager, RateLimiter

logger = logging.getLogger(__name__)


class TwitterAPIError(Exception):
    """Custom exception for Twitter API errors."""

    pass


@dataclass
class Tweet:
    """Data class representing a tweet."""

    id: str
    text: str
    created_at: datetime
    author_id: str
    author_username: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert tweet to dictionary."""
        return {
            "id": self.id,
            "text": self.text,
            "created_at": self.created_at.isoformat(),
            "author_id": self.author_id,
            "author_username": self.author_username,
        }


class TwitterClient:
    """
    Twitter API client with caching, rate limiting, and error handling.
    """

    def __init__(
        self,
        bearer_token: str,
        cache_manager: Optional[CacheManager] = None,
        rate_limiter: Optional[RateLimiter] = None,
        timeout: int = 30,
    ):
        """
        Initialize Twitter client.

        Args:
            bearer_token: Twitter API bearer token
            cache_manager: Optional cache manager instance
            rate_limiter: Optional rate limiter instance
            timeout: API request timeout in seconds

        Raises:
            TwitterAPIError: If authentication fails
        """
        self.timeout = timeout
        self.cache_manager = cache_manager
        self.rate_limiter = rate_limiter

        try:
            self.client = tweepy.Client(
                bearer_token=bearer_token, wait_on_rate_limit=True
            )
            logger.info("Twitter client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Twitter client: {e}")
            raise TwitterAPIError(f"Authentication failed: {e}") from e

    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """
        Get user information by username.

        Args:
            username: Twitter username (without @)

        Returns:
            User data dictionary or None if not found

        Raises:
            TwitterAPIError: If API request fails
        """
        cache_key = f"user:{username}"

        # Check cache
        if self.cache_manager:
            cached_user = self.cache_manager.get(cache_key)
            if cached_user:
                logger.debug(f"User {username} retrieved from cache")
                return cached_user

        # Check rate limit
        if self.rate_limiter and not self.rate_limiter.is_allowed():
            wait_time = self.rate_limiter.wait_time()
            raise TwitterAPIError(f"Rate limit exceeded. Wait {wait_time:.1f} seconds.")

        try:
            logger.info(f"Fetching user: {username}")
            response = self.client.get_user(username=username)

            if not response.data:
                logger.warning(f"User not found: {username}")
                return None

            user_data = {
                "id": response.data.id,
                "username": response.data.username,
                "name": response.data.name,
            }

            # Cache the result
            if self.cache_manager:
                self.cache_manager.set(cache_key, user_data)

            logger.info(f"User {username} fetched successfully")
            return user_data

        except tweepy.TweepyException as e:
            logger.error(f"Twitter API error fetching user {username}: {e}")
            raise TwitterAPIError(f"Failed to fetch user: {e}") from e
        except Exception as e:
            logger.error(f"Unexpected error fetching user {username}: {e}")
            raise TwitterAPIError(f"Unexpected error: {e}") from e

    def get_user_tweets(
        self,
        user_id: str,
        max_results: int = 50,
        exclude_replies: bool = True,
        exclude_retweets: bool = True,
    ) -> List[Tweet]:
        """
        Get tweets from a user.

        Args:
            user_id: Twitter user ID
            max_results: Maximum number of tweets to fetch (5-100)
            exclude_replies: Exclude reply tweets
            exclude_retweets: Exclude retweets

        Returns:
            List of Tweet objects

        Raises:
            TwitterAPIError: If API request fails
        """
        # Validate max_results
        if not 5 <= max_results <= 100:
            raise ValueError("max_results must be between 5 and 100")

        cache_key = (
            f"tweets:{user_id}:{max_results}:{exclude_replies}:{exclude_retweets}"
        )

        # Check cache
        if self.cache_manager:
            cached_tweets = self.cache_manager.get(cache_key)
            if cached_tweets:
                logger.debug(f"Tweets for user {user_id} retrieved from cache")
                return cached_tweets

        # Check rate limit
        if self.rate_limiter and not self.rate_limiter.is_allowed():
            wait_time = self.rate_limiter.wait_time()
            raise TwitterAPIError(f"Rate limit exceeded. Wait {wait_time:.1f} seconds.")

        try:
            logger.info(f"Fetching tweets for user {user_id} (max: {max_results})")

            # Build exclusions
            excludes = []
            if exclude_replies:
                excludes.append("replies")
            if exclude_retweets:
                excludes.append("retweets")

            response = self.client.get_users_tweets(
                id=user_id,
                max_results=max_results,
                exclude=excludes if excludes else None,
                tweet_fields=["created_at", "author_id"],
            )

            if not response.data:
                logger.warning(f"No tweets found for user {user_id}")
                return []

            # Convert to Tweet objects
            tweets = []
            for tweet_data in response.data:
                tweet = Tweet(
                    id=tweet_data.id,
                    text=tweet_data.text,
                    created_at=tweet_data.created_at,
                    author_id=tweet_data.author_id,
                    author_username="",  # Will be filled if needed
                )
                tweets.append(tweet)

            # Cache the result
            if self.cache_manager:
                self.cache_manager.set(cache_key, tweets)

            logger.info(f"Fetched {len(tweets)} tweets for user {user_id}")
            return tweets

        except tweepy.TweepyException as e:
            logger.error(f"Twitter API error fetching tweets: {e}")
            raise TwitterAPIError(f"Failed to fetch tweets: {e}") from e
        except Exception as e:
            logger.error(f"Unexpected error fetching tweets: {e}")
            raise TwitterAPIError(f"Unexpected error: {e}") from e

    def get_tweets_by_username(
        self,
        username: str,
        max_results: int = 50,
        exclude_replies: bool = True,
        exclude_retweets: bool = True,
    ) -> List[Tweet]:
        """
        Get tweets from a user by username.

        Args:
            username: Twitter username (without @)
            max_results: Maximum number of tweets to fetch (5-100)
            exclude_replies: Exclude reply tweets
            exclude_retweets: Exclude retweets

        Returns:
            List of Tweet objects

        Raises:
            TwitterAPIError: If user not found or API request fails
        """
        # Get user first
        user = self.get_user_by_username(username)
        if not user:
            raise TwitterAPIError(f"User not found: {username}")

        # Get tweets
        tweets = self.get_user_tweets(
            user_id=user["id"],
            max_results=max_results,
            exclude_replies=exclude_replies,
            exclude_retweets=exclude_retweets,
        )

        # Add username to tweets
        for tweet in tweets:
            tweet.author_username = username

        return tweets


# Made with Bob
