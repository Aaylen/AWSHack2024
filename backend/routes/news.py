from flask import Blueprint, jsonify, request
import requests
from datetime import datetime, timedelta

# Create the Blueprint
news = Blueprint('news', __name__)

def fetch_economy_sentiment(api_key, time_from=None, time_to=None, limit=50):
    """
    Fetches news sentiment data about the economy from the Alpha Vantage API and calculates sentiment.
    """
    topic = "economy_macro"
    url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&apikey={api_key}"
    if time_from:
        url += f"&time_from={time_from}"
    if time_to:
        url += f"&time_to={time_to}"
    url += f"&topics={topic}&limit={limit}"

    response = requests.get(url)
    if response.status_code != 200:
        return {"error": f"Failed to fetch data. Status Code: {response.status_code}"}

    data = response.json()

    # Handle case with no articles
    if "feed" not in data or not data["feed"]:
        return {"error": "No news articles found for the given parameters."}

    # Process sentiment scores
    sentiment_scores = [float(article["overall_sentiment_score"]) for article in data["feed"]]
    average_sentiment = sum(sentiment_scores) / len(sentiment_scores)

    # Determine market trend
    if average_sentiment > 0.2:
        trend = "Bullish Economy"
    elif average_sentiment < -0.2:
        trend = "Bearish Economy"
    else:
        trend = "Neutral Economy"

    return {
        "average_sentiment_score": average_sentiment,
        "economic_trend": trend,
        "article_count": len(data["feed"]),
        "articles_analyzed": [
            {
                "title": article["title"],
                "summary": article["summary"],
                "sentiment_score": float(article["overall_sentiment_score"]),
                "published_at": article["time_published"],
            }
            for article in data["feed"]
        ],
    }

@news.route('/endpoint', methods=['POST'])
def post_endpoint():
    """
    Endpoint to fetch and return economy sentiment data.
    """
    # Get JSON data from the request
    request_data = request.get_json()
    if not request_data:
        return jsonify({"error": "Invalid or missing JSON data"}), 400

    api_key = request_data.get("api_key")
    time_range = request_data.get("time_range", "weekly")  # Default to weekly
    limit = request_data.get("limit", 50)

    # Validate API key
    if not api_key:
        return jsonify({"error": "API key is required"}), 400

    # Set time range
    now = datetime.utcnow()
    if time_range == "daily":
        time_from = (now - timedelta(days=1)).strftime("%Y%m%dT%H%M")
    elif time_range == "monthly":
        time_from = (now - timedelta(days=30)).strftime("%Y%m%dT%H%M")
    elif time_range == "yearly":
        time_from = (now - timedelta(days=365)).strftime("%Y%m%dT%H%M")
    else:  # Default to weekly
        time_from = (now - timedelta(days=7)).strftime("%Y%m%dT%H%M")
    time_to = now.strftime("%Y%m%dT%H%M")

    # Fetch economy sentiment
    result = fetch_economy_sentiment(api_key, time_from, time_to, limit)
    if "error" in result:
        return jsonify({"error": result["error"]}), 500

    return jsonify(result)
