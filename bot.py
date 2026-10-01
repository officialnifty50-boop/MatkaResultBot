import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📢 Announcements", callback_data="news")],
        [InlineKeyboardButton("ℹ️ About", callback_data="about")],
        [InlineKeyboardButton("❓ Help", callback_data="help")],
    ]

    await update.message.reply_text(
        "👋 Welcome to Matka Result Bot\n\n"
        "General information & announcements.",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "news":
        text = "📢 अभी कोई नया announcement उपलब्ध नहीं है."
    elif query.data == "about":
        text = (
            "ℹ️ @MatkaResult_bot\n\n"
            "General information & announcements bot."
        )
    else:
        text = "❓ Help\n\n/start - Main Menu\n/help - Help"

    await query.edit_message_text(text)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start - Main Menu\n"
        "/help - Help"
    )


def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN missing")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button))

    print("Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()
