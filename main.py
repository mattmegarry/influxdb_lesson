import pprint
import yfinance as yf

def get_stock_price(symbol):
    try:
        data = yf.download(symbol, period='1d', interval="1m")
        datetime = data.index[-1]
        price = data['Close'].iloc[-1]
        return datetime, price
        
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")

print(get_stock_price("GLEN.L"))