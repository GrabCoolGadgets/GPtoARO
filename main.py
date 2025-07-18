from telegram import Update
from telegram.ext import (
    ApplicationBuilder, ContextTypes,
    MessageHandler, CommandHandler, filters
)
import requests

BOT_TOKEN = "7917551868:AAGwsx2ptetUGD5jYttRtbZG9SpCWFEWEHs"
AROLINKS_API_KEY = "9ebb1dc3ef10cfbe1d433e2ba98c3d023b843468"
BYPASS_API = "https://gptoaro-1.onrender.com/bypass"  # ✅ your working Flask URL

# AroLinks Shorten Function
def create_arolink(original_url):
    try:
        api_url = f"https://api.arolinks.com/api?api={AROLINKS_API_KEY}&url={original_url}"
        res = requests.get(api_url)
        data = res.json()
        return data.get("shortenedUrl") if data.get("status") == "success" else None
    except:
        return None

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Bot is live! Send a GPLinks link to convert to AroLink.")

# Main handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.strip()

    if not user_message.startswith("https://gplinks.co/"):
        await update.message.reply_text("⚠️ Sirf GPLinks short link bhejo.")
        return

    await update.message.reply_text("⏳ Bypassing GPLinks...")

    try:
        # Step 1: Bypass GPLinks
        bypass_res = requests.get(BYPASS_API, params={"url": user_message})
        bypass_data = bypass_res.json()

        if bypass_data.get("status") != "success":
            await update.message.reply_text("❌ GPLinks bypass failed.")
            return

        real_url = bypass_data.get("destination")

        # Step 2: Create AroLink
        short_url = create_arolink(real_url)
        if short_url:
            await update.message.reply_text(f"✅ AroLink Ready:\n{short_url}")
        else:
            await update.message.reply_text("❌ AroLinks shortening failed.")

    except Exception as e:
        await update.message.reply_text(f"❌ Error:\n{str(e)}")

# Start the Bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Bot started...")
    app.run_polling()
