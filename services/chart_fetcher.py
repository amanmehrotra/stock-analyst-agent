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
        result = get_period_interval_string(self.trading_type)

        data = yf.download(self.ticker, period=result["period"], interval=result["interval"])
        #data = ticker.history(period="30d", interval="1d")
        # Step 2: Plot close price
        plt.figure(figsize=(10, 5))

        plt.plot(data.index, data['Close'], label='Close Price', color='blue')
        plt.title(f'{self.ticker} Close Price (Last {result["period_string"]})')
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
        indicators = get_active_indicators(self.trading_type)
        close = df["Close"][self.ticker]
        high = df["High"][self.ticker]
        low = df["Low"][self.ticker]
        volume = df["Volume"][self.ticker]

        if "EMA_20" in indicators:
            df["EMA_20"] = ta.ema(close, length=20)

        if "EMA_50" in indicators:
            df["EMA_50"] = ta.ema(close, length=50)

        df["SMA_20"] = ta.sma(df["Close"][self.ticker], length=20)
        df["SMA_50"] = ta.sma(df["Close"][self.ticker], length=50)

        if "RSI" in indicators:
            df["RSI"] = ta.rsi(close, length=14)

        if "MACD" in indicators:
            macd = ta.macd(df["Close"][self.ticker])
            if macd is not None:
                df["MACD"] = macd["MACD_12_26_9"]
                df["MACD_signal"] = macd["MACDs_12_26_9"]

        if "OBV" in indicators:
            df["OBV"] = ta.obv(close, volume)

        if "Bollinger" in indicators:
            bb = ta.bbands(close, length=20)

            if bb is not None:
                df["bollinger_hband"] = bb["BBU_20_2.0"]
                df["bollinger_lband"] = bb["BBL_20_2.0"]

        if "ADX" in indicators:
            adx = ta.adx(high=high, low=low, close=close)
            if adx is not None:
                df["ADX"] = adx["ADX_14"]

        if "CCI" in indicators:
            df["CCI"] = ta.cci(high=high, low=low, close=close, length=20)

        return df

    # def get_indicators(self, df):
    #     latest_data = df.dropna().iloc[-1]
    #     # Print the latest data with all calculated indicators
    #     print(f"Latest Close Price: {round(latest_data['Close'].iloc[-1], 2)}")
    #     print(f"20-Day Moving Average: {round(latest_data['SMA_20'].iloc[-1], 2)}")
    #     print(f"50-Day Moving Average: {round(latest_data['SMA_50'].iloc[-1], 2)}")
    #     print(f"RSI (14): {round(latest_data['RSI'].iloc[-1], 2)}")
    #     print(f"MACD: {round(latest_data['MACD'].iloc[-1], 2)}")
    #     print(f"MACD Signal: {round(latest_data['MACD_signal'].iloc[-1], 2)}")
    #     print(f"Bollinger High Band: {round(latest_data['bollinger_hband'].iloc[-1], 2)}")
    #     print(f"Bollinger Low Band: {round(latest_data['bollinger_lband'].iloc[-1], 2)}")
    #
    #     indicators = {
    #         "close_price": round(latest_data['Close'].iloc[-1], 2) if 'Close' in latest_data else None,
    #         "SMA_20": round(latest_data['SMA_20'].iloc[-1], 2) if 'SMA_20' in latest_data else None,
    #         "SMA_50": round(latest_data['SMA_50'].iloc[-1], 2) if 'SMA_50' in latest_data else None,
    #         "RSI": round(latest_data['RSI'].iloc[-1], 2) if 'RSI' in latest_data else None,
    #         "MACD": round(latest_data['MACD'].iloc[-1], 2) if 'MACD' in latest_data else None,
    #         "MACD_signal": round(latest_data['MACD_signal'].iloc[-1], 2) if 'MACD_signal' in latest_data else None,
    #         "bollinger_high_band": round(latest_data['bollinger_hband'].iloc[-1],
    #                                      2) if 'bollinger_hband' in latest_data else None,
    #         "bollinger_low_band": round(latest_data['bollinger_lband'].iloc[-1],
    #                                     2) if 'bollinger_lband' in latest_data else None
    #     }
    #     return indicators

    def get_indicators(self, df):
        latest = df.dropna().iloc[-1]

        def safe(name):
            return round(latest[name].iloc[-1], 2) if name in df.columns else None

        raw_indicators = {
            "close_price": safe("Close"),
            # "SMA_20": safe("SMA_20"),
            # "SMA_50": safe("SMA_50"),
            "EMA_20": safe("EMA_20"),
            "EMA_50": safe("EMA_50"),
            "RSI": safe("RSI"),
            "MACD": safe("MACD"),
            "MACD_signal": safe("MACD_signal"),
            "OBV": safe("OBV"),
            "bollinger_high_band": safe("bollinger_hband"),
            "bollinger_low_band": safe("bollinger_lband"),
            "ADX": safe("ADX"),
            "CCI": safe("CCI")
        }

        # Filter out indicators that are None
        indicators = {k: v for k, v in raw_indicators.items() if v is not None}

        return indicators

def get_period_interval_string(trading_type: str):
    mapping = {
        "Intraday":       {"period": "1d",  "interval": "5m",  "period_string": "1 Day"},
        "1-3 Days":       {"period": "5d",  "interval": "15m", "period_string": "5 Days"},
        "1-2 Weeks":      {"period": "14d", "interval": "30m", "period_string": "14 Days"},
        "2-4 Weeks":      {"period": "1mo", "interval": "1h",  "period_string": "1 Month"},
        "1-3 Months":     {"period": "3mo", "interval": "1d",  "period_string": "3 Months"},
        "3-6 Months":     {"period": "6mo", "interval": "1d",  "period_string": "6 Months"},
    }

    return mapping.get(trading_type, {"period": None, "interval": None, "period_string": "Unknown"})

def get_active_indicators(trading_type):
    # if trading_type == "Intraday":
    #     return ["EMA_20", "RSI", "OBV", "Bollinger"]
    # elif trading_type == "1-3 Days":
    #     return ["EMA_20", "EMA_50", "RSI", "OBV", "Bollinger", "MACD"]
    # elif trading_type in ["1-2 Weeks", "2-4 Weeks"]:
    #     return ["EMA_20", "EMA_50", "RSI", "MACD", "OBV", "Bollinger", "ADX"]
    # elif trading_type in ["1-3 Months", "3-6 Months"]:
    #     return ["EMA_20", "EMA_50", "RSI", "MACD", "OBV", "Bollinger", "ADX", "CCI"]
    # else:
    #     return ["EMA_20", "RSI"]
    return ["EMA_20", "EMA_50", "RSI", "MACD", "OBV", "Bollinger", "ADX", "CCI"]