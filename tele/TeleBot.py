import requests
from bs4 import BeautifulSoup
import re

from telegram import Update
from telegram.ext import Application,CommandHandler,ContextTypes

TELEGRAM_TOKEN = "7671557996:AAFIrBJ9mNenIZiAJwjfr291POr4MSw6rYU"
CHAT_ID = "7658509784"

# 關鍵字列表（不分大小寫）
keywords = ["比特幣", "以太幣", "bitcoin", "eth", "ethereum", "ada"]

# ABMedia 網站
base_url = "https://abmedia.io"

def send_to_telegram(message):

    url=f"https://api.telegram.org/bot7671557996:AAFIrBJ9mNenIZiAJwjfr291POr4MSw6rYU/sendMessage"

    data = {
        "chat_id":CHAT_ID,
        "text":message,
        "parse_mode":"HTML"
    }
    response = requests.post(url, data=data)
    if response.status_code ==200:
        print("✅ 訊息已傳送到 Telegram")
    else:
        print(f"❌ 傳送失敗，狀態碼：{response.status_code}")
        print(response.text)

def fetch_abmedia_articles():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
    }
    response = requests.get(base_url, headers=headers,timeout=20)
    if response.status_code ==200:

        soup = BeautifulSoup(response.text, "html.parser")

        articles = []

        for article in soup.find_all("article"):
            #href 它需要明確的值或是設定為 True 才能當作篩選條件。
            link_tag = article.find("a", href=True)
            #在這網頁裡title都在h3格式裡
            title_tag = article.find("h3")
            if not link_tag or not title_tag:
                continue

            title = title_tag.text.strip()
            href = link_tag["href"]

            # 比對關鍵字,(re.IGNORECASE)這句代表忽略大小寫,在尾巴必須加入，如果你的關鍵字是英文，一定要加 re.IGNORECASE，保證不漏字！✊
            # 你也可以對中文、英文混合的文章做更穩的過濾～
            #search是re模組裡的函式
            if any(re.search(keyword, title, re.IGNORECASE) for keyword in keywords):
                # 組成完整網址(startswith)很重要 要記得
                if not href.startswith("http"):
                    href = base_url + href
                    #這是把一筆資料 (title, href) 加進 articles 這個列表（list）中。這兩個東西 綁在一起當成一筆資料，而不是分開的兩個值,所以說要使用雙括號
                articles.append((title, href))
        return articles
    else:
        print(f"錯誤，狀態碼{response.status_code}")


async def get_news_handler(update:Update,context:ContextTypes.DEFAULT_TYPE):
    results =fetch_abmedia_articles()
    if results:
        message = ("📰<b> ABMeadia 熱門關鍵字文章：</b>\n\n")
        for title , link in results:
            message += f" 📌<b> {title}</b>\n 🔗{link}\n\n"
        await context.bot.send_message(chat_id=update.effective_chat.id,text=message,parse_mode="HTML")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,text="沒有符合關鍵字的文章。")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("gettingNews",get_news_handler))

    print("🤖Telegram Bot 正在運作...")

    app.run_polling()

if __name__ == "__main__":
    main()