import re
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# 🔑 API Keys
TELEGRAM_BOT_TOKEN = '7917551868:AAGwsx2ptetUGD5jYttRtbZG9SpCWFEWEHs'
AROLINKS_API_KEY = '9ebb1dc3ef10cfbe1d433e2ba98c3d023b843468'

# ✅ Step 1: Extract links from message
def extract_links(text):
    return re.findall(r'(https?://[^\s]+)', text)

# ✅ Step 2: Bypass GPLinks
def bypass_gplink(url):
    try:
        session = requests.Session()
        headers = {"User-Agent": "Mozilla/5.0"}
        response = session.get(url, headers=headers, allow_redirects=True, timeout=10)
        return response.url
    except Exception as e:
        print("❌ Bypass Error:", e)
        return None

# ✅ Step 3: Send to AroLinks
def convert_to_arolink(url):
    try:
        res = requests.get(f"https://arolinks.com/api?api={AROLINKS_API_KEY}&url={url}")
        data = res.json()
        if data.get("status") == "success":
            return data["shortenedUrl"]
        else:
            print("❌ AroLinks API error:", data)
            return None
    except Exception as e:
        print("❌ AroLinks Error:", e)
        return None

# ✅ Step 4: Handle incoming messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    links = extract_links(message)

    if not links:
        await update.message.reply_text("❗ Koi link nahi mila.")
        return

    for link in links:
        if "gplinks.co/" not in link:
            await update.message.reply_text("❗ Sirf GPLinks link bhejo.")
            continue

        await update.message.reply_text("🔄 Bypassing GPLinks...")

        original_url = bypass_gplink(link)

        if not original_url:
            await update.message.reply_text("❌ GPLinks bypass failed.")
            continue

        await update.message.reply_text(f"✅ Destination: `{original_url}`", parse_mode='Markdown')

        arolink = convert_to_arolink(original_url)

        if arolink:
            await update.message.reply_text(f"✅ AroLink: `{arolink}`", parse_mode='Markdown')
        else:
            await update.message.reply_text("❌ AroLink conversion failed.")

# ▶️ Start the bot
if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Bot started...")
    app.run_polling()
