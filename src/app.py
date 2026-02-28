from flask import Flask, render_template, request
from analyzer import analyze_ticker

app = Flask(__name__, template_folder="../templates")

@app.route('/')
def home():
    """Landing page with ticker search."""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze ticker and show results."""
    ticker = request.form.get('ticker', '').upper().strip()
    
    # Basic validation
    if not ticker:
        return render_template('error.html', error="Please enter a ticker symbol.")
    
    try:
        result = analyze_ticker(ticker)
        return render_template('result.html', data=result)
    except ValueError as e:
        return render_template('error.html', error=str(e))
    except Exception as e:
        error_msg = f"Unable to fetch data for {ticker}. Please verify it's a valid US stock ticker (e.g., AAPL, MSFT, TSLA)."
        return render_template('error.html', error=error_msg)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
