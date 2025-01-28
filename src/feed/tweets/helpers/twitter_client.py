import logging
import os
import requests
from requests_oauthlib import OAuth1
from dotenv import load_dotenv
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
load_dotenv()

def validate_env_vars():
    required_vars = [
        "TWITTER_API_KEY", 
        "TWITTER_API_SECRET",
        "TWITTER_ACCESS_TOKEN", 
        "TWITTER_ACCESS_SECRET"
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

class TwitterClient:
    def __init__(self):
        self.api_key = os.getenv("TWITTER_API_KEY")
        self.api_secret = os.getenv("TWITTER_API_SECRET")
        self.access_token = os.getenv("TWITTER_ACCESS_TOKEN")
        self.access_secret = os.getenv("TWITTER_ACCESS_SECRET")
        self.api_url = "https://api.x.com/2/tweets"
        
        if not all([self.api_key, self.api_secret, self.access_token, self.access_secret]):
            raise EnvironmentError("Missing Twitter API credentials in environment variables.")
        
        self.auth = OAuth1(
            self.api_key,
            self.api_secret,
            self.access_token,
            self.access_secret
        )
        self.headers = {"Content-Type": "application/json"}
    
    def post_tweet(self, text, media_ids=None):
        payload = {"text": text}
        if media_ids:
            payload["media"] = {"media_ids": media_ids}
        
        try:
            response = requests.post(
                self.api_url,
                json=payload,
                auth=self.auth,
                headers=self.headers
            )
            response_data = response.json()

            if response.status_code == 201:
                logging.info(f"Tweet posted successfully: {response_data}")
                return response_data
            else:
                error = response_data.get("detail", "Unknown error occurred")
                logging.error(f"Failed to post tweet: {response.status_code} - {error}")
                return {"status": "error", "details": response_data}
        except requests.RequestException as e:
            logging.exception(f"Request failed: {e}")
            return {"status": "error", "message": str(e)}

    def get_tweet(self, tweet_id):
        url = f"{self.api_url}/{tweet_id}"
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response.json()
            else:
                logging.error(f"Failed to retrieve tweet: {response.status_code}")
                return None
        except requests.RequestException as e:
            logging.exception(f"Failed to retrieve tweet: {e}")
            return None
        
    def get_user_id(self, username):
        """Resolve a username to a user ID."""
        url = f"https://api.twitter.com/2/users/by/username/{username}"
        try:
            response = requests.get(url, headers=self.headers, auth=self.auth)
            if response.status_code == 200:
                data = response.json().get("data", {})
                return data.get("id")
            else:
                logging.error(f"Failed to get user ID: {response.status_code}")
                return None
        except requests.RequestException as e:
            logging.exception(f"Failed to get user ID: {e}")
            return None

    def get_user_tweets(self, user_id, max_results=100, start_time=None, pagination_token=None):
        """Fetch user tweets with pagination and start_time support."""
        url = f"https://api.twitter.com/2/users/{user_id}/tweets"
        params = {
            "max_results": max_results,
            "tweet.fields": "created_at"
        }
        if start_time:
            params["start_time"] = start_time
        if pagination_token:
            params["pagination_token"] = pagination_token
        try:
            response = requests.get(url, headers=self.headers, params=params, auth=self.auth)
            if response.status_code == 200:
                response_json = response.json()
                data = response_json.get("data", [])
                meta = response_json.get("meta", {})
                next_token = meta.get("next_token", None)
                return data, next_token
            else:
                logging.error(f"Failed to fetch user tweets: {response.status_code}")
                return None, None
        except requests.RequestException as e:
            logging.exception(f"Failed to fetch user tweets: {e}")
            return None, None