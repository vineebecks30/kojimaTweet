"""Movie review analyzer for Kojima's tweets."""

import re
import logging
from typing import Optional, List, Tuple
from dataclasses import dataclass
from datetime import datetime

from ..api.twitter_client import Tweet

logger = logging.getLogger(__name__)


@dataclass
class MovieReview:
    """Data class representing a movie review from a tweet."""

    movie_name: str
    rating: int
    tweet_text: str
    tweet_id: str
    created_at: datetime
    character_count: int

    def __str__(self) -> str:
        """String representation with star rating."""
        stars = "⭐" * self.rating
        return f"{self.movie_name} → {stars} ({self.rating}/5)"

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "movie_name": self.movie_name,
            "rating": self.rating,
            "tweet_text": self.tweet_text,
            "tweet_id": self.tweet_id,
            "created_at": self.created_at.isoformat(),
            "character_count": self.character_count,
        }


class MovieAnalyzer:
    """
    Analyzer for movie review tweets.

    Identifies movie-related tweets and rates them based on content length.
    """

    # Movie-related keywords
    MOVIE_KEYWORDS = [
        "movie",
        "film",
        "watched",
        "cinema",
        "screening",
        "director",
        "actor",
        "actress",
        "masterpiece",
    ]

    # Common patterns for movie mentions
    MOVIE_PATTERNS = [
        r"Watched\s+(.+?)\.",  # "Watched [Movie Name]."
        r"(?:Saw|Viewing)\s+(.+?)\.",  # "Saw [Movie Name]."
        r"(?:Movie|Film):\s*(.+?)(?:\.|$)",  # "Movie: [Movie Name]"
        r"\"(.+?)\"",  # Quoted movie names
    ]

    def __init__(
        self,
        rating_5_stars: int = 200,
        rating_4_stars: int = 100,
        rating_3_stars: int = 50,
    ):
        """
        Initialize movie analyzer.

        Args:
            rating_5_stars: Character threshold for 5-star rating
            rating_4_stars: Character threshold for 4-star rating
            rating_3_stars: Character threshold for 3-star rating
        """
        self.rating_5_stars = rating_5_stars
        self.rating_4_stars = rating_4_stars
        self.rating_3_stars = rating_3_stars

        # Compile regex patterns for efficiency
        self.compiled_patterns = [
            re.compile(pattern, re.IGNORECASE) for pattern in self.MOVIE_PATTERNS
        ]

        logger.info(
            f"MovieAnalyzer initialized with thresholds: "
            f"5★={rating_5_stars}, 4★={rating_4_stars}, 3★={rating_3_stars}"
        )

    def is_movie_tweet(self, tweet_text: str) -> bool:
        """
        Check if tweet is about a movie.

        Args:
            tweet_text: Tweet text to analyze

        Returns:
            True if tweet contains movie-related keywords
        """
        text_lower = tweet_text.lower()
        return any(keyword in text_lower for keyword in self.MOVIE_KEYWORDS)

    def extract_movie_name(self, tweet_text: str) -> str:
        """
        Extract movie name from tweet text.

        Args:
            tweet_text: Tweet text to analyze

        Returns:
            Extracted movie name or "Unknown Movie"
        """
        # Try each pattern
        for pattern in self.compiled_patterns:
            match = pattern.search(tweet_text)
            if match:
                movie_name = match.group(1).strip()
                # Clean up the movie name
                movie_name = self._clean_movie_name(movie_name)
                if movie_name:
                    logger.debug(f"Extracted movie name: {movie_name}")
                    return movie_name

        logger.debug("Could not extract movie name from tweet")
        return "Unknown Movie"

    def _clean_movie_name(self, name: str) -> str:
        """
        Clean extracted movie name.

        Args:
            name: Raw movie name

        Returns:
            Cleaned movie name
        """
        # Remove common suffixes
        name = re.sub(r"\s+(?:by|directed by|from).*$", "", name, flags=re.IGNORECASE)

        # Remove extra whitespace
        name = " ".join(name.split())

        # Remove trailing punctuation except for titles that end with punctuation
        name = name.rstrip(".,;:")

        return name

    def calculate_rating(self, tweet_text: str, movie_name: str) -> Tuple[int, int]:
        """
        Calculate movie rating based on tweet length.

        Args:
            tweet_text: Full tweet text
            movie_name: Extracted movie name

        Returns:
            Tuple of (rating, character_count)
        """
        # Remove movie name from text for character count
        text_without_name = tweet_text.replace(movie_name, "")
        char_count = len(text_without_name.strip())

        # Determine rating based on character count
        if char_count >= self.rating_5_stars:
            rating = 5
        elif char_count >= self.rating_4_stars:
            rating = 4
        elif char_count >= self.rating_3_stars:
            rating = 3
        else:
            rating = 2

        logger.debug(
            f"Rating calculated: {rating}★ "
            f"(chars: {char_count}, thresholds: "
            f"5★≥{self.rating_5_stars}, 4★≥{self.rating_4_stars}, "
            f"3★≥{self.rating_3_stars})"
        )

        return rating, char_count

    def analyze_tweet(self, tweet: Tweet) -> Optional[MovieReview]:
        """
        Analyze a single tweet for movie review.

        Args:
            tweet: Tweet object to analyze

        Returns:
            MovieReview object if tweet is about a movie, None otherwise
        """
        # Check if it's a movie tweet
        if not self.is_movie_tweet(tweet.text):
            logger.debug(f"Tweet {tweet.id} is not about a movie")
            return None

        # Extract movie name
        movie_name = self.extract_movie_name(tweet.text)

        # Calculate rating
        rating, char_count = self.calculate_rating(tweet.text, movie_name)

        # Create review object
        review = MovieReview(
            movie_name=movie_name,
            rating=rating,
            tweet_text=tweet.text,
            tweet_id=tweet.id,
            created_at=tweet.created_at,
            character_count=char_count,
        )

        logger.info(f"Analyzed tweet {tweet.id}: {review}")
        return review

    def analyze_tweets(self, tweets: List[Tweet]) -> List[MovieReview]:
        """
        Analyze multiple tweets for movie reviews.

        Args:
            tweets: List of Tweet objects

        Returns:
            List of MovieReview objects
        """
        logger.info(f"Analyzing {len(tweets)} tweets for movie reviews")

        reviews = []
        for tweet in tweets:
            review = self.analyze_tweet(tweet)
            if review:
                reviews.append(review)

        logger.info(f"Found {len(reviews)} movie reviews out of {len(tweets)} tweets")
        return reviews

    def get_statistics(self, reviews: List[MovieReview]) -> dict:
        """
        Get statistics about analyzed reviews.

        Args:
            reviews: List of MovieReview objects

        Returns:
            Dictionary with statistics
        """
        if not reviews:
            return {
                "total_reviews": 0,
                "average_rating": 0.0,
                "rating_distribution": {},
                "average_length": 0,
            }

        # Calculate statistics
        total = len(reviews)
        avg_rating = sum(r.rating for r in reviews) / total
        avg_length = sum(r.character_count for r in reviews) / total

        # Rating distribution
        distribution = {}
        for i in range(1, 6):
            count = sum(1 for r in reviews if r.rating == i)
            distribution[f"{i}_stars"] = count

        return {
            "total_reviews": total,
            "average_rating": round(avg_rating, 2),
            "rating_distribution": distribution,
            "average_length": round(avg_length, 1),
        }


# Made with Bob
