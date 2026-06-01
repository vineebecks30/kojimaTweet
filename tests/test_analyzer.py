"""Tests for movie analyzer module."""

import pytest
from datetime import datetime
from src.analyzers.movie_analyzer import MovieAnalyzer, MovieReview
from src.api.twitter_client import Tweet


@pytest.fixture
def analyzer():
    """Create analyzer instance for testing."""
    return MovieAnalyzer(rating_5_stars=200, rating_4_stars=100, rating_3_stars=50)


@pytest.fixture
def sample_tweet():
    """Create sample tweet for testing."""
    return Tweet(
        id="123456789",
        text="Watched Oppenheimer. Nolan's masterpiece about the father of the atomic bomb. "
        "Incredible cinematography and powerful performances. A must-see film that explores "
        "the moral complexities of scientific discovery and its consequences.",
        created_at=datetime.now(),
        author_id="987654321",
        author_username="HIDEO_KOJIMA_EN",
    )


class TestMovieAnalyzer:
    """Test cases for MovieAnalyzer class."""

    def test_is_movie_tweet_positive(self, analyzer):
        """Test detection of movie-related tweets."""
        assert analyzer.is_movie_tweet("Watched a great movie last night")
        assert analyzer.is_movie_tweet("This film was amazing")
        assert analyzer.is_movie_tweet("Just saw the new cinema release")

    def test_is_movie_tweet_negative(self, analyzer):
        """Test rejection of non-movie tweets."""
        assert not analyzer.is_movie_tweet("Having lunch today")
        assert not analyzer.is_movie_tweet("Working on my new game")
        assert not analyzer.is_movie_tweet("Beautiful weather outside")

    def test_extract_movie_name_watched_pattern(self, analyzer):
        """Test movie name extraction with 'Watched' pattern."""
        text = "Watched Oppenheimer. Great film!"
        assert analyzer.extract_movie_name(text) == "Oppenheimer"

    def test_extract_movie_name_quoted(self, analyzer):
        """Test movie name extraction with quotes."""
        text = 'Just saw "The Zone of Interest" - powerful stuff'
        assert analyzer.extract_movie_name(text) == "The Zone of Interest"

    def test_extract_movie_name_unknown(self, analyzer):
        """Test fallback for unknown movie name."""
        text = "This movie was great"
        assert analyzer.extract_movie_name(text) == "Unknown Movie"

    def test_calculate_rating_5_stars(self, analyzer):
        """Test 5-star rating calculation."""
        text = "A" * 250  # Long text
        rating, char_count = analyzer.calculate_rating(text, "Movie")
        assert rating == 5
        assert char_count >= 200

    def test_calculate_rating_4_stars(self, analyzer):
        """Test 4-star rating calculation."""
        text = "A" * 150  # Medium-long text
        rating, char_count = analyzer.calculate_rating(text, "Movie")
        assert rating == 4
        assert 100 <= char_count < 200

    def test_calculate_rating_3_stars(self, analyzer):
        """Test 3-star rating calculation."""
        text = "A" * 75  # Medium text
        rating, char_count = analyzer.calculate_rating(text, "Movie")
        assert rating == 3
        assert 50 <= char_count < 100

    def test_calculate_rating_2_stars(self, analyzer):
        """Test 2-star rating calculation."""
        text = "A" * 30  # Short text
        rating, char_count = analyzer.calculate_rating(text, "Movie")
        assert rating == 2
        assert char_count < 50

    def test_analyze_tweet_movie(self, analyzer, sample_tweet):
        """Test analyzing a movie tweet."""
        review = analyzer.analyze_tweet(sample_tweet)

        assert review is not None
        assert isinstance(review, MovieReview)
        assert review.movie_name == "Oppenheimer"
        assert review.rating >= 2
        assert review.rating <= 5
        assert review.tweet_id == sample_tweet.id

    def test_analyze_tweet_non_movie(self, analyzer):
        """Test analyzing a non-movie tweet."""
        tweet = Tweet(
            id="123",
            text="Working on my new game project today",
            created_at=datetime.now(),
            author_id="456",
            author_username="test_user",
        )

        review = analyzer.analyze_tweet(tweet)
        assert review is None

    def test_analyze_tweets_multiple(self, analyzer):
        """Test analyzing multiple tweets."""
        tweets = [
            Tweet(
                id="1",
                text="Watched Oppenheimer. Amazing film with great performances.",
                created_at=datetime.now(),
                author_id="123",
                author_username="test",
            ),
            Tweet(
                id="2",
                text="Working on game development",
                created_at=datetime.now(),
                author_id="123",
                author_username="test",
            ),
            Tweet(
                id="3",
                text="Watched The Zone of Interest. Powerful and disturbing film.",
                created_at=datetime.now(),
                author_id="123",
                author_username="test",
            ),
        ]

        reviews = analyzer.analyze_tweets(tweets)
        assert len(reviews) == 2  # Only 2 movie tweets (tweet 2 is not about movies)

    def test_get_statistics_empty(self, analyzer):
        """Test statistics with no reviews."""
        stats = analyzer.get_statistics([])

        assert stats["total_reviews"] == 0
        assert stats["average_rating"] == 0.0
        assert stats["average_length"] == 0

    def test_get_statistics_with_reviews(self, analyzer):
        """Test statistics with reviews."""
        reviews = [
            MovieReview(
                movie_name="Movie1",
                rating=5,
                tweet_text="A" * 250,
                tweet_id="1",
                created_at=datetime.now(),
                character_count=250,
            ),
            MovieReview(
                movie_name="Movie2",
                rating=3,
                tweet_text="A" * 75,
                tweet_id="2",
                created_at=datetime.now(),
                character_count=75,
            ),
        ]

        stats = analyzer.get_statistics(reviews)

        assert stats["total_reviews"] == 2
        assert stats["average_rating"] == 4.0
        assert stats["average_length"] == 162.5
        assert stats["rating_distribution"]["5_stars"] == 1
        assert stats["rating_distribution"]["3_stars"] == 1


class TestMovieReview:
    """Test cases for MovieReview dataclass."""

    def test_movie_review_creation(self):
        """Test creating a MovieReview instance."""
        review = MovieReview(
            movie_name="Test Movie",
            rating=4,
            tweet_text="Great film!",
            tweet_id="123",
            created_at=datetime.now(),
            character_count=100,
        )

        assert review.movie_name == "Test Movie"
        assert review.rating == 4
        assert review.character_count == 100

    def test_movie_review_str(self):
        """Test string representation of MovieReview."""
        review = MovieReview(
            movie_name="Test Movie",
            rating=4,
            tweet_text="Great film!",
            tweet_id="123",
            created_at=datetime.now(),
            character_count=100,
        )

        str_repr = str(review)
        assert "Test Movie" in str_repr
        assert "⭐" in str_repr
        assert str_repr.count("⭐") == 4

    def test_movie_review_to_dict(self):
        """Test converting MovieReview to dictionary."""
        now = datetime.now()
        review = MovieReview(
            movie_name="Test Movie",
            rating=4,
            tweet_text="Great film!",
            tweet_id="123",
            created_at=now,
            character_count=100,
        )

        review_dict = review.to_dict()

        assert review_dict["movie_name"] == "Test Movie"
        assert review_dict["rating"] == 4
        assert review_dict["tweet_text"] == "Great film!"
        assert review_dict["tweet_id"] == "123"
        assert review_dict["character_count"] == 100
        assert "created_at" in review_dict


# Made with Bob
