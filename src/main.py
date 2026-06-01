"""Main entry point for KojimaTweet application."""

import sys
import logging

from config.settings import get_settings, validate_environment
from src.utils.logger import setup_logger
from src.utils.cache import CacheManager, RateLimiter
from src.api.twitter_client import TwitterClient, TwitterAPIError
from src.analyzers.movie_analyzer import MovieAnalyzer

logger = logging.getLogger(__name__)


def display_reviews(reviews, show_stats: bool = True):
    """
    Display movie reviews in a formatted way.

    Args:
        reviews: List of MovieReview objects
        show_stats: Whether to show statistics
    """
    if not reviews:
        print("\n❌ No movie reviews found in recent tweets.")
        return

    print(f"\n{'='*60}")
    print(f"🎬 KOJIMA'S MOVIE REVIEWS ({len(reviews)} found)")
    print(f"{'='*60}\n")

    for i, review in enumerate(reviews, 1):
        print(f"{i}. {review}")
        print(f"   📝 Tweet: {review.tweet_text[:100]}...")
        print(f"   📊 Length: {review.character_count} chars")
        print(f"   📅 Date: {review.created_at.strftime('%Y-%m-%d %H:%M')}")
        print()

    if show_stats:
        from src.analyzers.movie_analyzer import MovieAnalyzer

        analyzer = MovieAnalyzer()
        stats = analyzer.get_statistics(reviews)

        print(f"{'='*60}")
        print("📈 STATISTICS")
        print(f"{'='*60}")
        print(f"Total Reviews: {stats['total_reviews']}")
        print(f"Average Rating: {stats['average_rating']}⭐")
        print(f"Average Length: {stats['average_length']} chars")
        print("\nRating Distribution:")
        for rating, count in sorted(stats["rating_distribution"].items()):
            stars = rating.split("_")[0]
            print(f"  {'⭐' * int(stars)}: {count} reviews")
        print(f"{'='*60}\n")


def main():
    """Main application function."""
    # Validate environment first
    is_valid, error_msg = validate_environment()
    if not is_valid:
        print(f"\n❌ Configuration Error:\n{error_msg}\n")
        print("Please create a .env file based on .env.example")
        return 1

    # Load settings
    try:
        settings = get_settings()
    except Exception as e:
        print(f"\n❌ Failed to load settings: {e}\n")
        return 1

    # Setup logging
    setup_logger(
        name="kojima_tweet", log_level=settings.log_level, log_file=settings.log_file
    )

    logger.info("=" * 60)
    logger.info("KojimaTweet Application Started")
    logger.info("=" * 60)

    try:
        # Initialize cache manager
        cache_manager = None
        if settings.cache_enabled:
            cache_manager = CacheManager(maxsize=100, ttl=settings.cache_ttl)
            logger.info("Cache enabled")

        # Initialize rate limiter
        rate_limiter = RateLimiter(
            max_calls=settings.rate_limit_calls, period=settings.rate_limit_period
        )

        # Initialize Twitter client
        logger.info(f"Connecting to Twitter API for user: {settings.twitter_username}")
        twitter_client = TwitterClient(
            bearer_token=settings.twitter_bearer_token,
            cache_manager=cache_manager,
            rate_limiter=rate_limiter,
            timeout=settings.api_timeout,
        )

        # Fetch tweets
        print(f"\n🔍 Fetching tweets from @{settings.twitter_username}...")
        tweets = twitter_client.get_tweets_by_username(
            username=settings.twitter_username,
            max_results=settings.max_tweets,
            exclude_replies=True,
            exclude_retweets=True,
        )

        logger.info(f"Fetched {len(tweets)} tweets")
        print(f"✅ Retrieved {len(tweets)} tweets")

        # Initialize analyzer
        analyzer = MovieAnalyzer(
            rating_5_stars=settings.rating_5_stars,
            rating_4_stars=settings.rating_4_stars,
            rating_3_stars=settings.rating_3_stars,
        )

        # Analyze tweets
        print("\n🎬 Analyzing tweets for movie reviews...")
        reviews = analyzer.analyze_tweets(tweets)

        # Display results
        display_reviews(reviews, show_stats=True)

        # Show cache stats if enabled
        if cache_manager:
            stats = cache_manager.get_stats()
            logger.info(f"Cache stats: {stats}")
            print(
                f"💾 Cache: {stats['hits']} hits, {stats['misses']} misses "
                f"({stats['hit_rate']} hit rate)"
            )

        logger.info("Application completed successfully")
        return 0

    except TwitterAPIError as e:
        logger.error(f"Twitter API error: {e}")
        print(f"\n❌ Twitter API Error: {e}")
        print("Please check your bearer token and network connection.")
        return 1

    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        print("\n\n⚠️  Application interrupted by user")
        return 130

    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        print(f"\n❌ Unexpected Error: {e}")
        print("Check logs for more details.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

# Made with Bob
