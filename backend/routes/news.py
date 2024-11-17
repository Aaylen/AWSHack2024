import requests
from flask import Blueprint, jsonify, request
import os


news = Blueprint('news', __name__)


# Alpha Vantage News API Endpoint
API_BASE_URL = "https://www.alphavantage.co/query"


@news.route('/news_sentiment', methods=['POST'])
def fetch_recent_sentiment_endpoint():
    """
    Flask endpoint to fetch recent news sentiment data.
    """
    try:
        data = request.get_json()
        apikey = data.get("apikey", os.getenv("YOUR_ALPHA_VANTAGE_API_KEY"))
        topics = data.get("topics", "technology,ai")
        limit = data.get("limit", 1000)


        if not apikey:
            return jsonify({"error": "API key is required"}), 400


        sentiment_data = fetch_recent_sentiment(apikey, topics, limit)
        return jsonify(sentiment_data)
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500




def fetch_recent_sentiment(apikey, topics, limit=1000):
    """
    Fetches recent news sentiment data for the given topics using the Alpha Vantage API.
   
    Args:
        apikey (str): Your Alpha Vantage API key.
        topics (str): Topics to filter articles by (comma-separated).
        limit (int): Maximum number of articles to fetch (default 1000).


    Returns:
        dict: JSON response containing articles and sentiment analysis.
    """
    try:
        # Construct the API request URL
        params = {
            "function": "NEWS_SENTIMENT",
            "topics": topics,
            "limit": limit,
            "apikey": apikey
        }


        response = requests.get(API_BASE_URL, params=params)
        if response.status_code != 200:
            return {"error": f"Failed to fetch news data. Status code: {response.status_code}"}


        data = response.json()


        # Handle potential errors in the API response
        if "error" in data:
            return {"error": data["error"]}


        return data  # Return the entire JSON response
    except Exception as e:
        return {"error": f"An error occurred while fetching news data: {e}"}
