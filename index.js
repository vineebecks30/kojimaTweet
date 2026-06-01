require('dotenv').config();
const { TwitterApi } = require('twitter-api-v2');

// Configuration
const CONFIG = {
  bearerToken: process.env.TWITTER_BEARER_TOKEN,
  username: process.env.TWITTER_USERNAME || 'HIDEO_KOJIMA_EN',
  maxTweets: parseInt(process.env.MAX_TWEETS) || 50,
  ratingThresholds: {
    fiveStars: parseInt(process.env.RATING_5_STARS) || 200,
    fourStars: parseInt(process.env.RATING_4_STARS) || 100,
    threeStars: parseInt(process.env.RATING_3_STARS) || 50
  }
};

// Movie keywords to detect movie-related tweets
const MOVIE_KEYWORDS = ['movie', 'film', 'watched', 'cinema', 'screening', 'director'];

// Patterns to extract movie names
const MOVIE_PATTERNS = [
  /Watched\s+(.+?)\./i,
  /(?:Saw|Viewing)\s+(.+?)\./i,
  /(?:Movie|Film):\s*(.+?)(?:\.|$)/i,
  /"(.+?)"/
];

/**
 * Check if tweet is about a movie
 */
function isMovieTweet(text) {
  const lowerText = text.toLowerCase();
  return MOVIE_KEYWORDS.some(keyword => lowerText.includes(keyword));
}

/**
 * Extract movie name from tweet
 */
function extractMovieName(text) {
  for (const pattern of MOVIE_PATTERNS) {
    const match = text.match(pattern);
    if (match && match[1]) {
      return match[1].trim().replace(/\s+(?:by|directed by|from).*$/i, '');
    }
  }
  return 'Unknown Movie';
}

/**
 * Calculate rating based on tweet length
 */
function calculateRating(text, movieName) {
  const textWithoutName = text.replace(movieName, '');
  const charCount = textWithoutName.trim().length;
  
  if (charCount >= CONFIG.ratingThresholds.fiveStars) return 5;
  if (charCount >= CONFIG.ratingThresholds.fourStars) return 4;
  if (charCount >= CONFIG.ratingThresholds.threeStars) return 3;
  return 2;
}

/**
 * Analyze a single tweet
 */
function analyzeTweet(tweet) {
  if (!isMovieTweet(tweet.text)) return null;
  
  const movieName = extractMovieName(tweet.text);
  const rating = calculateRating(tweet.text, movieName);
  
  return {
    movieName,
    rating,
    tweetText: tweet.text,
    tweetId: tweet.id,
    createdAt: tweet.created_at,
    stars: '⭐'.repeat(rating)
  };
}

/**
 * Display reviews in console
 */
function displayReviews(reviews) {
  if (reviews.length === 0) {
    console.log('\n❌ No movie reviews found in recent tweets.\n');
    return;
  }
  
  console.log('\n' + '='.repeat(60));
  console.log(`🎬 KOJIMA'S MOVIE REVIEWS (${reviews.length} found)`);
  console.log('='.repeat(60) + '\n');
  
  reviews.forEach((review, index) => {
    console.log(`${index + 1}. ${review.movieName} → ${review.stars} (${review.rating}/5)`);
    console.log(`   📝 Tweet: ${review.tweetText.substring(0, 100)}...`);
    console.log(`   📅 Date: ${new Date(review.createdAt).toLocaleString()}\n`);
  });
  
  // Statistics
  const avgRating = (reviews.reduce((sum, r) => sum + r.rating, 0) / reviews.length).toFixed(2);
  const distribution = reviews.reduce((acc, r) => {
    acc[r.rating] = (acc[r.rating] || 0) + 1;
    return acc;
  }, {});
  
  console.log('='.repeat(60));
  console.log('📈 STATISTICS');
  console.log('='.repeat(60));
  console.log(`Total Reviews: ${reviews.length}`);
  console.log(`Average Rating: ${avgRating}⭐`);
  console.log('\nRating Distribution:');
  for (let i = 5; i >= 2; i--) {
    if (distribution[i]) {
      console.log(`  ${'⭐'.repeat(i)}: ${distribution[i]} reviews`);
    }
  }
  console.log('='.repeat(60) + '\n');
}

/**
 * Main function
 */
async function main() {
  try {
    // Validate configuration
    if (!CONFIG.bearerToken || CONFIG.bearerToken === 'your_bearer_token_here') {
      console.error('\n❌ Error: TWITTER_BEARER_TOKEN not set!');
      console.error('Please create a .env file with your Twitter API credentials.\n');
      console.error('Example:');
      console.error('TWITTER_BEARER_TOKEN=your_actual_token_here\n');
      process.exit(1);
    }
    
    console.log(`\n🔍 Fetching tweets from @${CONFIG.username}...`);
    
    // Initialize Twitter client
    const client = new TwitterApi(CONFIG.bearerToken);
    
    // Get user
    const user = await client.v2.userByUsername(CONFIG.username);
    if (!user.data) {
      throw new Error(`User @${CONFIG.username} not found`);
    }
    
    console.log(`✅ Found user: ${user.data.name}`);
    
    // Get tweets
    const tweets = await client.v2.userTimeline(user.data.id, {
      max_results: CONFIG.maxTweets,
      exclude: ['retweets', 'replies'],
      'tweet.fields': ['created_at']
    });
    
    console.log(`✅ Retrieved ${tweets.data.data.length} tweets`);
    console.log('\n🎬 Analyzing tweets for movie reviews...');
    
    // Analyze tweets
    const reviews = tweets.data.data
      .map(analyzeTweet)
      .filter(review => review !== null);
    
    // Display results
    displayReviews(reviews);
    
  } catch (error) {
    console.error('\n❌ Error:', error.message);
    if (error.code === 401) {
      console.error('Authentication failed. Please check your bearer token.\n');
    } else if (error.code === 429) {
      console.error('Rate limit exceeded. Please wait before trying again.\n');
    }
    process.exit(1);
  }
}

// Run the application
if (require.main === module) {
  main();
}

module.exports = { isMovieTweet, extractMovieName, calculateRating, analyzeTweet };

// Made with Bob
