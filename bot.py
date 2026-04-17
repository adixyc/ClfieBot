
import os
import asyncio
import logging
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

logging.basicConfig(level=logging.INFO)

flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Bot alive"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port)

def keep_alive():
    t = Thread(target=run_web)
    t.daemon = True
    t.start()

DELETE_AFTER = 60
BOT_TOKEN = "8359980681:AAGtSb-Su8zg6MGuKPGBR73gCEj52sPVfNY"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is active.")

async def auto_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await asyncio.sleep(DELETE_AFTER)
    try:
        await context.bot.delete_message(
            chat_id=update.effective_chat.id,
            message_id=update.message.message_id
        )
    except Exception as e:
        print("Delete failed:", e)

def main():
    bot_app = ApplicationBuilder().token(BOT_TOKEN).build()

    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(MessageHandler(~filters.COMMAND, auto_delete))

    keep_alive()
    print("Bot polling started...")

    bot_app.run_polling(drop_pending_updates=True, close_loop=False)

if __name__ == "__main__":
    main()
