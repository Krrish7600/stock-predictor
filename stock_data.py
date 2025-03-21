import yfinance as yf
import pandas as pd

def fetch_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        # Fetch 1 year of daily data
        data = stock.history(period="1y")
        if data.empty:
            return None
        return data['Close'].tolist()  # Return closing prices
    except Exception:
        return None