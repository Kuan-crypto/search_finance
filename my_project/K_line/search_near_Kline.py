import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
import io
import ccxt

exchange = ccxt.binance()


def fetch_to_near():
    symbol = "NEAR/USDT"
    timeframe = "1h"
    limit = 150

    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)

    df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "close", "high", "low", "volume"])

    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

    df.set_index("timestamp", inplace=True)

    df["10MA"] = df["close"].rolling(10).mean()
    df["30MA"] = df["close"].rolling(30).mean()
    df["60MA"] = df["close"].rolling(60).mean()
    df["120MA"] = df["close"].rolling(120).mean()

    fig, axlist = mpf.plot(df,
                           type="candle",
                           mav=[10, 30, 60, 120],
                           volume=True,
                           title="NEAR/USDT K-line",
                           style="binance",
                           returnfig=True
                           )

    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    plt.close(fig)

    latest = df.iloc[-1]
    price_text = (
        f"📊 NEAR/USDT 最新 1H 資訊：\n"
        f"開盤價：{latest['open']}\n"
        f"收盤價：{latest['close']}\n"
        f"最高價：{latest['high']}\n"
        f"最低價：{latest['low']}\n"
        f"成交量：{latest['volume']}"
    )

    return buf, price_text
