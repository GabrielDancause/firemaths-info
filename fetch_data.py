import yfinance as yf
import json
import pandas as pd
import numpy as np

tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "BRK-B", "SPY"]
data = {}

for t in tickers:
    print(f"Fetching {t}...")
    stock = yf.Ticker(t)
    hist = stock.history(period="max", interval="1mo")
    hist = hist.dropna(subset=['Close'])
    # We need Close, Dividends.
    # To calculate total return with dividends reinvested, we need the raw Close and Dividends.
    # Wait, yfinance history gives "Close" which is adjusted for splits but not dividends,
    # OR it gives adjusted close?
    # By default, yfinance's `history` adjusts for both splits and dividends if auto_adjust=True.
    # If auto_adjust=False, it gives raw Open, High, Low, Close, Adj Close, Volume, Dividends, Stock Splits.
    hist_raw = stock.history(period="max", interval="1mo", auto_adjust=False)
    hist_raw = hist_raw.dropna(subset=['Close'])

    dates = [d.strftime('%Y-%m-%d') for d in hist_raw.index]
    close = [None if np.isnan(x) else round(x, 4) for x in hist_raw['Close']]
    adj_close = [None if np.isnan(x) else round(x, 4) for x in hist_raw['Adj Close']]
    dividends = [None if np.isnan(x) else round(x, 4) for x in hist_raw['Dividends']]

    data[t] = {
        "dates": dates,
        "close": close,
        "adj_close": adj_close,
        "dividends": dividends
    }

with open("stock_data.json", "w") as f:
    json.dump(data, f)
print("Done")
