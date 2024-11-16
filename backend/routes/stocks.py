from flask import Blueprint, jsonify, request
import yfinance as yf
from datetime import datetime

stocks = Blueprint('stocks', __name__)

@stocks.route('/endpoint', methods=['POST'])
def post_endpoint():
    try:
        data = request.get_json()
        response = {}
        
        if 'action' not in data:
            return jsonify({'error': 'No action specified'}), 400
    
        if data['action'] == 'average_return':
            response['average_return'] = average_return(data)

        elif data['action'] == 'best_days':
            response['best_days'] = best_days(data)

        elif data['action'] == 'display_stock':
            response['chart'] = display_stock(data)
            
        return jsonify(response), 200
        
    except KeyError as e:
        return jsonify({'error': f'Missing required field: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

        


def display_stock(data):
    tickerSymbol = data['ticker']
    stock = yf.Ticker(tickerSymbol)
    entry = data['entry']

    # Get key metrics (P/E, Market Cap)
    key_metrics = {
        'pe': stock.info.get('trailingPE', 'N/A'),
        'marketCap': stock.info.get('marketCap', 'N/A'),
    }

    # Get historical data based on the timeframe
    if entry == '5d':
        historical_data = stock.history(period="5d")
    elif entry == 'ytd':
        today = datetime.now()
        start_date = datetime(today.year, 1, 1)
        historical_data = stock.history(start=start_date)
    else:
        historical_data = stock.history(period=entry)

    dates = historical_data.index.strftime('%Y-%m-%d').tolist()
    closing_prices = historical_data['Close'].tolist()
    opening_prices = historical_data['Open'].tolist()
    high_prices = historical_data['High'].tolist()
    low_prices = historical_data['Low'].tolist()

    return jsonify({
        "dates": dates,
        "closing_prices": closing_prices,
        "opening_prices": opening_prices,
        "high_prices": high_prices,
        "low_prices": low_prices,
        "key_metrics": key_metrics, 
    })


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