import os
import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    CommandHandler,
    filters,
)

# 🛡️ Env Vars or hardcoded tokens
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "7917551868:AAGwsx2ptetUGD5jYttRtbZG9SpCWFEWEHs")
BYPASS_API = "https://gptoaro-1.onrender.com/bypass"  # ⛔️ Replace with actual deployed bypass URL
AROLINKS_API_KEY = os.environ.get("AROLINKS_API_KEY", "9ebb1dc3ef10cfbe1d433e2ba98c3d023b843468")

# 🔗 Create AroLink
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

# 📩 Handle messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.strip()

    if not user_message.startswith("https://gplinks.co/"):
        await update.message.reply_text("⚠️ Sirf GPLinks ka short link bhejo.")
        return

    await update.message.reply_text("⏳ Bypassing GPLinks...")

    try:
        bypass_res = requests.get(BYPASS_API, params={"url": user_message})
        data = bypass_res.json()

        if data.get("status") != "success":
            await update.message.reply_text("❌ GPLinks bypass failed.")
            return

        real_url = data.get("destination")
        short_url = create_arolink(real_url)

        if short_url:
            await update.message.reply_text(f"✅ AroLink Ready:\n{short_url}")
        else:
            await update.message.reply_text("❌ AroLinks shortening failed.")

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

# 🟢 Bot startup message (optional)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot is running. Send me a GPLinks short URL.")

# ▶️ Start app
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Bot started...")
    app.run_polling()
