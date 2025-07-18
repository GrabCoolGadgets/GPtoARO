import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, CommandHandler, filters

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
AROLINKS_API_KEY = os.environ.get("AROLINKS_API_KEY")
BYPASS_API = "https://gptoaro-1.onrender.com/bypass"  # Replace with your actual API URL

# Start Command Message
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome! Send me a GPLinks URL to convert it into AroLinks.")

# Convert to AroLinks Function
def create_arolink(original_url):
    try:
        res = requests.get(f"https://api.arolinks.com/api?api={AROLINKS_API_KEY}&url={original_url}")
        data = res.json()
        if data.get("status") == "success":
            return data.get("shortenedUrl")
    except:
        return None
    return None

# Handle Message
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.strip()

    if not user_message.startswith("https://gplinks.co/"):
        await update.message.reply_text("⚠️ Please send a valid GPLinks short link.")
        return

    await update.message.reply_text("⏳ Bypassing GPLinks...")

    try:
        # Bypass GPLinks via your API
        bypass_res = requests.get(BYPASS_API, params={"url": user_message})
        bypass_data = bypass_res.json()

        if bypass_data.get("status") != "success":
            await update.message.reply_text("❌ GPLinks bypass failed.")
            return

        real_url = bypass_data.get("destination")

        # Shorten via AroLinks
        short_url = create_arolink(real_url)
        if short_url:
            await update.message.reply_text(f"✅ AroLink Ready:\n{short_url}")
        else:
            await update.message.reply_text("❌ AroLinks shortening failed.")
    except Exception as e:
        await update.message.reply_text("❌ Unexpected error occurred.")
        print("Error:", e)

# Run Bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot started...")
    app.run_polling()
