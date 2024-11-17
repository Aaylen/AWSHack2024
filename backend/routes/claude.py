import boto3
from flask import Blueprint, request, jsonify
import os
import requests
from datetime import datetime

claude = Blueprint('claude', __name__)

# AWS Bedrock Configuration
try:
    client = boto3.client(
        "bedrock-runtime",
        region_name=os.getenv("AWS_DEFAULT_REGION", "us-west-2"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
    )
    model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
except Exception as e:
    raise RuntimeError(f"Failed to configure AWS Bedrock client: {e}")


def send_message_to_claude(user_message):
    """
    Sends a message to Claude for processing user input.
    """
    conversation = [{"role": "user", "content": [{"text": user_message}]}]
    try:
        response = client.converse(
            modelId=model_id,
            messages=conversation,
            inferenceConfig={"maxTokens": 2000, "temperature": 0},
            additionalModelRequestFields={"top_k": 250},
        )
        return response.get("output", {}).get("message", {}).get("content", [{}])[0].get("text", "No response")
    except Exception as e:
        return f"ERROR: Unable to connect to Claude API. Details: {e}"


@claude.route('/analyze', methods=['POST'])
def analyze():
    """
    Analyzes user input and routes the request to the appropriate service.
    """
    try:
        data = request.get_json()
        user_question = data.get("question", "").strip()
        if not user_question:
            return jsonify({"error": "No question provided"}), 400

        # Determine intent
        analysis_prompt = f"""
        Analyze the following question: '{user_question}'
        Is the user asking about:
        1. News
        2. Stock data
        3. General query
        Respond with "news", "stock", or "general" only.
        """
        intent = send_message_to_claude(analysis_prompt).lower().strip()

        # Route request
        if intent == "news":
            return handle_news_request(user_question)
        elif intent == "stock":
            return handle_stock_request(user_question)
        else:
            ai_response = send_message_to_claude(user_question)
            return jsonify({"response": ai_response})
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500


def handle_news_request(user_question):
    """
    Processes a news request by extracting the relevant topic.
    """
    # Extract topic from the user question
    analysis_prompt = f"""
    Extract the main topic from the following question: '{user_question}'
    Use one of the following predefined topics: blockchain, earnings, ipo, mergers_and_acquisitions,
    financial_markets, economy_fiscal, economy_monetary, economy_macro, energy_transportation,
    finance, life_sciences, manufacturing, real_estate, retail_wholesale, technology.
    Respond with the topic name only.
    """
    topic = send_message_to_claude(analysis_prompt).lower().strip()
    
    # Default topic to "technology" if none is extracted
    topic = topic if topic in [
        "blockchain", "earnings", "ipo", "mergers_and_acquisitions",
        "financial_markets", "economy_fiscal", "economy_monetary", "economy_macro",
        "energy_transportation", "finance", "life_sciences", "manufacturing",
        "real_estate", "retail_wholesale", "technology"
    ] else "technology"

    apikey = os.getenv("YOUR_ALPHA_VANTAGE_API_KEY")
    time_from = datetime.utcnow().strftime("%Y%m%dT%H%M")

    try:
        # Call the Alpha Vantage News API
        response = requests.get(
            "https://www.alphavantage.co/query",
            params={
                "function": "NEWS_SENTIMENT",
                "topics": topic,
                "time_from": time_from,
                "limit": 100,
                "apikey": apikey,
            },
        )
        response.raise_for_status()
        news_data = response.json()

        # Analyze sentiment and provide advice
        sentiment_score = news_data.get("sentiment_score", 0)
        if sentiment_score > 0.5:
            advice = "Based on the news sentiment, it seems like a good time to invest in this sector."
        else:
            advice = "The news sentiment suggests caution when considering investments in this sector."

        return jsonify({
            "topic": topic,
            "sentiment_score": sentiment_score,
            "advice": advice,
            "articles": news_data.get("articles", [])
        })
    except Exception as e:
        return jsonify({"error": f"Failed to fetch news data: {e}"}), 500


def handle_stock_request(user_question):
    """
    Processes a stock request.
    """
    stock_data = {
        "action": "display_stock",
        "ticker": "AAPL",  # Example ticker
        "entry": "5d",  # Fetch 5 days of stock data
    }
    try:
        response = requests.post(
            "http://127.0.0.1:5000/stocks/endpoint", json=stock_data
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return jsonify({"error": f"Failed to fetch stock data: {e}"}), 500
