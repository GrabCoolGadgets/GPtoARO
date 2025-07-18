import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# 🔐 Tokens & API Keys (use environment variables or hardcoded)
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "your_telegram_bot_token")
BYPASS_API = "https://gptoaro-1.onrender.com/bypass/bypass"
AROLINKS_API_KEY = os.environ.get("AROLINKS_API_KEY", "your_arolink_api_key")

# 🔗 AroLinks Shortener
def create_arolink(original_url):
    try:
        api_url = f"https://api.arolinks.com/api?api={AROLINKS_API_KEY}&url={original_url}"
        res = requests.get(api_url)
        data = res.json()
        if data.get("status") == "success":
            return data.get("shortenedUrl")
        else:
            return None
    except:
        return None

# 📩 Message Handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.strip()

    if not user_message.startswith("https://gplinks.co/"):
        await update.message.reply_text("⚠️ Sirf GPLinks URL bhejo.")
        return

    await update.message.reply_text("⏳ Bypassing GPLinks...")

    try:
        bypass_res = requests.get(BYPASS_API, params={"url": user_message})
        data = bypass_res.json()

        if data.get("status") != "success":
            await update.message.reply_text("❌ Bypass failed.")
            return

        real_url = data.get("destination")
        short_url = create_arolink(real_url)

        if short_url:
            await update.message.reply_text(f"✅ AroLink Ready:\n{short_url}")
        else:
            await update.message.reply_text("❌ AroLinks shortening failed.")

    except Exception as e:
        await update.message.reply_text("❌ Error: " + str(e))

# 🟢 Start Bot
async def on_startup(app):
    print("🤖 Bot started...")
    # Optionally send a message to admin here if needed

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).post_init(on_startup).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
