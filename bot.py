import os
import asyncio
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "adubot is alive"

def run():
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host='0.0.0.0', port=port)

def keep_alive():
    Thread(target=run).start()

DELETE_AFTER = 60

async def a(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    msg_id = update.message.message_id

    await asyncio.sleep(DELETE_AFTER)

    try:
        await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
        print(f"Deleted {msg_id}")
    except Exception as e:
        print("Delete failed:", e)

bot_app = ApplicationBuilder().token(os.getenv("8359980681:AAGtSb-Su8zg6MGuKPGBR73gCEj52sPVfNY")).build()
bot_app.add_handler(MessageHandler(filters.ALL, a))

keep_alive()
bot_app.run_polling()
