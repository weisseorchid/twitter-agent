import logging
import os
from datetime import datetime
from dotenv import load_dotenv
from src.helpers.gemini_client import GeminiClient
from src.helpers.twitter_client import TwitterClient
import sys

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

load_dotenv()

def validate_env_vars():
    required_vars = [
        "TWITTER_API_KEY", 
        "TWITTER_API_SECRET",
        "TWITTER_ACCESS_TOKEN", 
        "TWITTER_ACCESS_SECRET",
        "TWITTER_BEARER_TOKEN",
        "GEMINI_API_KEY"
    ]
    for var in required_vars:
        if not os.getenv(var):
            raise EnvironmentError(f"Missing required environment variable: {var}")

validate_env_vars()

log_level = os.getenv("LOGGING_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, log_level, logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

def main():
    # Generate tweet content
    gemini = GeminiClient()
    tweet_text = gemini.generate_tweet("Current trends: AI automation, productivity hacks, bootstrapping startups, sales strategies")
    logging.info(f"Tweet content: {tweet_text}")

    try:
        twitter_client = TwitterClient()

        # Post tweet
        response = twitter_client.post_tweet(tweet_text)

        if response.get("data") and response["data"].get("id"):
            tweet_id = response["data"]["id"]
            logging.info(f"Tweet posted successfully with ID: {tweet_id}")

            # Retrieve posted tweet
            retrieved_tweet = twitter_client.get_tweet(tweet_id)
            if retrieved_tweet:
                logging.info(f"Retrieved tweet: {retrieved_tweet}")

            # Fetch user tweets
            user_id = 1234567890  # Replace with a valid user ID
            user_tweets = twitter_client.get_user_tweets(user_id)
            if user_tweets:
                for tweet in user_tweets:
                    logging.info(f"User Tweet: {tweet}")
            else:
                logging.info("No tweets found for the user.")
        else:
            logging.error("Failed to post tweet.")

    except Exception as e:
        logging.exception(f"An error occurred: {e}")

if __name__ == "__main__":
    main()