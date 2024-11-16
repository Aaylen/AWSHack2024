from flask import Blueprint, jsonify, request
import boto3
from routes.news import fetch_most_recent_sentiment
from routes.stocks import fetch_stock_data

claude = Blueprint('claude', __name__)

# AWS Bedrock Configuration
client = boto3.client("bedrock-runtime", region_name="us-west-2")
model_id = "anthropic.claude-3-sonnet-20240229-v1:0"

def send_message_to_claude(user_message):
    """
    Sends a message to Claude 3 Sonnet for processing user input or re-analysis.
    """
    conversation = [{"role": "user", "content": [{"text": user_message}]}]
    try:
        response = client.converse(
            modelId=model_id,
            messages=conversation,
            inferenceConfig={"maxTokens": 2000, "temperature": 0},
            additionalModelRequestFields={"top_k": 250},
        )
        return response["output"]["message"]["content"][0]["text"]
    except Exception as e:
        return f"ERROR: AWS Bedrock issue - {e}"

@claude.route('/analyze', methods=['POST'])
def analyze():
    """
    Analyzes the user's question to determine the appropriate API to call (news or stocks).
    Fetches data, analyzes it, and provides an investment recommendation.
    """
    data = request.get_json()
    user_question = data.get("question", "")
    if not user_question:
        return jsonify({"error": "No question provided"}), 400

    # Send question to Claude to determine the appropriate API
    ai_prompt = f"""
    Analyze the following question: '{user_question}'
    Based on the question, determine if it is related to 'news' or 'stocks'.
    Return only the relevant category as a single word: 'news' or 'stocks'.
    """
    print(f"[DEBUG] Sending question to Claude: {user_question}")
    api_decision = send_message_to_claude(ai_prompt).strip().lower()
    print(f"[DEBUG] Claude decision: {api_decision}")

    if api_decision == "news":
        # Extract topic from the user's question
        topic_prompt = f"""
        Extract the topic of interest from the question: '{user_question}'.
        Provide a single keyword representing the topic.
        """
        topic = send_message_to_claude(topic_prompt).strip().lower()
        print(f"[DEBUG] Extracted topic for news: {topic}")

        # Fetch news sentiment
        sentiment_data = fetch_most_recent_sentiment("YOUR_ALPHA_VANTAGE_API_KEY", topic)
        if "error" in sentiment_data:
            return jsonify({"error": sentiment_data["error"]}), 500

        # Prepare data for AI analysis
        articles = sentiment_data["articles"]
        sentiment_scores = sentiment_data["sentiment_scores"]
        article_summaries = "\n".join(
            [f"Title: {article['title']}\nSummary: {article['summary']}\nSentiment Score: {article['sentiment_score']}\n"
             for article in articles]
        )
        ai_analysis_prompt = f"""
        Based on the following articles and sentiment scores, determine if it's a good time to invest in {topic}.
        Sentiment Scores: {sentiment_scores}
        Articles:
        {article_summaries}
        Provide a clear recommendation: "Invest" or "Do Not Invest" with an explanation.
        """
        recommendation = send_message_to_claude(ai_analysis_prompt)
        return jsonify({"recommendation": recommendation, "sentiment_scores": sentiment_scores, "articles": articles})

    elif api_decision == "stocks":
        # Extract stock symbol from the user's question
        stock_prompt = f"""
        Extract the stock symbol of interest from the question: '{user_question}'.
        Provide the stock symbol as a single word.
        """
        stock_symbol = send_message_to_claude(stock_prompt).strip().upper()
        print(f"[DEBUG] Extracted stock symbol: {stock_symbol}")

        # Fetch stock data
        stock_data = fetch_stock_data(stock_symbol)
        if "error" in stock_data:
            return jsonify({"error": stock_data["error"]}), 500

        # Prepare data for AI analysis
        stock_summary = json.dumps(stock_data, indent=2)
        ai_analysis_prompt = f"""
        Based on the following stock data for {stock_symbol}, determine if it's a good time to invest.
        Stock Data:
        {stock_summary}
        Provide a clear recommendation: "Invest" or "Do Not Invest" with an explanation.
        """
        recommendation = send_message_to_claude(ai_analysis_prompt)
        return jsonify({"recommendation": recommendation, "stock_data": stock_data})

    else:
        return jsonify({"error": "Unable to determine the appropriate API to call."}), 400
