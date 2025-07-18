from telegram import Update
from telegram.ext import (
    ApplicationBuilder, ContextTypes,
    MessageHandler, CommandHandler, filters
)
import requests

BOT_TOKEN = "YOUR_BOT_TOKEN"
AROLINKS_API_KEY = "YOUR_AROLINKS_API_KEY"
BYPASS_API = "https://gptoaro-1.onrender.com/bypass"

def create_arolink(original_url):
    try:
        api_url = f"https://api.arolinks.com/api?api={AROLINKS_API_KEY}&url={original_url}"
        res = requests.get(api_url)
        data = res.json()
        return data.get("shortenedUrl") if data.get("status") == "success" else None
    except:
        return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Bot is active! Send a GPLinks link to begin.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.strip()

    if not user_message.startswith("https://gplinks.co/"):
        await update.message.reply_text("⚠️ Ye GPLinks short link hona chahiye.")
        return

    await update.message.reply_text("⏳ Bypassing GPLinks...")

    try:
        bypass_res = requests.get(BYPASS_API, params={"url": user_message})
        bypass_data = bypass_res.json()

        if bypass_data.get("status") != "success":
            await update.message.reply_text("❌ GPLinks bypass failed.")
            return

        real_url = bypass_data.get("destination")
        short_url = create_arolink(real_url)

        if short_url:
            await update.message.reply_text(f"✅ AroLink Ready:\n{short_url}")
        else:
            await update.message.reply_text("❌ AroLinks shortening failed.")
    except Exception as e:
        await update.message.reply_text(f"❌ Error occurred: {str(e)}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Bot started...")
    app.run_polling()
