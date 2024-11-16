from flask import Flask
from routes.stocks import stocks
from routes.news import news
from flask_cors import CORS  # type: ignore

app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(stocks, url_prefix='/stocks')
app.register_blueprint(news, url_prefix='/news')

if __name__ == "__main__":
    app.run(debug=True)
