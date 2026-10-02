import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ==============================
# SETTINGS
# ==============================

BOT_TOKEN = os.environ["BOT_TOKEN"]

CHANNEL_LINK = "https://t.me/+vR2rLmOtc2EyOWQ1"


# ==============================
# RENDER FREE PORT SERVER
# ==============================

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Matka Result Bot is running")

    def log_message(self, format, *args):
        return


def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)

    print(f"Web server running on port {port}")

    server.serve_forever()


# ==============================
# START MESSAGE
# ==============================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    name = update.effective_user.first_name or "User"

    message = f"""
👋 Welcome {name}!

📢 MATKA RESULT BOT

Get channel announcements and updates in one place.

🔔 Regular Updates
📢 Important Announcements
📋 Channel Information

👇 Join our private Telegram channel below.

🔞 18+ only.
Please follow applicable local laws.
"""

    keyboard = [
        [
            InlineKeyboardButton(
                "📢 JOIN PRIVATE CHANNEL",
                url=CHANNEL_LINK
            )
        ],
        [
            InlineKeyboardButton(
                "ℹ️ ABOUT",
                callback_data="about"
            )
        ],
        [
            InlineKeyboardButton(
                "❓ HELP",
                callback_data="help"
            )
        ]
    ]

    await update.message.reply_text(
        message,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ==============================
# BUTTONS
# ==============================

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "about":

        text = """
ℹ️ MATKA RESULT BOT

This bot provides channel information and announcements.

Use the button below to access the private Telegram channel.
"""

        keyboard = [[
            InlineKeyboardButton(
                "📢 JOIN PRIVATE CHANNEL",
                url=CHANNEL_LINK
            )
        ]]

        await query.message.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "help":

        await query.message.reply_text(
            "❓ HELP\n\n"
            "Use /start to open the main menu.\n\n"
            "Tap 📢 JOIN PRIVATE CHANNEL to open the channel."
        )


# ==============================
# HELP COMMAND
# ==============================

async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "❓ HELP\n\n"
        "/start - Main Menu\n"
        "/help - Help"
    )


# ==============================
# MAIN
# ==============================

def main():

    # Start Render HTTP server
    threading.Thread(
        target=run_web_server,
        daemon=True
    ).start()

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CommandHandler("help", help_command)
    )

    application.add_handler(
        CallbackQueryHandler(buttons)
    )

    print("Matka Result Bot Running...")

    application.run_polling(
        allowed_updates=Update.ALL_TYPES
    )


if __name__ == "__main__":
    main()
