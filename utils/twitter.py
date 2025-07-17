from tweepy import Client
from typing import List, Dict, Optional
import logging

class Twitter:
    def __init__(
        self,
        bearer_token: str,
        consumer_key: str,
        consumer_secret: str,
        access_token: str,
        access_token_secret: str,
    ):
        self.client = Client(
            bearer_token=bearer_token,
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
        )

    def post_tweet(self, message: str) -> Optional[str]:
        """Posts a tweet and returns the tweet ID."""
        try:
            response = self.client.create_tweet(text=message)
            return response.data["id"]
        except Exception as e:
            logging.error(f"Error posting tweet: {e}")
            return None

    def get_posted_tweets(self, user_id: str, limit: int = 5) -> List[Dict]:
        """Gets the latest tweets posted by the given user ID."""
        try:
            response = self.client.get_users_tweets(id=user_id, max_results=limit)
            if response.data:
                return [{"id": tweet.id, "text": tweet.text} for tweet in response.data]
            return []
        except Exception as e:
            logging.error(f"Error fetching tweets: {e}")
            return []

    def delete_tweet(self, tweet_id: str) -> bool:
        """Deletes a tweet by ID."""
        try:
            self.client.delete_tweet(tweet_id)
            return True
        except Exception as e:
            logging.error(f"Error deleting tweet: {e}")
            return False


# -------- Example usage:

# CONSUMER_KEY = "your_consumer_key"
# CONSUMER_SECRET = "your_consumer_secret"
# BEARER_TOKEN = "your_bearer_token"
# ACCES_TOKEN = "your_access_token"
# ACCES_TOKEN_SECRET = "your_access_token_secret"

# client = Twitter(
#     bearer_token=BEARER_TOKEN,
#     consumer_key=CONSUMER_KEY,
#     consumer_secret=CONSUMER_SECRET,
#     access_token=ACCES_TOKEN,
#     access_token_secret=ACCES_TOKEN_SECRET,
# )

# ✅ Post a tweet
# tweet_id = twitter.post_tweet("Hello Twitter API v2 from Python! 🚀")
# print("Tweet ID:", tweet_id)

# # ✅ Fetch latest tweets (you'll need your numeric user ID, not username)
# user_id = "1269870663059283968"  # Replace with your actual user ID
# tweets = twitter.get_posted_tweets(user_id=user_id, limit=3)
# print("Recent Tweets:", tweets)

# # ✅ Delete a tweet
# if tweet_id:
#     deleted = twitter.delete_tweet(tweet_id)
#     print("Tweet deleted?" , deleted)