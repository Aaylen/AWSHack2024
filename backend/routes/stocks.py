from flask import Blueprint, jsonify, request
from flask_cors import CORS
import yfinance as yf
from datetime import datetime

stocks = Blueprint('stocks', __name__)
CORS(stocks)  # Enable CORS for this blueprint

@stocks.route('/endpoint', methods=['POST'])
def post_endpoint():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        if 'action' not in data:
            return jsonify({'error': 'No action specified'}), 400

        if data['action'] == 'display_stock':
            return display_stock(data)
        elif data['action'] == 'average_return':
            return jsonify({'average_return': average_return(data)}), 200
        elif data['action'] == 'best_days':
            return jsonify({'best_days': best_days(data)}), 200
        elif data['action'] == 'balanceSheets':
            return jsonify({'balanceSheets': balanceSheets(data)}), 200
        else:
            return jsonify({'error': 'Invalid action specified'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def display_stock(data):
    try:
        if 'ticker' not in data or 'entry' not in data:
            return jsonify({'error': 'Missing ticker or entry parameter'}), 400

        ticker_symbol = data['ticker']
        entry = data['entry']
        
        stock = yf.Ticker(ticker_symbol)
        
        # Get historical data based on the timeframe
        if entry == 'ytd':
            start_date = datetime(datetime.now().year, 1, 1)
            historical_data = stock.history(start=start_date)
        elif entry in ['1d', '5d']:
            # Use 5m intervals for 1d and 60m for 5d
            interval = '5m' if entry == '1d' else '60m'
            historical_data = stock.history(period=entry, interval=interval)
        else:
            historical_data = stock.history(period=entry)

        # Format dates based on timeframe
        if entry == '1d':
            date_format = '%H:%M'  # Just show hours and minutes for 1d
        elif entry == '5d':
            date_format = '%m/%d %H:%M'  # Show date and time for 5d
        else:
            date_format = '%Y-%m-%d'  # Regular date format for other periods

        # Format the response data
        response_data = {
            "dates": historical_data.index.strftime(date_format).tolist(),
            "closing_prices": historical_data['Close'].tolist(),
            "opening_prices": historical_data['Open'].tolist(),
            "high_prices": historical_data['High'].tolist(),
            "low_prices": historical_data['Low'].tolist(),
            "key_metrics": {
                'pe': format_metric(stock.info.get('trailingPE')),
                'marketCap': format_metric(stock.info.get('marketCap')),
                '52WeekHigh': format_metric(stock.info.get('fiftyTwoWeekHigh')),
                '52WeekLow': format_metric(stock.info.get('fiftyTwoWeekLow')),
                'beta': format_metric(stock.info.get('beta')),
                'forwardPE': format_metric(stock.info.get('forwardPE')),
                'priceToSales': format_metric(stock.info.get('priceToSalesTrailing12Months')),
                'priceToBook': format_metric(stock.info.get('priceToBook')),
                'dividendYield': format_metric(stock.info.get('dividendYield'))
            }
        }
        
        return jsonify({'chart': response_data}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def format_metric(value):
    """Formats values to the style guideline (in billions and minimal decimal places)."""
    if value == 'N/A' or value is None:
        return 'N/A'
    if isinstance(value, (int, float)):
        if value >= 1e9:
            return f"${value / 1e9:.2f}B"
        return f"{value:.2f}"
    return value


def average_return(data):
    tickerSymbol = data['stock']
    start_date = data['start_date']
    end_date = data['end_date']
    
    # Get stock data for the given ticker and date range
    stock = yf.Ticker(tickerSymbol)
    historical_data = stock.history(start=start_date, end=end_date)
    
    # Calculate the average percentage return
    historical_data['Pct Change'] = historical_data['Close'].pct_change() * 100
    avg_return = historical_data['Pct Change'].mean()
    
    return float(avg_return)

def best_days(data):
    start_date = data['start_date']
    end_date = data['end_date']
    tickerSymbol = data['stock']
    days = int(data['days'])
    
    # Get stock data for the given ticker and date range
    stock = yf.Ticker(tickerSymbol)
    historical_data = stock.history(start=start_date, end=end_date)
    
    # Calculate the daily percentage change in closing price
    historical_data['Pct Change'] = historical_data['Close'].pct_change() * 100
    
    # Add a column for the previous day's close
    historical_data['Previous Close'] = historical_data['Close'].shift(1)
    
    # Sort the data by the percentage change in descending order
    sorted_data = historical_data.sort_values(by='Pct Change', ascending=False)
    
    # Get the top 'days' number of rows (days with the highest percentage gains)
    top_days = sorted_data.head(days)
    
    # Create a list of tuples with date, previous close, close, and percentage gain
    result = [
        (date.strftime('%Y-%m-%d'), row['Previous Close'], row['Close'], row['Pct Change']) 
        for date, row in top_days.iterrows()
    ]
    
    return result


def balanceSheets(data):
    ticker_symbol = data['ticker']
    stock = yf.Ticker(ticker_symbol)
    balance_sheet = stock.balance_sheet