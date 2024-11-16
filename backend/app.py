from flask import Flask
from backend.routes.stocks import server1
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(server1, url_prefix='/stocks')


if __name__ == "__main__":
    app.run(debug=True)
