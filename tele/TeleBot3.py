import requests
from bs4 import BeautifulSoup as bs
import re

from telegram import Update
from telegram.ext import Application , CommandHandler , ContextTypes

CHAT_ID = "7658509784"
TELEGRAM_TOKEN ="7671557996:AAFIrBJ9mNenIZiAJwjfr291POr4MSw6rYU"

keywords = ["bitcoin","eth","ethereum","ada","near"]

base_url ="https://crypto.news/"

def send_to_telegram(message):
    url=f"https://api.telegram.org/bot7671557996:AAFIrBJ9mNenIZiAJwjfr291POr4MSw6rYU/sendMessage"

    data = {
        "chat_id":CHAT_ID,
        "text":message,
        "parse_mode":"HTML"
    }

    response = requests.post (url,data=data)
    if response.status_code == 200:
        print("抓取帳號成功")
    else:
        print(f"抓取帳號失敗，狀態碼{response.status_code}")

def fetch_crypto_article():
    headers ={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
    }
    response = requests.get (base_url,headers=headers,timeout=20)

    soup = bs(response.text,"html.parser")

    articles = []
    #第一段- 從首頁抓取文章
    if response.status_code == 200:
        for article in soup.find_all("div",class_="home-latest-news__list"):
            link_tag = article.find("a",href=True)
            title_tag = article.find("span")

            if not link_tag or not title_tag:
                continue

            title = title_tag.get_text(strip=True)

            href = link_tag["href"]

            if any(re.search(keyword , title , re.IGNORECASE)for keyword in keywords):
                if not href.startswith("http"):
                    href = base_url + href
                articles.append((title,href))

        #第二段-從<article>抓取文章
        for article in soup.find_all("article"):
            link_tag = article.find("a", href=True)

            if not link_tag:
                continue

            title = link_tag.get_text(strip=True)

            href = link_tag["href"]

            if any(re.search(keyword ,title,re.IGNORECASE)for keyword in keywords):
                if not href.startswith("http"):
                    href = base_url + href
                articles.append((title,href))

    else:
        print(f"爬取失敗，狀態碼{response.status_code}")

    return articles

async def get_crypto_news(update:Update,context:ContextTypes.DEFAULT_TYPE):
    results = fetch_crypto_article()

    if results:
        message =(f"📰<b>crypto news熱門關鍵字文章：</b>\n\n")

        for title , link in results:
            message += (f"📎<b>{title}</b>\n 📎<b>{link}</b>\n\n")

        await context.bot.send_message(chat_id = update.effective_chat.id,text = message,parse_mode = "HTML")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="沒有符合的文章")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("gettingNews", get_crypto_news))

    print("🤖Telegram Bot 正在運作...")

    app.run_polling()

if __name__ == "__main__":
    main()






