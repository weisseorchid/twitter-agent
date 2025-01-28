import json
from datetime import datetime, timedelta, timezone
from src.helpers.twitter_client import TwitterClient

def main():
    parser = argparse.ArgumentParser(description="Fetch a user's tweets from the past year.")
    parser.add_argument("username", help="Twitter username to fetch tweets from")
    args = parser.parse_args()

    twitter = TwitterClient()

    # Resolve username to user ID
    user_id = twitter.get_user_id(args.username)
    if not user_id:
        print(f"Error: User '{args.username}' not found.")
        return

    # Calculate start_time (one year ago in UTC)
    now_utc = datetime.now(timezone.utc)
    one_year_ago = now_utc - timedelta(days=365)
    start_time = one_year_ago.isoformat(timespec="seconds").replace("+00:00", "Z")

    all_tweets = []
    next_token = None

    print(f"Fetching tweets for @{args.username} (ID: {user_id})...")
    while True:
        tweets, next_token = twitter.get_user_tweets(
            user_id=user_id,
            max_results=100,
            start_time=start_time,
            pagination_token=next_token
        )
        if tweets is None:
            print("Error occurred while fetching tweets.")
            break

        all_tweets.extend(tweets)
        print(f"Fetched {len(tweets)} tweets (total: {len(all_tweets)})")

        if not next_token:
            break  # Exit loop when there are no more pages

    # Save to JSON
    filename = f"{args.username}_tweets.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(all_tweets, f, indent=2, ensure_ascii=False)
    print(f"Successfully saved {len(all_tweets)} tweets to {filename}")

if __name__ == "__main__":
    import argparse
    main()