import yfinance as yf
from prefect import flow, task
from influx import get_influx_writer
from influxdb_client import Point, WritePrecision

influx_writer = get_influx_writer()

@task
def ingest_to_influx_db(datetime, price):
    point = (
        Point("stock-prices")
        .tag("symbol", "GLEN.L")
        .field("price", price)
        .time(datetime, WritePrecision.NS)
        )
    
    influx_writer.write(bucket="moo", org="Moo", record=point)
    print(f"Ingesting {price} at {datetime} to InfluxDB")

@task
def get_stock_price(symbol):
    try:
        data = yf.download(symbol, period='1d', interval="1m")
        datetime = data.index[-1]
        price = data['Close'].iloc[-1]
        return datetime, price
        
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")

@flow(name="ingest-stock-price")
def stock_ingress(symbol):
    datetime, price = get_stock_price(symbol)
    ingest_to_influx_db(datetime, price)
    

if __name__ == "__main__":
    stock_ingress.serve(name="ingest-stock-price", 
                        tags=["yahoo_finance"], 
                        parameters={"symbol": "GLEN.L"}, 
                        interval="60")