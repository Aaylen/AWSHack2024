from flask import Blueprint, jsonify, request
import requests

# Create the Blueprint
news = Blueprint('news', __name__)

def fetch_recent_sentiment(api_key, topic, limit=1000):
    """
    Fetches the most recent sentiment data for a given topic from the Alpha Vantage API.
    """
    url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&apikey={api_key}&topics={topic}&limit={limit}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Handle case with no articles
        if "feed" not in data or not data["feed"]:
            return {"error": "No news articles found for the given parameters."}

        return {
            "sentiment_scores": [float(article["overall_sentiment_score"]) for article in data["feed"]],
            "articles": [
                {
                    "title": article["title"],
                    "summary": article["summary"],
                    "sentiment_score": float(article["overall_sentiment_score"]),
                    "published_at": article["time_published"],
                }
                for article in data["feed"]
            ],
        }
    except requests.RequestException as e:
        return {"error": f"API request error: {e}"}
    except Exception as e:
        return {"error": f"Unexpected error: {e}"}

@news.route('/recent', methods=['POST'])
def get_recent_news_sentiment():
    """
    Endpoint to fetch the most recent sentiment data for a given topic.
    """
    # Get JSON data from the request
    request_data = request.get_json()
    if not request_data:
        return jsonify({"error": "Invalid or missing JSON data"}), 400

    api_key = request_data.get("api_key")
    topic = request_data.get("topic", "technology")  # Default topic: technology

    # Validate required inputs
    if not api_key:
        return jsonify({"error": "API key is required"}), 400
    if not topic:
        return jsonify({"error": "Topic is required"}), 400

    # Fetch the most recent sentiment data
    result = fetch_recent_sentiment(api_key, topic)
    if "error" in result:
        return jsonify({"error": result["error"]}), 500

    return jsonify(result)
