import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# ✅ API KEYS
BOT_TOKEN = "7917551868:AAGwsx2ptetUGD5jYttRtbZG9SpCWFEWEHs"
AROLINKS_API_KEY = "9ebb1dc3ef10cfbe1d433e2ba98c3d023b843468"
BYPASS_API = "https://gptoaro-1.onrender.com/bypass"  # 🔁 replace with your actual render URL

# ✅ Start message when bot runs
async def start_message(app):
    chat_id = "1413767412"  # 👈 Replace with your Telegram User ID
    try:
        await app.bot.send_message(chat_id=chat_id, text="🤖 Bot is Live and Ready!")
    except Exception as e:
        print("❌ Could not send startup message:", e)

# ✅ Handle user messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.strip()

    if not user_message.startswith("https://gplinks.co/"):
        await update.message.reply_text("⚠️ Ye GPLinks short link hai. Sirf GPLinks link bhejo.")
        return

    await update.message.reply_text("⏳ GPLinks bypass ho raha hai...")

    try:
        # Step 1: Bypass GPLinks to get real destination
        bypass_res = requests.get(BYPASS_API, params={"url": user_message})
        bypass_data = bypass_res.json()

        if bypass_data.get("status") != "success":
            await update.message.reply_text("❌ GPLinks bypass failed.")
            return

        real_url = bypass_data.get("destination")

        # Step 2: AroLinks shortening
        aro_api = f"https://api.arolinks.com/api?api={AROLINKS_API_KEY}&url={real_url}"
        aro_res = requests.get(aro_api).json()

        if aro_res.get("status") == "success":
            short_url = aro_res["shortenedUrl"]
            await update.message.reply_text(f"✅ AroLink Ready:\n{short_url}")
        else:
            await update.message.reply_text("❌ AroLinks shortening failed.")

    except Exception as e:
        await update.message.reply_text("❌ Error occurred while processing.")
        print("Error:", e)

# ✅ Start Bot
if __name__ == "__main__":
    print("🤖 Starting bot...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Optional: Send "Bot is live" message
    app.post_init = start_message

    app.run_polling()
