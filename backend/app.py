from flask import Flask
from routes.stocks import stocks
from routes.claude import claude
from routes.income import income
from routes.cashflow import cashflow
from flask_cors import CORS  # type: ignore

app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(stocks, url_prefix='/stocks')
app.register_blueprint(claude, url_prefix='/claude')
app.register_blueprint(income, url_prefix='/income')
app.register_blueprint(cashflow, url_prefix='/cashflow')


if __name__ == "__main__":
    app.run(debug=True)
