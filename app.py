from flask import Flask
from flask_cors import CORS

from api.portfolio import portfolio_bp
from api.translate import translate_bp
from api.currency import currency_bp

app = Flask(__name__)
CORS(app)

# Register Blueprints
app.register_blueprint(portfolio_bp, url_prefix='/api/portfolio')
app.register_blueprint(translate_bp, url_prefix='/api/translate')
app.register_blueprint(currency_bp, url_prefix='/api/currency')

if __name__ == '__main__':
    app.run(debug=True)
