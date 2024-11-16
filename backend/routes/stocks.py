from flask import Blueprint, jsonify, request
import yfinance as yf
import requests
from flask import Flask, jsonify
from datetime import datetime, timedelta

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
    if data['entry'] == '1day':
        today = datetime.now()
        yesterday = today - timedelta(days = 1)
        date_of_interest = yesterday.strftime('%Y-%m-%d')
        historical_data = stock.history(interval = "60m", start = date_of_interest, end = date_of_interest)
        filtered_data = historical_data.reset_index()
        filtered_data['Datetime'] = filtered_data['Datetime'].dt.tz_localize(None)
        filtered_data = filtered_data[filtered_data['Datetime'].dt.date == pd.to_datetime(date).date()]
        hours = filtered_data['Datetime'].dt.strftime('%H:%M:%S').tolist()
        opening_prices = filtered_data['Open'].tolist()
        closing_prices = filtered_data['Close'].tolist()
        high_prices = filtered_data['High'].tolist()
        low_prices = filtered_data['Low'].tolist()
    else:   
        historical_data = stock.history(period = entry)
        dates = historical_data.index.strftime('%Y-%m-%d').tolist()
        closing_prices = historical_data['Close'].tolist()                                    
        opening_prices = historical_data['Open'].tolist()   
        high_prices = historical_data['High'].tolist()   
        low_prices = historical_data['Low'].tolist()   
    
    return jsonify({
        "hours": hours,
        "dates": dates,
        "closing_prices": closing_prices,
        "opening_prices": opening_prices,
        "high_prices": high_prices,
        "low_prices": low_prices,
    })


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



