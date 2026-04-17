import os
import threading
import asyncio
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "8597105923:AAF9m8C4k5UVYlJCm7vGbN9vdYvjdiQt5VU"

app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot is running!"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(f"Hello {user.first_name}! 👋")

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        await update.message.reply_text(f"Welcome {member.first_name}! 🎉")

def run_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))

    app.run_polling()

threading.Thread(target=run_bot).start()

port = int(os.environ.get("PORT", 10000))
app_web.run(host="0.0.0.0", port=port)
