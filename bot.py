```python
import os
import asyncio
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

# ------------------- Flask Web Service -------------------
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Auto-delete bot is alive"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host='0.0.0.0', port=port)

def keep_alive():
    Thread(target=run_web).start()

# ------------------- Bot Config -------------------
DELETE_AFTER = 60  # seconds
BOT_TOKEN = os.getenv("BOT_TOKEN") 

# ------------------- Commands -------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Bot is active.\nMessages will auto-delete after {DELETE_AFTER} seconds."
    )

# ------------------- Auto Delete Logic -------------------
async def auto_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    msg_id = update.message.message_id

    await asyncio.sleep(DELETE_AFTER)

    try:
        await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
        print(f"Deleted message {msg_id}")
    except Exception as e:
        print("Delete failed:", e)

# ------------------- Main -------------------
def main():
    if not BOT_TOKEN:
        print("BOT_TOKEN environment variable not set.")
        return

    bot_app = ApplicationBuilder().token(BOT_TOKEN).build()

    # handlers
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(MessageHandler(~filters.COMMAND, auto_delete))

    # start flask server
    keep_alive()

    # start telegram bot
    bot_app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
```
