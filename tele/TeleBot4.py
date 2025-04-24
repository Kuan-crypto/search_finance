import requests
from bs4 import BeautifulSoup as bs
import re

from telegram import Update
from telegram.ext import Application,CommandHandler,ContextTypes

TELEGRAM_TOKEN =
CHAT_ID =

keywords = [
    "bitcoin",
    "eth",
    "ethereum",
    "ada",
    "near"
]

base_url ="https://blockcast.it/"


def send_to_telegram():
    url =

    data ={
        "chat_id":CHAT_ID,
        "text":message,
        "parse_mode":"HTML"
    }

    response = requests.post(url,data=data)

    if response.status_code == 200:
        print("抓取成功")
    else:
        print(f"抓去失敗，狀態碼{response.status_code}")

def fetch_BlockCast_article():
    headers ={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
    }

    response = requests.get(base_url,headers = headers)

    soup = bs(response.text,"html.parser")

    articles = []

    if response.status_code == 200:
        for article in soup.find_all("article"):
            link_tag = article.find("a",href = True)
            title_tag = article.find("a",strip =True)

            if not link_tag or not title_tag:
                continue

            title = title_tag.text.strip()
            href = link_tag["href"]

            if any(re.search(keyword , title , re.IGNORECASE)for keyword in keywords):
                if not href.startswith("http"):
                    href = base_url + href

            articles.append((title,href))
        return articles

    else:
        print(f"無法開啟，狀態碼{response.status_code}")

async def get_news_blockcast(update:Update,context:ContextTypes.DEFAULT_TYPE):
    results = fetch_BlockCast_article()
    if results:
        message = (f"📰<b>熱門關鍵字文章:</b>\n\n")
        for title , link in results:
            message += (f"📎<b>{title}</b>\n 📎<b>{link}</b>\n\n")

        await context.bot.send_message(chat_id=update.effective_chat.id,text=message,parser_mode="HTML")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,text="沒有符合的文章")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("gettingNews", get_news_blockcast))

    print("🤖Telegram Bot 正在運作...")

    app.run_polling()

if __name__ =="__main__":
    main()

