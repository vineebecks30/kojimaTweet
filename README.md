# 🎬 KojimaTweet - Kojima Movie Review Analyzer

A Python application that fetches and analyzes Hideo Kojima's movie review tweets, automatically rating them based on tweet length and content.

## 📋 Overview

KojimaTweet connects to Twitter's API to fetch tweets from [@HIDEO_KOJIMA_EN](https://twitter.com/HIDEO_KOJIMA_EN), identifies movie-related tweets, extracts movie names, and rates them on a 5-star scale based on the length and detail of Kojima's commentary.

### Features

- ✅ **Secure Configuration**: Environment-based credential management
- ✅ **Smart Caching**: Reduces API calls with TTL-based caching
- ✅ **Rate Limiting**: Prevents API quota exhaustion
- ✅ **Error Handling**: Comprehensive error handling and logging
- ✅ **Movie Detection**: Intelligent pattern matching for movie names
- ✅ **Star Ratings**: Automatic rating based on review length
- ✅ **Statistics**: Detailed analytics on reviews
- ✅ **Colored Logging**: Beautiful console output with color-coded logs

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Twitter API Bearer Token ([Get one here](https://developer.twitter.com/en/portal/dashboard))

### Installation

1. **Clone or download the project**

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment**
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your Twitter API credentials
nano .env  # or use your preferred editor
```

4. **Run the application**
```bash
python -m src.main
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```env
# Twitter API Configuration
TWITTER_BEARER_TOKEN=your_bearer_token_here
TWITTER_USERNAME=HIDEO_KOJIMA_EN

# API Settings
MAX_TWEETS=50
API_TIMEOUT=30

# Rating Thresholds (character counts)
RATING_5_STARS=200
RATING_4_STARS=100
RATING_3_STARS=50

# Caching Configuration
CACHE_ENABLED=true
CACHE_TTL=3600

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=logs/kojima_tweet.log

# Rate Limiting
RATE_LIMIT_CALLS=15
RATE_LIMIT_PERIOD=900
```

### Rating System

The application rates movies based on tweet length (excluding the movie name):

| Stars | Character Count | Description |
|-------|----------------|-------------|
| ⭐⭐⭐⭐⭐ | 200+ chars | Detailed, passionate review |
| ⭐⭐⭐⭐ | 100-199 chars | Substantial commentary |
| ⭐⭐⭐ | 50-99 chars | Brief thoughts |
| ⭐⭐ | < 50 chars | Minimal commentary |

## 📁 Project Structure

```
kojimaTweet/
├── .env.example              # Environment template
├── .gitignore               # Git ignore rules
├── requirements.txt         # Python dependencies
├── README.md                # This file
├── ANALYSIS_AND_IMPROVEMENTS.md  # Detailed analysis
├── config/
│   ├── __init__.py
│   └── settings.py          # Configuration management
├── src/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── api/
│   │   ├── __init__.py
│   │   └── twitter_client.py # Twitter API wrapper
│   ├── analyzers/
│   │   ├── __init__.py
│   │   └── movie_analyzer.py # Movie rating logic
│   └── utils/
│       ├── __init__.py
│       ├── cache.py         # Caching utilities
│       └── logger.py        # Logging setup
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   ├── test_analyzer.py
│   └── test_cache.py
└── logs/                    # Log files (auto-created)
```

## 🔒 Security Features

### Implemented Security Measures

1. **Environment Variables**: All sensitive data stored in `.env` file
2. **Git Ignore**: Credentials excluded from version control
3. **Input Validation**: Pydantic-based configuration validation
4. **Rate Limiting**: Prevents API abuse
5. **Error Handling**: Secure error messages without exposing internals
6. **Logging**: Audit trail of all operations

### Best Practices

- Never commit `.env` file to version control
- Rotate API tokens regularly
- Use read-only API tokens when possible
- Monitor API usage through Twitter Developer Portal
- Review logs regularly for suspicious activity

## 📊 Usage Examples

### Basic Usage

```bash
python -m src.main
```

### Sample Output

```
🔍 Fetching tweets from @HIDEO_KOJIMA_EN...
✅ Retrieved 50 tweets

🎬 Analyzing tweets for movie reviews...

============================================================
🎬 KOJIMA'S MOVIE REVIEWS (12 found)
============================================================

1. Oppenheimer → ⭐⭐⭐⭐⭐ (5/5)
   📝 Tweet: Watched Oppenheimer. Nolan's masterpiece about the father of the atomic bomb...
   📊 Length: 245 chars
   📅 Date: 2024-01-15 14:30

2. The Zone of Interest → ⭐⭐⭐⭐ (4/5)
   📝 Tweet: Watched The Zone of Interest. Powerful and disturbing film...
   📊 Length: 156 chars
   📅 Date: 2024-01-10 09:15

============================================================
📈 STATISTICS
============================================================
Total Reviews: 12
Average Rating: 4.2⭐
Average Length: 178.5 chars

Rating Distribution:
  ⭐⭐⭐⭐⭐: 5 reviews
  ⭐⭐⭐⭐: 4 reviews
  ⭐⭐⭐: 2 reviews
  ⭐⭐: 1 reviews
============================================================

💾 Cache: 3 hits, 2 misses (60.00% hit rate)
```

## 🧪 Testing

Run tests with pytest:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_analyzer.py

# Run with verbose output
pytest -v
```

## 🔧 Development

### Code Quality Tools

```bash
# Format code with black
black src/ tests/

# Lint with flake8
flake8 src/ tests/

# Type checking with mypy
mypy src/

# Security scan with bandit
bandit -r src/

# Check dependencies for vulnerabilities
safety check
```

### Adding New Features

1. Create feature branch
2. Implement changes with tests
3. Run code quality checks
4. Update documentation
5. Submit pull request

## 📈 Performance Optimization

### Caching Strategy

- **User Data**: Cached for 1 hour (configurable)
- **Tweet Data**: Cached for 1 hour (configurable)
- **Cache Size**: 100 items max (configurable)

### Rate Limiting

- **Default**: 15 calls per 15 minutes (Twitter API limit)
- **Configurable**: Adjust via environment variables
- **Automatic**: Built-in wait mechanism

## 🐛 Troubleshooting

### Common Issues

**Issue**: `Authentication failed`
- **Solution**: Check your bearer token in `.env` file
- Verify token is active in Twitter Developer Portal

**Issue**: `Rate limit exceeded`
- **Solution**: Wait for the specified time or reduce `MAX_TWEETS`
- Consider increasing `CACHE_TTL` to reduce API calls

**Issue**: `No movie reviews found`
- **Solution**: Adjust `MAX_TWEETS` to fetch more tweets
- Check if the target user has recent movie-related tweets

**Issue**: `Module not found`
- **Solution**: Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (3.8+ required)

## 📝 Logging

Logs are stored in `logs/kojima_tweet.log` by default.

### Log Levels

- **DEBUG**: Detailed diagnostic information
- **INFO**: General informational messages
- **WARNING**: Warning messages for potential issues
- **ERROR**: Error messages for failures
- **CRITICAL**: Critical errors requiring immediate attention

### Viewing Logs

```bash
# View recent logs
tail -f logs/kojima_tweet.log

# Search for errors
grep ERROR logs/kojima_tweet.log

# View with colors (if supported)
cat logs/kojima_tweet.log
```

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

This project is provided as-is for educational and personal use.

## 🙏 Acknowledgments

- Hideo Kojima for his insightful movie reviews
- Twitter API for data access
- Tweepy library for Python Twitter integration

## 📞 Support

For issues, questions, or suggestions:
- Check the [Troubleshooting](#-troubleshooting) section
- Review logs in `logs/kojima_tweet.log`
- Open an issue on the project repository

## 🔄 Version History

### Version 2.0.0 (Current)
- Complete rewrite with improved architecture
- Added security features and environment configuration
- Implemented caching and rate limiting
- Enhanced error handling and logging
- Added comprehensive testing
- Improved documentation

### Version 1.0.0 (Original)
- Basic tweet fetching and analysis
- Simple rating system
- Hardcoded configuration

---

**Made with ❤️ for movie enthusiasts and Kojima fans**