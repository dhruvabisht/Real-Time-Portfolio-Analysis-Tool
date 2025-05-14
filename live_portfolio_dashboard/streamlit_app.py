import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from alpaca_trade_api.rest import REST, TimeFrame
import datetime

# Load secrets
API_KEY = st.secrets["ALPACA_API_KEY"]
SECRET_KEY = st.secrets["ALPACA_SECRET_KEY"]
BASE_URL = "https://paper-api.alpaca.markets/v2"

# Initialize Alpaca API
api = REST(API_KEY, SECRET_KEY, BASE_URL)

st.title("Live Market Data Dashboard")
st.markdown("This app fetches real-time stock/ETF data using Alpaca API.")

# Ticker input
symbols = st.multiselect("Choose Tickers", ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA", "SPY", "QQQ"], default=["AAPL", "SPY"])

# Fetch and display data
for symbol in symbols:
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=5)

    # 🛠️ Format datetime to RFC3339 string format
    start = start_date.strftime('%Y-%m-%dT%H:%M:%SZ')
    end = end_date.strftime('%Y-%m-%dT%H:%M:%SZ')

    try:
        df = api.get_bars(symbol, TimeFrame.Hour, start=start, end=end, feed='iex').df
        df.index = pd.to_datetime(df.index)
        st.subheader(f" {symbol} – Last 5 Days (Hourly)")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=df['close'], mode='lines', name='Close Price'))
        fig.update_layout(title=f"{symbol} Price", xaxis_title="Time", yaxis_title="Price (USD)", height=400)
        st.plotly_chart(fig)
    except Exception as e:
        st.error(f"Error fetching data for {symbol}: {e}")

        
# Footer
st.markdown("---")
st.markdown("<p style='text-align: center;'>© Dhruva Bisht 2025</p>", unsafe_allow_html=True)

