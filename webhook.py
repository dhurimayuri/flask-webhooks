from flask import Flask, request, jsonify

app = Flask(__name__)

# Store the latest traded prices for different tokens
latest_prices = {}

# Store alerts for multiple tokens
alerts = {}

@app.route("/")
def home():
    """Check if API is running."""
    return jsonify({"message": "Flask TradingView Webhook is running!"})

@app.route("/webhook", methods=["POST"])
def tradingview_webhook():
    """Receives webhook alerts from TradingView and processes them."""
    data = request.json
    if not data:
        return jsonify({"error": "Invalid data"}), 400

    action = data.get("action")
    price = data.get("price")
    token = data.get("token")

    if action and price and token:
        print(f"✅ Webhook Received: {data}")
        latest_prices[token] = price  # Update latest price dynamically
        return jsonify({"status": "success", "message": f"Order received: {action} at {price} for token {token}"}), 200
    else:
        return jsonify({"error": "Missing required fields (action, price, token)"}), 400

@app.route("/ltp/<token>", methods=["GET"])
def get_ltp(token):
    """Returns the latest traded price for a given token."""
    if token in latest_prices:
        return jsonify({"token": token, "last_traded_price": latest_prices[token]})
    else:
        return jsonify({"error": f"No data available for token {token}"}), 404

@app.route("/set_alert", methods=["POST"])
def set_alert():
    """Sets a price alert for a given token."""
    data = request.json
    token = data.get("token")
    alert_price = data.get("alert_price")

    if token and alert_price:
        if token not in alerts:
            alerts[token] = []
        alerts[token].append(alert_price)

        print(f"🔔 Alert set for token {token} at {alert_price}")
        return jsonify({"message": f"Alert set for token {token} at {alert_price}"}), 200
    else:
        return jsonify({"error": "Missing required fields (token, alert_price)"}), 400

@app.route("/alerts/<token>", methods=["GET"])
def get_alerts(token):
    """Returns the alerts for a given token."""
    if token in alerts:
        return jsonify({"token": token, "alerts": alerts[token]})
    else:
        return jsonify({"message": f"No alerts set for token {token}"}), 404

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
