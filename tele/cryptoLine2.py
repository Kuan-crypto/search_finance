import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
import ccxt
import io

from matplotlib.pyplot import ylabel
from telegram import Update, InputFile
from telegram.ext import Application,CommandHandler,ContextTypes

from tele.cryptoLine import exchange

TOKEN = '7671557996:AAFIrBJ9mNenIZiAJwjfr291POr4MSw6rYU'
URL = f'https://api.telegram.org/bot{TOKEN}/'
chat_id = "7658509784"

exchange = ccxt.binance()

def fetch_to_eth():
    ohlcv = exchange.fetch_ohlcv(symbol="ETH/USDT",timeframe="1h",limit=150)

    df = pd.DataFrame(ohlcv,columns=["timestamp","open","high","low","close","volume"])

    df["timestamp"] = pd.to_datetime(df["timestamp"],unit = "ms")

    df.set_index("timestamp",inplace=True)

    df["10MA"] = df["close"].rolling(10).mean()
    df["30MA"] = df["close"].rolling(30).mean()
    df["60MA"] = df["close"].rolling(60).mean()
    df["120MA"] = df["close"].rolling(120).mean()

    df["change_pct"] = df["close"].pct_change() * 100

    fig , axlist = mpf.plot(df,
                            type = "candle",
                            mav = [10,30,60,120],
                            volume = True,
                            style="yahoo",
                            title="ETH/USDT 1h K-line",
                            ylabel="price USDT",
                            ylabel_lower="volume",
                            returnfig = True
                            )

    buf = io.BytesIO()
    fig.savefig(buf,format="png")
    plt.close(fig)
    buf.seek(0)

    return buf

async def send_to_photo(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("正在等待Bot繪圖中...")

    img_buf = fetch_to_eth()

    await update.message.reply_photo(photo=InputFile(img_buf,filename="eth.chart.png"))

async def error_handler(update, context):
    print(f"發生錯誤：{context.error}")

def main():
    app =Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("eth_line",send_to_photo))

    print("Bot已啟動，等待指令中...")
    app.run_polling()


if __name__ == "__main__":
    main()

