from flask import Blueprint, jsonify, request
from flask_cors import CORS
import yfinance as yf
from datetime import datetime

cashflow = Blueprint('cashflow', __name__)
CORS(cashflow)  # Enable CORS for this blueprint

@cashflow.route('/endpoint', methods=['POST'])
def post_endpoint():
    print("cashflow endpoint")
    try:
        data = request.get_json()
        
        if not data or 'ticker' not in data:
            return jsonify({'error': 'Ticker is required'}), 400
            
        ticker = data['ticker']
        
        stock = yf.Ticker(ticker)
        cash_flow_statement = stock.cashflow  # Use the cash flow statement
        most_recent_quarter = cash_flow_statement.iloc[:, 0]
        quarter_dict = most_recent_quarter.to_dict()
        
        # Handle data types for JSON serialization
        processed_dict = {}
        for key, value in quarter_dict.items():
            if isinstance(value, datetime):
                processed_dict[key] = value.strftime('%Y-%m-%d')
            # Handle numpy numbers
            elif hasattr(value, 'item'):
                processed_dict[key] = value.item()
            else:
                processed_dict[key] = value
        print(most_recent_quarter.name.strftime('%Y-%m-%d'), processed_dict)  
        return jsonify({
            'ticker': ticker,
            'most_recent_quarter': {
                'date': most_recent_quarter.name.strftime('%Y-%m-%d'),
                'data': processed_dict
            }
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
