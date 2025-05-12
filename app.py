from flask import Flask, request, jsonify
from flask_cors import CORS
from tradingview-ta-v2 import TA_Handler, Interval

app = Flask(__name__)
CORS(app)

interval_map = {
    "1m": Interval.INTERVAL_1_MINUTE,
    "5m": Interval.INTERVAL_5_MINUTES,
    "15m": Interval.INTERVAL_15_MINUTES,
    "1h": Interval.INTERVAL_1_HOUR,
    "4h": Interval.INTERVAL_4_HOURS,
    "1d": Interval.INTERVAL_1_DAY,
    "1w": Interval.INTERVAL_1_WEEK,
    "1mo": Interval.INTERVAL_1_MONTH,
}

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        symbol = data.get("symbol", "").upper()
        interval_str = data.get("interval", "1d")
        interval = interval_map.get(interval_str, Interval.INTERVAL_1_DAY)

        print(f"Received symbol: {symbol}, interval: {interval_str}")

        if not symbol:
            return jsonify({"error": "Symbol is required"}), 400

        handler = TA_Handler(
            symbol=symbol,
            screener="india",
            exchange="NSE",
            interval=interval
        )

        analysis = handler.get_analysis()
        summary = analysis.summary

        return jsonify({
            "symbol": symbol,
            "interval": interval_str,
            "recommendation": summary.get('RECOMMENDATION', "Not Available"),
            "BUY": summary.get('BUY', 0),
            "NEUTRAL": summary.get('NEUTRAL', 0),
            "SELL": summary.get('SELL', 0),
            "indicators": analysis.indicators
        })

    except Exception as e:
        print(f"Error: {str(e)}")  # Log to server logs
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
