import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

# Стартовое меню
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💰 Preise", callback_data="preise")],
        [InlineKeyboardButton("ℹ️ Was ist OlyLife?", callback_data="about")],
        [InlineKeyboardButton("📞 Kontakt", callback_data="kontakt")],
        [InlineKeyboardButton("🚀 Abo starten", callback_data="abo")]
    ]
    text = (
        "Willkommen bei *OlyLife*\\! 👋\n\n"
        "Dein Partner für Gesundheit, Energie und Freiheit\\.\n\n"
        "Was möchtest du wissen\\?"
    )
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="MarkdownV2")

# Кнопки
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "preise":
        await query.edit_message_text(
            "💰 *Unsere Pakete:*\n\n"
            "• Starter \\- 29€ / Monat\n"
            "• Family \\- 49€ / Monat\n"
            "• Business \\- 99€ / Monat\n\n"
            "✅ 30 Tage Geld\\-zurück\\-Garantie",
            parse_mode="MarkdownV2"
        )
    elif query.data == "about":
        await query.edit_message_text(
            "ℹ️ *OlyLife*\n\n"
            "Internationales Unternehmen für Gesundheit und Wellness\\.\n"
            "Über 10 Jahre am Markt, hochwertige Produkte, faire Chancen\\."
        )
    elif query.data == "kontakt":
        await query.edit_message_text("📞 Schreib uns: @OlyLife\\_Support")
    elif query.data == "abo":
        await query.edit_message_text(
            "🚀 *Bereit zu starten\\?*\n\n"
            "Schreibe an @OlyLife\\_Support\n"
            "oder olylife\\.de",
            parse_mode="MarkdownV2"
        )

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    print("Bot läuft...")
    app.run_polling()

if __name__ == "__main__":
    main()
