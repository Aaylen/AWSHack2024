from flask import Blueprint, jsonify, request

server1 = Blueprint('server1', __name__)

@server1.route('/endpoint', methods=['POST'])
def post_endpoint():
    data = request.get_json()
    name = data.get('name', 'Unkonwn')
    return jsonify({"message": f"Hello {name}"})