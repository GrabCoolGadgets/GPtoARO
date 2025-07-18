import re
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# ✅ API Keys
TELEGRAM_BOT_TOKEN = '7917551868:AAGwsx2ptetUGD5jYttRtbZG9SpCWFEWEHs'
GPLINKS_API_KEY = '2469484d258897da1dc9edaf4face6f466301f39'
AROLINKS_API_KEY = '9ebb1dc3ef10cfbe1d433e2ba98c3d023b843468'

# 🔍 Extract all URLs
def extract_links(text):
    return re.findall(r'(https?://[^\s]+)', text)

# 🔗 Create GPLinks Short URL
def create_gplink(original_url):
    try:
        res = requests.get(f"https://gplinks.co/api?api={GPLINKS_API_KEY}&url={original_url}")
        data = res.json()
        if data.get("status") == "success" and "shortenedUrl" in data:
            return data["shortenedUrl"]
        else:
            print("GPLinks Error:", data)
            return None
    except Exception as e:
        print("❌ GPLinks Exception:", e)
        return None

# 🔁 Convert to AroLink
def create_arolink(original_url):
    try:
        res = requests.get(f"https://arolinks.com/api?api={AROLINKS_API_KEY}&url={original_url}")
        data = res.json()
        if data.get("status") == "success" and "shortenedUrl" in data:
            return data["shortenedUrl"]
        else:
            print("AroLinks Error:", data)
            return None
    except Exception as e:
        print("❌ AroLinks Exception:", e)
        return None

# 📩 Handle Messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    links = extract_links(text)

    if not links:
        await update.message.reply_text("⚠️ Koi bhi link nahi mila.")
        return

    for url in links:
        if "gplinks.co/" in url:
            await update.message.reply_text("⚠️ Ye already GPLinks short link hai. Original URL bhejo.")
            continue

        gplink = create_gplink(url)
        if not gplink:
            await update.message.reply_text("❌ GPLinks se shorten nahi ho paya.")
            continue

        arolink = create_arolink(gplink)
        if not arolink:
            await update.message.reply_text("❌ AroLinks conversion failed.")
            continue

        # ✅ Final Reply
        reply = f"""✅ *Link Converted Successfully!*

🔗 Original: `{url}`
🔁 GPLink: `{gplink}`
🔁 AroLink: `{arolink}`"""
        await update.message.reply_text(reply, parse_mode='Markdown')

# ▶️ Start Bot
if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Bot started...")
    app.run_polling()
