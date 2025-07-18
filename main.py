import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters

# 🔐 CONFIGURATION
BOT_TOKEN = "7917551868:AAGwsx2ptetUGD5jYttRtbZG9SpCWFEWEWEHs"
AROLINKS_API_KEY = "9ebb1dc3ef10cfbe1d433e2ba98c3d023b843468"
BYPASS_API = "https://gptoaro-1.onrender.com/bypass"  # 🔁 Replace with your Render deployed API URL

# 🔗 Convert original URL to AroLink short URL
def create_arolink(original_url):
    try:
        api_url = f"https://api.arolinks.com/api?api={AROLINKS_API_KEY}&url={original_url}"
        response = requests.get(api_url)
        data = response.json()
        if data.get("status") == "success":
            return data.get("shortenedUrl")
    except:
        return None
    return None

# 👋 Handle /start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 *Welcome to GPLinks ➜ AroLinks Bot!*\n\n"
        "📥 *Send me any GPLinks short link*,\n"
        "I'll bypass it and give you a working AroLink. 🔁\n\n"
        "🧪 Just send link like:\n`https://gplinks.co/xxxxxxx`",
        parse_mode="Markdown"
    )

# 📩 Handle normal messages (links)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if not text.startswith("https://gplinks.co/"):
        await update.message.reply_text("⚠️ Ye already GPLinks short link hai. Original URL bhejo.")
        return

    await update.message.reply_text("⏳ GPLinks bypass ho raha hai...")

    try:
        res = requests.get(BYPASS_API, params={"url": text})
        data = res.json()

        if data.get("status") != "success":
            await update.message.reply_text("❌ GPLinks bypass failed.")
            return

        real_url = data.get("destination")
        short_url = create_arolink(real_url)

        if short_url:
            await update.message.reply_text(f"✅ *AroLink Ready:*\n{short_url}", parse_mode="Markdown")
        else:
            await update.message.reply_text("❌ AroLinks shortening failed.")

    except Exception as e:
        await update.message.reply_text("❌ Unexpected error occurred.")

# 🚀 Start the bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot is running...")
    app.run_polling()
