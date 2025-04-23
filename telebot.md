import requests
from bs4 import BeautifulSoup as bs
import re

from telegram import Update
from telegram.ext import Application,CommandHandler,ContextTypes

TELEGRAM_TOKEN = "7671557996:AAFIrBJ9mNenIZiAJwjfr291POr4MSw6rYU"
CHAT_ID = "7658509784"

base_url = "https://www.coindesk.com"

keywords =["bitcoin","eth","ethereum","ada","near"]

def send_to_telegram(message):

    url =f"https://api.telegram.org/bot7671557996:AAFIrBJ9mNenIZiAJwjfr291POr4MSw6rYU/sendMessage"

    data = {
        "chat_id":CHAT_ID,
        "text":message,
        "parse_mode":"HTML"
    }

    response = requests.post (url,data=data)

    if response.status_code == 200:
        print("✅ 訊息已傳送到 Telegram")
    else:
        print(f"❌錯誤，狀態碼{response.status_code}")
        print(response.text)


def fetch_coindesk_article():
    markets_url =base_url + "/markets"
    headers ={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
    }
    response = requests.get(markets_url,headers=headers,timeout=20)

    soup = bs(response.text,"html.parser")

    articles = []
    if response.status_code == 200:
        for article in soup.find_all("a",class_="text-color-charcoal-900 mb-4 hover:underline"):
            href = article.get( "href")
            title_tag = article.find("h2")
            if not href or not title_tag:
                continue
            title = title_tag.get_text(strip=True)

            if any(re.search(keyword,title,re.IGNORECASE)for keyword in keywords):

                if not href.startswith("http"):
                    href = base_url + href
                articles.append((title,href))
        return articles

    else:
        print(f"❌抓取錯誤，狀態碼{response.status_code}")

async def get_new_handler(update:Update,context:ContextTypes.DEFAULT_TYPE):
    results = fetch_coindesk_article()
    if results:
        message = (f"📰<b> telegraph 熱門關鍵字文章:</b>\n\n")
        for title , link in results:
            message += f" 📌<b> {title}</b>\n 🔗{link}\n\n"
        await context.bot.send_message(chat_id=update.effective_chat.id,text=message,parse_mode = "HTML")
    else:
        await context.bot.send_message(chat_id = update.effective_chat.id,text = "沒有符合的文章")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("gettingNews",get_new_handler))

    print("🤖Telegram Bot 正在運作...")

    app.run_polling()

if __name__ == "__main__":
    main()
