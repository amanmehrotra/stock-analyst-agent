from io import BytesIO

import yfinance as yf
import matplotlib.pyplot as plt
import pandas_ta as ta
from numpy.ma.core import append

from utils.ticker import tickers

class ChartService:
    def __init__(self, stock_name, trading_type):
        self.stock_name = stock_name
        self.ticker = tickers[stock_name]
        self.trading_type = trading_type

    def fetch_chart(self):
        period=""
        interval=""
        if self.trading_type == "Intraday":
            period = "5d"
            interval = "15m"
        elif self.trading_type == "Short-term":
            period="3mo"
            interval="1d"
        data = yf.download(self.ticker, period=period, interval=interval)
        #data = ticker.history(period="30d", interval="1d")
        # Step 2: Plot close price
        plt.figure(figsize=(10, 5))
        period_string = ""
        if period =="5d":
            period_string = "5 Days"
        elif period =="3mo":
            period_string = "3 Months"
        plt.plot(data.index, data['Close'], label='Close Price', color='blue')
        plt.title(f'{self.ticker} Close Price (Last {period_string})')
        plt.xlabel('Date')
        plt.ylabel('Price (INR)')
        plt.grid(True)
        plt.legend()

        # Step 3: Save the chart
        #chart_path = f'chart.png'
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plt.close()
        return data, buffer

    def calculate_technical_indicators(self, df):
        # Calculate indicators

        df["SMA_20"] = ta.sma(df["Close"][self.ticker], length=20)
        df["SMA_50"] = ta.sma(df["Close"][self.ticker], length=50)
        df["RSI"] = ta.rsi(df["Close"][self.ticker], length=14)
        macd = ta.macd(df["Close"][self.ticker])
        if macd is not None:
            df["MACD"] = macd["MACD_12_26_9"]
            df["MACD_signal"] = macd["MACDs_12_26_9"]
        bbands = ta.bbands(df["Close"][self.ticker], length=20)
        if bbands is not None:
            df["bollinger_hband"] = bbands["BBU_20_2.0"]
            df["bollinger_lband"] = bbands["BBL_20_2.0"]

        return df

    def get_indicators(self, df):
        latest_data = df.dropna().iloc[-1]
        # Print the latest data with all calculated indicators
        print(f"Latest Close Price: {round(latest_data['Close'].iloc[-1], 2)}")
        print(f"20-Day Moving Average: {round(latest_data['SMA_20'].iloc[-1], 2)}")
        print(f"50-Day Moving Average: {round(latest_data['SMA_50'].iloc[-1], 2)}")
        print(f"RSI (14): {round(latest_data['RSI'].iloc[-1], 2)}")
        print(f"MACD: {round(latest_data['MACD'].iloc[-1], 2)}")
        print(f"MACD Signal: {round(latest_data['MACD_signal'].iloc[-1], 2)}")
        print(f"Bollinger High Band: {round(latest_data['bollinger_hband'].iloc[-1], 2)}")
        print(f"Bollinger Low Band: {round(latest_data['bollinger_lband'].iloc[-1], 2)}")

        indicators = {
            "close_price": round(latest_data['Close'].iloc[-1], 2) if 'Close' in latest_data else None,
            "SMA_20": round(latest_data['SMA_20'].iloc[-1], 2) if 'SMA_20' in latest_data else None,
            "SMA_50": round(latest_data['SMA_50'].iloc[-1], 2) if 'SMA_50' in latest_data else None,
            "RSI": round(latest_data['RSI'].iloc[-1], 2) if 'RSI' in latest_data else None,
            "MACD": round(latest_data['MACD'].iloc[-1], 2) if 'MACD' in latest_data else None,
            "MACD_signal": round(latest_data['MACD_signal'].iloc[-1], 2) if 'MACD_signal' in latest_data else None,
            "bollinger_high_band": round(latest_data['bollinger_hband'].iloc[-1],
                                         2) if 'bollinger_hband' in latest_data else None,
            "bollinger_low_band": round(latest_data['bollinger_lband'].iloc[-1],
                                        2) if 'bollinger_lband' in latest_data else None
        }
        return indicators
