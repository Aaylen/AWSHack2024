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
        print("User question:", user_question)
        prompt = f"""
        Correlate the user's question with a stock ticker symbol. 
        Give a one word response with that ticker symbol.
        If there is no related stock ticker symbol, respond with 'none'.
        {user_question}
        """
        ticker = send_message_to_claude(prompt).lower().strip()
        print("Ticker:", ticker)
        # Route request
        prompt = f"""
        Give an overview of the company with the ticker symbol {ticker}
        Limit the response to 3 sentences.
        """
        response = send_message_to_claude(prompt)
        return jsonify({
            "response": response,
            "ticker": ticker
            })
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500
    

