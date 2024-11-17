import boto3
from flask import Blueprint, request, jsonify
import os
import requests  # To call news and stock APIs


claude = Blueprint('claude', __name__)


# AWS Bedrock Configuration using environment variables
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
    Sends a message to Claude 3 Sonnet for processing user input or re-analysis.
    """
    conversation = [{"role": "user", "content": [{"text": user_message}]}]


    try:
        # Send the request to AWS Bedrock
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
    Receives a user question, analyzes intent, and routes to appropriate service.
    """
    try:
        # Parse incoming request
        data = request.get_json()
        user_question = data.get("question", "").strip()
       
        if not user_question:
            return jsonify({"error": "No question provided"}), 400


        # Use Claude to analyze intent
        analysis_prompt = f"""
        Analyze the following question: '{user_question}'
        Is the user asking about:
        1. News
        2. Stock data
        3. General query
        Respond with "news", "stock", or "general" only.
        """
        intent = send_message_to_claude(analysis_prompt).lower().strip()


        # Route based on intent
        if intent == "news":
            return handle_news_request(user_question)
        elif intent == "stock":
            return handle_stock_request(user_question)
        else:
            # General query handled by Claude
            ai_response = send_message_to_claude(user_question)
            return jsonify({"response": ai_response})
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500




def handle_news_request(user_question):
    """
    Handles requests related to news sentiment.
    """
    # Modify based on extracted intent (e.g., topics)
    topics = "technology,ai"
    apikey = os.getenv("YOUR_ALPHA_VANTAGE_API_KEY")
    response = requests.post(
        "http://127.0.0.1:5000/news/news_sentiment",
        json={"apikey": apikey, "topics": topics, "limit": 1000},
    )
    return response.json()




def handle_stock_request(user_question):
    """
    Handles requests related to stock data.
    """
    # Example: Use stock symbol (e.g., AAPL) extracted from user_question
    stock_data = {
        "action": "display_stock",
        "ticker": "AAPL",
        "entry": "5d",  # Fetch 5 days of stock data
    }
    response = requests.post(
        "http://127.0.0.1:5000/stocks/endpoint", json=stock_data
    )
    return response.json()


