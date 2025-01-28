# Twitter Agent

This project implements a Twitter agent that generates and posts tweets using the Gemini AI model and the Twitter API. It leverages Retrieval Augmented Generation (RAG) to create contextually relevant tweets based on current trends and example tweets.

## Features

- **Tweet Generation:** Uses Gemini AI to generate engaging tweets based on provided trend context and similar example tweets
- **RAG Enhancement:** Employs RAG to improve tweet relevance by retrieving and incorporating information from a dataset of example tweets
- **Automated Posting:** Posts generated tweets to Twitter using the Twitter API
- **Tweet Retrieval:** Retrieves specific tweets by ID
- **User Tweet Retrieval:** Fetches a user's tweets, including pagination and time-based filtering
- **Environment Variable Configuration:** Uses environment variables for API keys and other sensitive information
- **Logging:** Implements logging for debugging and monitoring
- **Data Export:** Exports user tweets to a JSON file

## Installation

1. Clone the repository:
    ```bash
    git clone [repository-url]
    cd twitter-agent
    ```

2. Create a virtual environment:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file:
    ```env
    COMET_API_KEY=your_comet_api_key  # Optional
    TWITTER_API_KEY=your_twitter_api_key
    TWITTER_API_SECRET=your_twitter_api_secret
    TWITTER_ACCESS_TOKEN=your_twitter_access_token
    TWITTER_ACCESS_SECRET=your_twitter_access_secret
    GEMINI_API_KEY=your_gemini_api_key
    DRY_RUN=True  # Set to False to actually post
    LOG_LEVEL=INFO
    ```

5. Prepare RAG data (optional):
    Create a directory (e.g., `feed/tweets`) containing JSON files with example tweets:
    ```json
    [
      {"text": "Example tweet 1 text", "tags": ["tag1", "tag2"]},
      {"text": "Example tweet 2", "tags": ["tag3"]}
    ]
    ```

## Usage

### Generating and Posting Tweets
```bash
python src/main.py
```

### Fetching User Tweets
```bash
python src/fetch_tweets.py <username>
```

## File Structure
```
twitter-agent/
├── .env                # Environment variables
├── .env.example        # Example .env file
├── requirements.txt    # Project dependencies
├── setup.py           # Package setup
└── src/
     ├── helpers/
     │   ├── gemini_client.py   # Gemini API interaction
     │   └── twitter_client.py  # Twitter API interaction
     ├── main.py             # Main script
     ├── fetch_tweets.py     # Tweet fetching script
     └── data/              # RAG data directory
          └── tweets/
                └── example_tweets.json
```

## Development

1. Install setuptools:
    ```bash
    pip install setuptools
    ```

2. Install in editable mode:
    ```bash
    pip install -e .
    ```

## Contributing
Contributions are welcome! Please open an issue or submit a pull request.

## License
MIT License