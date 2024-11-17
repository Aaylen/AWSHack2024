from flask import Blueprint, request, jsonify
import boto3
import os
import yfinance as yf

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
    Analyzes user input and handles follow-up questions for the same stock.
    """
    try:
        data = request.get_json()
        user_question = data.get("question", "").strip()
        if not user_question:
            return jsonify({"error": "No question provided"}), 400

        # Check if the user is asking a follow-up question about the same stock
        if hasattr(claude, 'current_stock') and claude.current_stock:
            stock_data = claude.current_stock
            follow_up_prompt = f"""
            Based on the user's follow-up question: '{user_question}', 
            and this data about {stock_data['ticker']}:
            {stock_data['data']}
            
            Answer the user's question in a concise manner.
            """
            response = send_message_to_claude(follow_up_prompt)
            return jsonify({
                "response": response,
                "ticker": stock_data["ticker"]
            })

        # If no stock context exists, proceed with a new analysis
        prompt = f"""
        Correlate the user's question with a stock ticker symbol. 
        Give a one word response with that ticker symbol in all capital letters.
        If there is no related stock ticker symbol, respond with 'none'.
        {user_question}
        """
        ticker = send_message_to_claude(prompt).upper().strip()
        if ticker == "NONE":
            return jsonify({"response": "No related stock found", "ticker": ""})

        # Fetch and analyze new stock data
        data = get_stock_data(ticker)
        claude.current_stock = {"ticker": ticker, "data": data}  # Store in variable for future use
        
        analysis_prompt = f"""
        Analyze the health of {ticker} based on this data: {data}
        Choose 3 statistics from the financial statements that stand out.
        Format your response exactly like this, including the line breaks:
        
        Overall Assessment:
        [One sentence summary of company's financial health]
        
        Key Metrics:
        • [First statistic that stands out and its implication]
        • [Second statistic that stands out and its implication]
        • [Third statistic that stands out and its implication]
        
        Future Outlook:
        [1-2 sentences about what the company should focus on]

        Score: [A score from 1-100, over 50 is bullish under 50 is bearish]
        """
        response = send_message_to_claude(analysis_prompt)
        sections = response.split('\n\n')
        formatted_response = '\n\n'.join(section.strip() for section in sections if section.strip())
        
        # Extract score and delete it from the response
        score_line = next((line for line in formatted_response.split("\n") if "Score:" in line), None)
        score = None
        if score_line:
            score = score_line.split(":")[1].strip()
            formatted_response = formatted_response.replace(score_line, "")  # Remove the score line
        print(score)
        return jsonify({
            "response": formatted_response,
            "ticker": ticker,
            "score": score
        })
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

def get_stock_data(ticker):
    """
    Fetches financial data for a given stock ticker using yfinance.
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Get key financial metrics
        data = {
            "company_name": info.get("shortName", "Unknown Company"),
            "current_price": info.get("currentPrice", "N/A"),
            "market_cap": info.get("marketCap", "N/A"),
            "pe_ratio": info.get("trailingPE", "N/A"),
            "dividend_yield": info.get("dividendYield", "N/A"),
            "business_summary": info.get("longBusinessSummary", "No summary available"),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "52_week_high": info.get("fiftyTwoWeekHigh", "N/A"),
            "52_week_low": info.get("fiftyTwoWeekLow", "N/A")
        }
        
        return data
    except Exception as e:
        raise ValueError(f"Failed to fetch stock data: {e}")
