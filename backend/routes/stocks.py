from flask import Blueprint, jsonify, request
import yfinance as yf

stocks = Blueprint('stocks', __name__)

@stocks.route('/endpoint', methods=['POST'])
def post_endpoint():
    data = request.get_json()
    if 'action' in data:
        if data['action'] == 'calculateAverage':
            calculateAverage(data)
        if data['action'] == 'bestDays':
            pass
    
    return jsonify(data) 

def calculateAverage(data):
    tickerSymbol = data['stock']
    stock = yf.Ticker(tickerSymbol)
    startDate = data['startDate']
    endDate = data['endDate']
    historical_data = stock.history(start=startDate, end=endDate)
    average = historical_data['Close'].mean()
    return average

def bestDays(data):
    startDate = data['startDate']
    endDate = data['endDate']
    tickerSymbol = data['stock']
    days = data['days']
    stock = yf.Ticker(tickerSymbol)
    historical_data = stock.history(start=startDate, end=endDate)
    sorted_data = historical_data.sort_values(by='Close', ascending=False)
    top_days = sorted_data.head(days).index.strftime('%Y-%m-%d').tolist()
    return top_days
    stock = yf.Ticker(tickerSymbol)
    historical_data = stock.history(start=startDate, end=endDate)



