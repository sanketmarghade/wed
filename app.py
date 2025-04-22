from flask import Flask, request, jsonify
from flask_cors import CORS
from tradingview_ta import TA_Handler, Interval

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

@app.route('/')
def home():
    return jsonify({"status": "API running", "version": "1.0"})

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        symbol = data.get("symbol", "").upper()
        interval_str = data.get("interval", "1d")
        exchange = data.get("exchange", "NSE")
        screener = data.get("screener", "india")

        if not symbol:
            return jsonify({"error": "Symbol is required"}), 400
        if interval_str not in interval_map:
            return jsonify({"error": f"Unsupported interval: {interval_str}"}), 400

        interval = interval_map[interval_str]

        handler = TA_Handler(
            symbol=symbol,
            screener=screener,
            exchange=exchange,
            interval=interval
        )

        analysis = handler.get_analysis()

        return jsonify({
            "symbol": symbol,
            "exchange": exchange,
            "screener": screener,
            "interval": interval_str,
            "summary": analysis.summary,
            "indicators": analysis.indicators,
            "oscillators": analysis.oscillators,
            "moving_averages": analysis.moving_averages,
            "time": analysis.time
        })

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
