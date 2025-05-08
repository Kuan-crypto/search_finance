from http.client import responses

import requests
from bs4 import BeautifulSoup as bs
import re

from telegram import Update
from telegram.ext import Application,CommandHandler,ContextTypes

TOKEN = '7671557996:AAFIrBJ9mNenIZiAJwjfr291POr4MSw6rYU'
URL = f'https://api.telegram.org/bot{TOKEN}/'
chat_id = "7658509784"

base_url = "https://abmedia.io/"

keywords = {
    "比特幣",
    "以太坊",
    "ada",
    "eth",
    "bitcoin",
    "near"
}
#成功
def fetch_to_telegram(message):
    url = f"https://api.telegram.org/bot7671557996:AAFIrBJ9mNenIZiAJwjfr291POr4MSw6rYU/sendMessage"

    data = {
        "chat_id":chat_id,
        "text":message,
        "parse_mode":"HTML"
    }

    response = requests.post(url,data=data)

    if response.status_code ==200:
        print("連接Telegram成功")
    else:
        print(f"連接Telegram失敗，狀態碼{response.status_code}")

def search_to_abmedia(pages=4):
    headers ={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
    }

    articles = []

    for page in range(1,pages+1):
        url = f"https://abmedia.io/blog/page/{page}"

        response = requests.get(url,headers=headers,timeout=10)

        soup = bs(response.text,"html.parser")



        if response.status_code ==200:

            for article in soup.find_all("article"):
                title_tag = article.find("h3",class_=True)
                link_tag = article.find("a",href=True)

                if not title_tag or not link_tag:
                    continue

                title =  title_tag.get_text(strip=True)
                href = link_tag["href"]

                if any(re.search(keyword,title ,re.IGNORECASE)for keyword in keywords):
                    if not href.startswith("http"):
                        href = base_url+ href
                    articles.append((title,href))
    

        else:
            print(f"查詢網頁失敗,狀態碼{response.status_code}")

    return articles


async def send_to_message(update:Update,context:ContextTypes.DEFAULT_TYPE):
    results = search_to_abmedia()

    if results:
        message = (f"📰<b>crypto news熱門關鍵字文章：</b>\n\n")

        for title , href in results:
            message += (f"📎<b>{title}</b>\n 📎<b>{href}</b>\n\n")

        await context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode="HTML")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="沒有符合的文章")


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("news", send_to_message))

    print("🤖Telegram Bot 正在運作...")

    app.run_polling()

if __name__ == "__main__":
    main()

