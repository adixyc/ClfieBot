from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters
)

BOT_TOKEN = "8597105923:AAF9m8C4k5UVYlJCm7vGbN9vdYvjdiQt5VU"

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"Hello {user.first_name}! 👋\n"
        f"I'm alive and ready to serve this group."
    )

# Welcome new members
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        await update.message.reply_text(
            f"{member.first_name} JUST UNLOCKED FRIENDS CHATTING GROUP."
        )

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))

print("Bot is running...")
app.run_polling()
