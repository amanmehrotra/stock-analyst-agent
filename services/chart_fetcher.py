from io import BytesIO

import yfinance as yf
import matplotlib.pyplot as plt
# import pandas_ta as ta
from ta.momentum import RSIIndicator
from ta.trend import MACD, EMAIndicator
from ta.volatility import AverageTrueRange
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

        data = yf.download(self.ticker, period=result["period"], interval=result["interval"], progress=False)
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

        # VWAP
        if "VWAP" in indicators:
            df['vwap'] = (close * volume).cumsum() / volume.cumsum()

        if "EMA_20" in indicators:
            df["EMA_20"] = EMAIndicator(close, window=20).ema_indicator()

        if "EMA_50" in indicators:
            df["EMA_50"] = EMAIndicator(close, window=50).ema_indicator()

        # df["SMA_20"] = ta.sma(df["Close"][self.ticker], length=20)
        # df["SMA_50"] = ta.sma(df["Close"][self.ticker], length=50)

        if "RSI" in indicators:
            df["RSI"] = RSIIndicator(close, window=14).rsi()

        if "MACD" in indicators:
            macd = MACD(df["Close"][self.ticker])
            if macd is not None:
                df["MACD"] = macd.macd()
                df["MACD_signal"] = macd.macd_signal()

        # if "OBV" in indicators:
        #     df["OBV"] = ta.obv(close, volume)

        # if "Bollinger" in indicators:
        #     bb = ta.bbands(close, length=20)
        #
        #     if bb is not None:
        #         df["bollinger_hband"] = bb["BBU_20_2.0"]
        #         df["bollinger_lband"] = bb["BBL_20_2.0"]

        # if "ADX" in indicators:
        #     adx = ta.adx(high=high, low=low, close=close)
        #     if adx is not None:
        #         df["ADX"] = adx["ADX_14"]

        # if "CCI" in indicators:
        #     df["CCI"] = ta.cci(high=high, low=low, close=close, length=20)

        if "ATR" in indicators:
            df["ATR"] = AverageTrueRange(high=high, low=low, close=close, window=14).average_true_range()

        avg_vol = volume.rolling(window=20).mean()
        df['volume_avg'] = avg_vol
        df["vol_surge"] = volume > 1.5 * avg_vol

        # Recent swing high/low (use last N bars)
        if "swing_high_30" in indicators:
            df["swing_high_30"] = high.rolling(window=30).max()
            df["swing_low_30"] = low.rolling(window=30).min()

        if "swing_high_50" in indicators:
            df["swing_high_50"] = high.rolling(window=50).max()
            df["swing_low_50"] = low.rolling(window=50).min()

        if "swing_high_60" in indicators:
            df["swing_high_60"] = high.rolling(window=60).max()
            df["swing_low_60"] = low.rolling(window=60).min()

        if "swing_high_75" in indicators:
            df["swing_high_75"] = high.rolling(window=75).max()
            df["swing_low_75"] = low.rolling(window=75).min()

        if "swing_high_90" in indicators:
            df["swing_high_90"] = high.rolling(window=90).max()
            df["swing_low_90"] = low.rolling(window=90).min()

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
        previous = df.dropna().iloc[-2]


        def safe(name):
            return round(latest[name].iloc[-1], 2) if name in df.columns else None

        raw_indicators = {
            "time": latest.name.strftime('%H:%M'),
            "vwap": safe("vwap"),
            "close_price": safe("Close"),
            # "SMA_20": safe("SMA_20"),
            # "SMA_50": safe("SMA_50"),
            "EMA_20": safe("EMA_20"),
            "EMA_50": safe("EMA_50"),
            "RSI": safe("RSI"),
            "MACD": safe("MACD"),
            "MACD_signal": safe("MACD_signal"),
            # "OBV": safe("OBV"),
            # "bollinger_high_band": safe("bollinger_hband"),
            # "bollinger_low_band": safe("bollinger_lband"),
            # "ADX": safe("ADX"),
            # "CCI": safe("CCI"),
            "ATR": safe("ATR"),
            "vol_surge": int(latest["vol_surge"].iloc[-1]) if latest["vol_surge"].iloc[-1] is not None else None,  # Boolean, convert to 1 or 0 if needed
            "swing_high_30": safe("swing_high_30"),
            "swing_low_30": safe("swing_low_30"),
            "volume": int(latest['Volume'].iloc[-1]),
            "candle_high": round(previous['High'].iloc[-1], 2),
            "candle_low": round(previous['Low'].iloc[-1], 2),
            # "swing_high_60": safe("swing_high_60"),
            # "swing_low_60": safe("swing_low_60"),
            # "swing_high_50": safe("swing_high_50"),
            # "swing_low_50": safe("swing_low_50"),
            # "swing_high_75": safe("swing_high_75"),
            # "swing_low_75": safe("swing_low_75"),
            # "swing_high_90": safe("swing_high_90"),
            # "swing_low_90": safe("swing_low_90")
        }

        # Filter out indicators that are None
        indicators = {k: v for k, v in raw_indicators.items() if v is not None}
        print(indicators)
        return indicators

def get_period_interval_string(trading_type: str):
    mapping = {
        "Intraday":       {"period": "1d",  "interval": "1m",  "period_string": "1 Day"},
        "1-3 Days":       {"period": "7d",  "interval": "15m", "period_string": "7 Days"},
        "1-2 Weeks":      {"period": "14d", "interval": "30m", "period_string": "14 Days"},
        "2-4 Weeks":      {"period": "1mo", "interval": "1h",  "period_string": "1 Month"},
        "1-3 Months":     {"period": "3mo", "interval": "1d",  "period_string": "3 Months"},
        "3-6 Months":     {"period": "6mo", "interval": "1d",  "period_string": "6 Months"},
    }

    return mapping.get(trading_type, {"period": None, "interval": None, "period_string": "Unknown"})

def get_active_indicators(trading_type):
    base = ["RSI", "MACD", "ATR", "vol_surge", "EMA_20", "EMA_50", "VWAP"]

    if trading_type == "Intraday":
        return base + [ "swing_high_30", "swing_low_30"] # exclude EMA_50, MACD, ADX, CCI — not reliable at 5m

    elif trading_type == "1-3 Days":
        return base + ["EMA_20", "EMA_50", "MACD"] + ["swing_high_30", "swing_low_30"]  # avoid ADX, CCI due to short horizon

    elif trading_type == "1-2 Weeks":
        return base + ["EMA_20", "EMA_50", "MACD", "ADX", "ATR"] + ["swing_high_50", "swing_low_50"]

    elif trading_type == "2-4 Weeks":
        return base + ["EMA_20", "EMA_50", "MACD", "ADX", "ATR"] + ["swing_high_75", "swing_low_75"]

    elif trading_type == "1-3 Months":
        return base + ["EMA_20", "EMA_50", "MACD", "ADX", "CCI", "ATR"] + ["swing_high_60", "swing_low_60"]

    elif trading_type == "3-6 Months":
        return base + ["EMA_20", "EMA_50", "MACD", "ADX", "CCI", "ATR"] + ["swing_high_90", "swing_low_90"]

    else:
        return base
    # return ["EMA_20", "EMA_50", "RSI", "MACD", "OBV", "Bollinger", "ADX", "CCI"]