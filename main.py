import re
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# ✅ API Keys
TELEGRAM_BOT_TOKEN = '7917551868:AAFLj0WWUjVIaIqTTS5CKpLomsst71Q7hyQ'
GPLINKS_API_KEY = '2469484d258897da1dc9edaf4face6f466301f39'
AROLINKS_API_KEY = '9ebb1dc3ef10cfbe1d433e2ba98c3d023b843468'

# 🔍 Extract GPLinks
def extract_gplinks(text):
    return re.findall(r'(https?://gplinks\.co/\S+)', text)

# 🔓 Bypass GPLinks
def bypass_gplink(url):
    try:
        res = requests.get(f"https://gplinks.co/api?api={GPLINKS_API_KEY}&url={url}")
        data = res.json()
        return data['shortenedUrl']
    except:
        return None

# 🔁 Convert to AroLinks
def make_arolink(original_url):
    try:
        res = requests.get(f"https://arolinks.com/api?api={AROLINKS_API_KEY}&url={original_url}")
        data = res.json()
        return data['shortenedUrl']
    except:
        return None

# 🧠 Message Handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    links = extract_gplinks(text)
    if links:
        for gplink in links:
            bypassed = bypass_gplink(gplink)
            if bypassed:
                arolink = make_arolink(bypassed)
                if arolink:
                    reply = f"""✅ *Link Converted Successfully!*

🔗 GPLink: `{gplink}`
🔓 Original: `{bypassed}`
🔁 AroLink: `{arolink}`"""
                    await update.message.reply_text(reply, parse_mode='Markdown')
                else:
                    await update.message.reply_text("❌ AroLinks conversion failed.")
            else:
                await update.message.reply_text("❌ GPLinks bypass failed.")
    else:
        await update.message.reply_text("⚠️ Koi GPLinks URL nahi mila.")

# ▶️ Start Bot
if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Bot started successfully...")
    app.run_polling()
