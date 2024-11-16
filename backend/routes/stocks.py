from flask import Blueprint, jsonify, request

stocks = Blueprint('stocks', __name__)

@stocks.route('/endpoint', methods=['POST'])
def post_endpoint():
    
    return jsonify()