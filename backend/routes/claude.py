from flask import Blueprint, jsonify, request
import requests


claude = Blueprint('claude', __name__)

@claude.route('/endpoint', methods=['POST'])
def post_endpoint():
    data = request.get_json()
    test = {
        'prompt': data['prompt'],
        'action': data['action'],
        'start_date': data['start_date'],
        'end_date': data['end_date'],
        'stock': data['stock'],
        'days': data['days']
    }
    stocks_response = requests.post('http://localhost:5000/stocks/endpoint', json=test)
    return stocks_response.json(), 200


    