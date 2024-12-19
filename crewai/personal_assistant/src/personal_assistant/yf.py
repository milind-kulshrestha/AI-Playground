import yfinance as yf

def get_latest_price(ticker):
    stock = yf.Ticker(ticker)
    latest_price = stock.history(period="1d")['Close'].iloc[-1]
    return latest_price

# Example usage
ticker_symbol = "AAPL"  # Replace with your desired ticker symbol
latest_price = get_latest_price(ticker_symbol)
print(f"The latest price for {ticker_symbol} is: ${latest_price:.2f}")