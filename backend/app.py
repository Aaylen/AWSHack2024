from flask import Flask
from routes.stocks import stocks
from routes.claude import claude
from routes.claude import claude
from flask_cors import CORS  # type: ignore

app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(stocks, url_prefix='/stocks')
app.register_blueprint(claude, url_prefix='/claude')


if __name__ == "__main__":
    app.run(debug=True)
