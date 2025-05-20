from telegram import Update
from telegram.ext import Application , CommandHandler , ContextTypes
from config import setting
from K_line.search_eth_Kline import fetch_to_eth
from crawler.crawlerAbmedia import fetch_to_abmedia
from crawler.crawlerblockcast import fetch_to_blockcast
from crawler.crawlercoingraph import fetch_to_coingraph
from K_line.search_near_Kline import fetch_to_near

token = setting.TOKEN

#K線以太
async def search_eth(update,context):
    buf , text = fetch_to_eth()

    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=buf)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

#K線Near
async def search_near(update,context):
    buf , text = fetch_to_near()

    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=buf)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

#爬蟲abmedia
async def search_abmedia(update,context):
   
    results =fetch_to_abmedia()

    if results:
        message = (f"📰<b>crypto news熱門關鍵字文章：</b>\n\n")

        for title , href in results:
            message += (f"📎<b>{title}</b>\n 📎<b>{href}</b>\n\n")

        await context.bot.send_message(chat_id=update.effective_chat.id,text=message,parse_mode="HTML")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,text="找不到相關新聞。")

#爬蟲blockcast
async def search_blockcast(update:Update,context:ContextTypes.DEFAULT_TYPE):
    
    results = fetch_to_blockcast()
    if results:
        print("bot在運作中...")
        message = (f"📰<b>crypto news熱門關鍵字文章：</b>\n\n")

        for title , href in results:
            message += (f"📎<b>{title}</b>\n 📎<b>{href}</b>\n\n")

        await context.bot.send_message(chat_id=update.effective_chat.id,text=message,parse_mode="HTML")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,text="找不到相關新聞。")

#爬蟲coingraph
async def search_coingraph(update:Update,context:ContextTypes.DEFAULT_TYPE):
    results = fetch_to_coingraph()

    if results:
        message = (f"📰<b>crypto news熱門關鍵字文章：</b>\n\n")

        for title , href in results:
            message += (f"📎<b>{title}</b>\n 📎<b>{href}</b>\n\n")

        await context.bot.send_message(chat_id=update.effective_chat.id,text=message,parse_mode="HTML")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,text="找不到相關新聞。")

        

def main():
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("eth_line", search_eth))
    app.add_handler(CommandHandler("near_line",search_near))
    app.add_handler(CommandHandler("news", search_abmedia))
    app.add_handler(CommandHandler("news2", search_blockcast))
    app.add_handler(CommandHandler("news3",search_coingraph))
    app.run_polling()

if __name__=="__main__":
    main()