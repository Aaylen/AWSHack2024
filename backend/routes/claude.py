import os
import requests
from datetime import datetime
import yfinance as yf
from flask import Blueprint, jsonify, request
import boto3

claude = Blueprint('claude', __name__)

# Initialize an in-memory conversation history
conversation_history = []

# AWS Bedrock Configuration
try:
    client = boto3.client(
        "bedrock-runtime",
        region_name=os.getenv("AWS_DEFAULT_REGION", "us-west-2"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
    )
except Exception as e:
    raise RuntimeError(f"Failed to configure AWS Bedrock client: {e}")


def send_message_to_claude(user_message):
    """
    Sends a message to Claude for processing user input.
    """
    conversation = [{"role": "user", "content": [{"text": user_message}]}]
    try:
        response = client.converse(
            modelId="anthropic.claude-3-sonnet-20240229-v1:0",
            messages=conversation,
            inferenceConfig={"maxTokens": 2000, "temperature": 0.5},
            additionalModelRequestFields={"top_k": 50},
        )
        return response.get("output", {}).get("message", {}).get("content", [{}])[0].get("text", "No response")
    except Exception as e:
        return f"ERROR: Unable to connect to Claude API. Details: {e}"


def send_message_to_claude_with_memory(user_question):
    """
    Checks if the user's question is a follow-up based on the conversation history and processes it.
    """
    # Step 1: Check if this is a follow-up question
    follow_up_prompt = f"""
    The user has asked: "{user_question}"

    Below is the previous conversation history:
    {conversation_history if conversation_history else "No prior conversation history."}

    Is the new question a follow-up to the previous conversation? if it is helpe the user limit of 30 words, 
    please dont restate the question and say this is a 30 word repsonse 
    """
    follow_up_response = send_message_to_claude(follow_up_prompt).strip()
    print("Follow-Up Analysis Response:", follow_up_response)

    # Step 2: Add new question to the conversation history
    conversation_history.append({"question": user_question, "follow_up_response": follow_up_response})

    # If the question is a follow-up, handle it accordingly
    if "yes" in follow_up_response.lower():
        return {
            "follow_up": True,
            "follow_up_analysis": follow_up_response,
            "conversation_history": conversation_history
        }

    # If not a follow-up, proceed with the main analysis
    return {
        "follow_up": False,
        "conversation_history": conversation_history
    }


@claude.route('/analyze', methods=['POST'])
def analyze():
    """
    Analyzes user input, checks for follow-up context, and processes financial data.
    """
    try:
        data = request.get_json()
        user_question = data.get("question", "").strip()
        if not user_question:
            return jsonify({"error": "No question provided"}), 400

        # Check if the question is a follow-up
        memory_check = send_message_to_claude_with_memory(user_question)

        if memory_check.get("follow_up"):
            return jsonify({
                "response": memory_check["follow_up_analysis"],
                "conversation_history": memory_check["conversation_history"]
            })

        # Process the question as a standalone request (if not a follow-up)
        print("User question:", user_question)
        prompt = f"""
        Correlate the user's question with a stock ticker symbol.
        Give a one-word response with that ticker symbol in all capital letters.
        If there is no related stock ticker symbol, respond with 'Not-Here'.

        {user_question}
        """
        ticker = send_message_to_claude(prompt).upper().strip()
        print("Ticker:", ticker)

        if ticker == "NOT-HERE":
            return jsonify({
                "response": "No related stock ticker symbol found.",
                "ticker": ""
            })

        # Fetch financial data using yfinance
        try:
            stock = yf.Ticker(ticker)
            company_name = stock.info.get("shortName", "Unknown Company")
            current_price = stock.info.get("currentPrice", "N/A")
            market_cap = stock.info.get("marketCap", "N/A")
            pe_ratio = stock.info.get("trailingPE", "N/A")
            dividend_yield = stock.info.get("dividendYield", "N/A")
            summary = stock.info.get("longBusinessSummary", "No summary available.")

            # Fetch cash flow, income statement, and balance sheet details
            cash_flow_text = "\n".join(
                [f"{row['index']}: {', '.join(f'{k}: {v}' for k, v in row.items() if k != 'index')}" for row in stock.cashflow.reset_index().to_dict(orient="records")[:3]]
            ) if not stock.cashflow.empty else "No cash flow data available."

            income_statement_text = "\n".join(
                [f"{row['index']}: {', '.join(f'{k}: {v}' for k, v in row.items() if k != 'index')}" for row in stock.income_stmt.reset_index().to_dict(orient="records")[:3]]
            ) if not stock.income_stmt.empty else "No income statement data available."

            balance_sheet_text = "\n".join(
                [f"{row['index']}: {', '.join(f'{k}: {v}' for k, v in row.items() if k != 'index')}" for row in stock.balance_sheet.reset_index().to_dict(orient="records")[:3]]
            ) if not stock.balance_sheet.empty else "No balance sheet data available."

            # Prepare financial data prompt for Claude
            financial_data = f"""
            Company Name: {company_name}
            Current Price: {current_price}
            Market Cap: {market_cap}
            P/E Ratio: {pe_ratio}
            Dividend Yield: {dividend_yield}
            Summary: {summary}

            Cash Flow:
            {cash_flow_text}

            Income Statement:
            {income_statement_text}

            Balance Sheet:
            {balance_sheet_text}

            Okay, your job is to state the pros and cons of the company and give a brief summary of the company's financial health
            whilst stating statistics in number form given to you by the Yahoo Finance API - 25 words or less.
            Give me an investment recommendation based on the data provided in a range from 1 to 100, REMEBR THE SCORE IS THE LAST TO BE MENTOINED
            report the score like this score: 75
            """
        except Exception as data_error:
            return jsonify({"error": f"Failed to retrieve financial data: {data_error}"}), 500

        # Reflect on the financial data using Claude
        reflection_prompt = f"""
        Reflect on the financial health and performance of the company with the ticker symbol {ticker}.
        Use the following financial data for context:
        {financial_data}

        Provide a concise reflection, summarizing the company's financial strengths, weaknesses, and overall outlook.
        Limit the response to 3 sentences.
        """
        response = send_message_to_claude(reflection_prompt)
        last_two_words = response.split()[-1:]
        words = response.split()

# Remove the last two words
        response = ' '.join(words[:-2])
        
        print(last_two_words)
        # Add the response to the conversation history
        conversation_history.append({"question": user_question, "response": response})

        return jsonify({
            "response": response,
            "ticker": ticker,
            "conversation_history": conversation_history,
            "last_two_words": last_two_words
        })

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500
