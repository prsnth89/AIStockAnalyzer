"""Flask application - AI Stock Analyzer v2.0"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request, jsonify
from screener import generate_recommendations_by_category, generate_recommendations
from analyzer import analyze_ticker
from congress_tracker import get_congress_signals, get_top_congress_stocks

app = Flask(__name__, template_folder='../templates', static_folder='../static')

_cache = {}

def _get_recommendations():
    if 'recs' not in _cache:
        _cache['recs'] = generate_recommendations_by_category()
    return _cache['recs']


@app.route('/')
def home():
    categories = _get_recommendations()
    return render_template('index.html', categories=categories)


@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    ticker = request.form.get('ticker', '') or request.args.get('ticker', '')
    ticker = ticker.strip().upper()
    if not ticker:
        return render_template('error.html', error="Please enter a stock ticker symbol.")
    try:
        result = analyze_ticker(ticker)
        if not result:
            return render_template('error.html', error=f"Could not find data for '{ticker}'.")
        return render_template('result.html', data=result)
    except Exception as e:
        return render_template('error.html', error=f"Error analyzing {ticker}: {str(e)}")


@app.route('/api/recommendations')
def api_recommendations():
    return jsonify(_get_recommendations())


@app.route('/api/congress/<ticker>')
def api_congress(ticker):
    signals = get_congress_signals(ticker.upper())
    return jsonify(signals)


@app.route('/refresh')
def refresh():
    _cache.clear()
    return jsonify({'status': 'ok', 'message': 'Cache cleared'})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)
