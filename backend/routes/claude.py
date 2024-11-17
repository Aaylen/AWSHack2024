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
            inferenceConfig={"maxTokens": 2000, "temperature": 0.5},
            additionalModelRequestFields={"top_k": 50},
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
        1. General stock inquiry (e.g., "How is the market today?")
        2. Specific stock statistics (e.g., "Show me AAPL chart").
        Respond with "general" or "specific".
        """
        classification = send_message_to_claude(analysis_prompt).lower().strip()
        print(f"Classification: {classification}")

        if classification == "general":
            return handle_general_stock_question(user_question)
        elif classification == "specific":
            return handle_specific_stock_question(user_question)
        else:
            return jsonify({"error": "Unable to classify the question."}), 400
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500


def handle_general_stock_question(user_question):
    """
    Handles general stock inquiries and provides a summary.
    """
    general_prompt = f"""
    Provide a brief summary of the current stock market based on the question: '{user_question}'.
    Keep the response under 25 words.
    """
    response = send_message_to_claude(general_prompt)
    return jsonify({"response": response})


def handle_specific_stock_question(user_question):
    """
    Processes specific stock requests.
    """
    # Extract ticker and intent using Claude
    analysis_prompt = f"""
    From the following question: '{user_question}', extract:
    1. The stock ticker symbol (e.g., AAPL, MSFT, etc.).
    2. The user's intent (e.g., "show chart", "average return", "best days").
    Respond with the stock ticker followed by the intent in this format: 'TICKER INTENT' only.
    """
    extracted_info = send_message_to_claude(analysis_prompt).strip()
    try:
        # Parse the extracted information
        ticker, intent = extracted_info.split()
        ticker = ticker.upper()
        intent = intent.lower()

        # Build stock request payload
        if intent == "chart":
            stock_data = {"action": "display_stock", "ticker": ticker, "entry": "5d"}
        elif intent == "average_return":
            stock_data = {
                "action": "average_return",
                "stock": ticker,
                "start_date": "2023-01-01",
                "end_date": datetime.now().strftime("%Y-%m-%d"),
            }
        elif intent == "best_days":
            stock_data = {
                "action": "best_days",
                "stock": ticker,
                "start_date": "2023-01-01",
                "end_date": datetime.now().strftime("%Y-%m-%d"),
                "days": 5,
            }
        else:
            return jsonify({"error": f"Unknown intent: {intent}"}), 400

        # Debug: Log the stock payload
        print(f"Stock payload: {stock_data}")

        # Call the stocks API endpoint
        response = requests.post(
            "http://127.0.0.1:5000/stocks/endpoint", json=stock_data
        )
        response.raise_for_status()
        stock_response = response.json()

        # Return stock data directly
        return jsonify({"response": stock_response})
    except Exception as e:
        return jsonify({"error": f"Failed to process stock request: {e}"}), 500
