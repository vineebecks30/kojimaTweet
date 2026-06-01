# 🎬 KojimaTweet - Simple Node.js Edition

A lightweight Node.js tool to analyze Hideo Kojima's movie review tweets and rate them based on tweet length.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your Twitter API bearer token
```

Your `.env` file should look like:
```env
TWITTER_BEARER_TOKEN=your_actual_bearer_token_here
TWITTER_USERNAME=HIDEO_KOJIMA_EN
MAX_TWEETS=50
```

### 3. Run

```bash
npm start
```

## 📋 Requirements

- Node.js 14 or higher
- Twitter API Bearer Token ([Get one here](https://developer.twitter.com/en/portal/dashboard))

## 🎯 How It Works

1. **Fetches tweets** from the specified Twitter account
2. **Identifies movie-related tweets** using keywords (movie, film, watched, etc.)
3. **Extracts movie names** using pattern matching
4. **Rates movies** based on tweet length:
   - ⭐⭐⭐⭐⭐ (5 stars): 200+ characters
   - ⭐⭐⭐⭐ (4 stars): 100-199 characters
   - ⭐⭐⭐ (3 stars): 50-99 characters
   - ⭐⭐ (2 stars): < 50 characters
5. **Displays results** with statistics

## 📁 Project Structure

```
kojimaTweet/
├── index.js          # Main application (180 lines)
├── package.json      # Dependencies
├── .env.example      # Environment template
├── .gitignore        # Git ignore rules
└── README.md         # This file
```

## ⚙️ Configuration

Edit `.env` to customize:

```env
# Change the Twitter account to analyze
TWITTER_USERNAME=HIDEO_KOJIMA_EN

# Number of tweets to fetch (5-100)
MAX_TWEETS=50

# Customize rating thresholds
RATING_5_STARS=200
RATING_4_STARS=100
RATING_3_STARS=50
```

## 📊 Example Output

```
🔍 Fetching tweets from @HIDEO_KOJIMA_EN...
✅ Found user: HIDEO KOJIMA
✅ Retrieved 50 tweets

🎬 Analyzing tweets for movie reviews...

============================================================
🎬 KOJIMA'S MOVIE REVIEWS (12 found)
============================================================

1. Oppenheimer → ⭐⭐⭐⭐⭐ (5/5)
   📝 Tweet: Watched Oppenheimer. Nolan's masterpiece about the father...
   📅 Date: 1/15/2024, 2:30:00 PM

2. The Zone of Interest → ⭐⭐⭐⭐ (4/5)
   📝 Tweet: Watched The Zone of Interest. Powerful and disturbing...
   📅 Date: 1/10/2024, 9:15:00 AM

============================================================
📈 STATISTICS
============================================================
Total Reviews: 12
Average Rating: 4.2⭐

Rating Distribution:
  ⭐⭐⭐⭐⭐: 5 reviews
  ⭐⭐⭐⭐: 4 reviews
  ⭐⭐⭐: 2 reviews
  ⭐⭐: 1 reviews
============================================================
```

## 🔧 Troubleshooting

### Error: TWITTER_BEARER_TOKEN not set

Create a `.env` file with your Twitter API credentials:
```bash
cp .env.example .env
# Edit .env and add your token
```

### Error: Authentication failed

Check that your bearer token is correct and active in the [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard).

### Error: Rate limit exceeded

Twitter API has rate limits. Wait 15 minutes before trying again.

## 🎓 Features

- ✅ Simple single-file implementation
- ✅ Environment-based configuration
- ✅ Error handling with helpful messages
- ✅ Statistics and rating distribution
- ✅ Easy to deploy and maintain
- ✅ No complex dependencies

## 📝 License

MIT

## 🙏 Acknowledgments

- Hideo Kojima for his insightful movie reviews
- Twitter API for data access