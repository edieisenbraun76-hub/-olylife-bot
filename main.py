from flask import Flask
import threading
flask_app = Flask(__name__)
@flask_app.route('/')
def home(): return "OlyLife bot is alive!"
threading.Thread(target=lambda: flask_app.run(host='0.0.0.0', port=10000), daemon=True).start()

import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💰 Preise", callback_data='price')],
        [InlineKeyboardButton("ℹ️ Was ist OlyLife?", callback_data='what')],
        [InlineKeyboardButton("📞 Kontakt", callback_data='contact')],
        [InlineKeyboardButton("🚀 Abo starten", callback_data='about')]
    ]
    text = (
        "Willkommen bei *OlyLife*\\! 👋\n\n"
        "Dein Partner fuer Gesundheit\n"
        "Was moechtest du wissen\\?"
    )
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="MarkdownV2")

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'price':
        await query.edit_message_text("💰 Starter - 29€ / Familie - 49€ / Business - 99€")
    elif query.data == 'what':
        await query.edit_message_text("OlyLife - Terahertz Technologie fuer deine Zellen.")
    elif query.data == 'contact':
        await query.edit_message_text("Schreib mir: @dein_nick")
    elif query.data == 'about':
        await query.edit_message_text("OlyLife International - Gesundheit ohne Tabletten.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    print("Bot started...")
    app.run_polling()

if __name__ == '__main__':
    main()
