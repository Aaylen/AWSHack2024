from flask import Blueprint, jsonify, request
import yfinance as yf
import requests



stocks = Blueprint('stocks', __name__)

@stocks.route('/endpoint', methods=['POST'])
def post_endpoint():
    data = request.get_json()
    if 'action' in data:
        if data['action'] == 'calculateAverage':
            calculateAverage(data)
        if data['action'] == 'bestDays':
            pass
        if data['action'] == 'displayStock':
            displayStock(data)


def displayStock(data):
    tickerSymbol = data['stock']
    stock = yf.Ticker(tickerSymbol)
    time_series = data['Time Series (Daily)']
    df = pd.DataFrame.from_dict(time_series, orient = 'index', dtype = float)
    df.index = pd.to_dateTime(df.index)
    df.sort_index(inplace = True)
    df = df[['4. close']].rename(columns = {'4. close': 'Close})'})

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



