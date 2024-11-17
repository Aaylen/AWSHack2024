from flask import Blueprint, jsonify, request
from flask_cors import CORS
import yfinance as yf
from datetime import datetime

income = Blueprint('income', __name__)
CORS(income)  # Enable CORS for this blueprint

@income.route('/endpoint', methods=['POST'])
def post_endpoint():
    try:
        data = request.get_json()
        data = request.get_json()
        
        if not data or 'ticker' not in data:
            return jsonify({'error': 'Ticker is required'}), 400
            
        ticker = data['ticker']
        
        stock = yf.Ticker(ticker)
        income_statement = stock.income_stmt
        most_recent_quarter = income_statement.iloc[:, 0]
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
                    
        return jsonify({
            'ticker': ticker,
            'most_recent_quarter': {
                'date': most_recent_quarter.name.strftime('%Y-%m-%d'),
                'data': processed_dict
            }
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500