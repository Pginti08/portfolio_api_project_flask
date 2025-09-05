from flask import Blueprint, request, jsonify

currency_bp = Blueprint('currency', __name__)

conversion_rates = {
    "IN": 80.0,     # Indian Rupee
    "US": 1.0,      # US Dollar
    "FR": 0.92,     # Euro (France)
    "ES": 0.92,     # Euro (Spain)
    "DE": 0.92,     # Euro (Germany)
    "JP": 140.0,    # Japanese Yen
    "GB": 0.81,     # British Pound (UK)
    "CN": 7.3,      # Chinese Yuan
    "CA": 1.35,     # Canadian Dollar
    "AU": 1.5,      # Australian Dollar
    "BR": 5.15,     # Brazilian Real
    "RU": 78.0,     # Russian Ruble
    "MX": 18.6,     # Mexican Peso
    "ZA": 18.5,     # South African Rand
    "KR": 1300.0,   # South Korean Won
    # Add more as needed
}

currency_codes = {
    "IN": "INR",
    "US": "USD",
    "FR": "EUR",
    "ES": "EUR",
    "DE": "EUR",
    "JP": "JPY",
    "GB": "GBP",
    "CN": "CNY",
    "CA": "CAD",
    "AU": "AUD",
    "BR": "BRL",
    "RU": "RUB",
    "MX": "MXN",
    "ZA": "ZAR",
    "KR": "KRW",
    # Add more as needed
}


@currency_bp.route('/', methods=['GET'])
def convert_price():
    try:
        price = float(request.args.get('price'))
        from_country = request.args.get('from_country', 'US').upper()
        to_country = request.args.get('to_country', 'US').upper()
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid or missing price parameter"}), 400

    from_rate = conversion_rates.get(from_country, None)
    to_rate = conversion_rates.get(to_country, None)

    if from_rate is None or to_rate is None:
        return jsonify({"error": "Unsupported country code"}), 400

    # Convert input price to USD
    price_usd = price / from_rate
    # Convert USD price to target currency
    converted_price = price_usd * to_rate

    return jsonify({
        "input_price": price,
        "input_currency": currency_codes.get(from_country, "USD"),
        "converted_price": round(converted_price, 2),
        "converted_currency": currency_codes.get(to_country, "USD")
    })
