from flask import Blueprint, jsonify, request
import yfinance as yf
from datetime import datetime


stocks = Blueprint('stocks', __name__)


@stocks.route('/analyze', methods=['POST'])
def analyze_request():
    """
    Flask endpoint to handle AI-specified stock analysis actions.
    """
    try:
        data = request.get_json()
        if 'action' not in data:
            return jsonify({'error': 'No action specified'}), 400


        action = data['action']
        if action == 'average_return':
            result = average_return(data)
        elif action == 'best_days':
            result = best_days(data)
        elif action == 'display_stock':
            result = display_stock(data)
        else:
            return jsonify({'error': f"Unknown action: {action}"}), 400


        # Format the response for better AI interaction
        response = {
            "action": action,
            "result": result
        }
        return jsonify(response), 200


    except KeyError as e:
        return jsonify({'error': f'Missing required field: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500




def display_stock(data):
    """
    Fetches stock data for the specified ticker and timeframe.
    """
    ticker_symbol = data.get('ticker', '').upper()
    entry = data.get('entry', '1mo')
   
    if not ticker_symbol:
        return {'error': 'Ticker symbol is required'}
   
    stock = yf.Ticker(ticker_symbol)


    # Get key metrics (P/E, Market Cap)
    key_metrics = {
        'pe': stock.info.get('trailingPE', 'N/A'),
        'marketCap': stock.info.get('marketCap', 'N/A'),
    }


    # Get historical data based on the timeframe
    try:
        if entry == '5d':
            historical_data = stock.history(period="5d")
        elif entry == 'ytd':
            today = datetime.now()
            start_date = datetime(today.year, 1, 1)
            historical_data = stock.history(start=start_date)
        else:
            historical_data = stock.history(period=entry)


        # Parse historical data
        dates = historical_data.index.strftime('%Y-%m-%d').tolist()
        closing_prices = historical_data['Close'].tolist()
        opening_prices = historical_data['Open'].tolist()
        high_prices = historical_data['High'].tolist()
        low_prices = historical_data['Low'].tolist()


        return {
            "dates": dates,
            "closing_prices": closing_prices,
            "opening_prices": opening_prices,
            "high_prices": high_prices,
            "low_prices": low_prices,
            "key_metrics": key_metrics
        }
    except Exception as e:
        return {'error': f"Failed to retrieve data for {ticker_symbol}: {e}"}




def average_return(data):
    """
    Calculates the average percentage return for a stock over a date range.
    """
    ticker_symbol = data.get('stock', '').upper()
    start_date = data.get('start_date')
    end_date = data.get('end_date')
   
    if not ticker_symbol or not start_date or not end_date:
        return {'error': 'Stock symbol, start_date, and end_date are required'}


    try:
        stock = yf.Ticker(ticker_symbol)
        historical_data = stock.history(start=start_date, end=end_date)


        # Calculate the average percentage return
        historical_data['Pct Change'] = historical_data['Close'].pct_change() * 100
        avg_return = historical_data['Pct Change'].mean()
        return {"average_return": avg_return}
    except Exception as e:
        return {'error': f"Failed to calculate average return: {e}"}




def best_days(data):
    """
    Finds the best trading days for a stock based on the highest percentage gains.
    """
    ticker_symbol = data.get('stock', '').upper()
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    days = int(data.get('days', 5))


    if not ticker_symbol or not start_date or not end_date:
        return {'error': 'Stock symbol, start_date, and end_date are required'}


    try:
        stock = yf.Ticker(ticker_symbol)
        historical_data = stock.history(start=start_date, end=end_date)


        # Calculate daily percentage changes
        historical_data['Pct Change'] = historical_data['Close'].pct_change() * 100


        # Add a column for the previous day's close
        historical_data['Previous Close'] = historical_data['Close'].shift(1)


        # Sort by percentage change
        sorted_data = historical_data.sort_values(by='Pct Change', ascending=False).head(days)


        # Prepare result
        result = [
            {
                "date": date.strftime('%Y-%m-%d'),
                "previous_close": row['Previous Close'],
                "close": row['Close'],
                "percentage_gain": row['Pct Change']
            }
            for date, row in sorted_data.iterrows()
        ]
        return result
    except Exception as e:
        return {'error': f"Failed to calculate best days: {e}"}
