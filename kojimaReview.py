import tweepy
import re

# Step 1: Authenticate (you’ll need X/Twitter API credentials)
client = tweepy.Client(bearer_token="bearer token")

# Step 2: Fetch recent tweets from Kojima
username = "HIDEO_KOJIMA_EN"
user = client.get_user(username=username)
tweets = client.get_users_tweets(id=user.data.id, max_results=50)

# Step 3: Filter & analyze tweets
def rate_movie_tweet(tweet_text):
    # Example heuristic: skip if it's not about a movie
    if not any(word in tweet_text.lower() for word in ["movie", "film", "watched"]):
        return None

    # Optional: Extract movie name if using a pattern like “Watched [movie name].”
    match = re.match(r"Watched\s+(.+?)\.", tweet_text,re.IGNORECASE)
    movie_name = match.group(1) if match else "Unknown Movie"

    # Step 4: Count characters excluding movie name
    text_without_name = tweet_text.replace(movie_name, "")
    char_count = len(text_without_name.strip())

    # Step 5: Rating logic
    if char_count > 200:
        stars = 5
    elif char_count > 100:
        stars = 4
    elif char_count > 50:
        stars = 3
    else:
        stars = 2

    return {"movie": movie_name, "tweet": tweet_text, "rating": stars}


# Step 6: Run it
for tweet in tweets.data:
    result = rate_movie_tweet(tweet.text)
    if result:
        print(f"{result['movie']} → {'⭐'*result['rating']}")
        print(f"Tweet: {result['tweet']}\n")
