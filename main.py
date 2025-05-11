from fastapi import FastAPI
from TeleBot5 import search_to_abmedia,fetch_to_telegram
from cryptoLine2 import fetch_to_eth , send_to_photo
app = FastAPI()

@app.get("/")
async def read_main():
    return {"Hello":"歡迎來到我設計的網頁，雖然不是很好的介面，但我會隨著每天的學習成果加強我的設計方式跟理念"}

@app.get("/sendnews")
async def program_send_news():
    results = search_to_abmedia()

    if results:
        message = (f"📰<b>crypto news熱門關鍵字文章：</b>\n\n")

        for title , href in results:
            message += (f"📎<b>{title}</b>\n 📎<b>{href}</b>\n\n")

        fetch_to_telegram(message)
        return {"status": "ok", "message": "文章已推送到 Telegram"}
    else:
        return {"status": "empty", "message": "沒有符合的文章"}

