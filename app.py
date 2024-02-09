import streamlit as st
import os
import pandas as pd
import numpy as np
from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS
import matplotlib.pyplot as plt
from dotenv import load_dotenv
load_dotenv()

url = "http://localhost:8086"
token = os.environ.get("INFLUXDB_TOKEN")
org = "Moo"
bucket = "moo"

def get_data():
    client = InfluxDBClient(url=url, token=token, org=org)
    query = f'''
        from(bucket: "{bucket}")
            |> range(start: -1h)
            |> filter(fn: (r) => r._measurement == "stock-prices")
            |> filter(fn: (r) => r._field == "price")
            |> filter(fn: (r) => r.symbol == "GLEN.L")
    '''
    tables = client.query_api().query(query, org=org)
    return tables[0].records

def main():
    st.title("My Lovely Stock Prices")
    st.write("These are my lovely stock prices!")
    
    data = get_data()
    prices = [[float(record.get_value())] for record in data]

    fig, ax = plt.subplots()
    ax.plot(pd.DataFrame(prices, columns=["Price"]))
    
    st.pyplot(fig)

if __name__ == "__main__":
    main()