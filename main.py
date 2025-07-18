# main.py
import re
import requests
from telegram.ext import Updater, MessageHandler, Filters

# 🔑 CONFIG - Replace with your actual keys
TELEGRAM_BOT_TOKEN = '7917551868:AAHlVUsSLSJ1gi5ruNUouR8asSiZ8dn8hbM'
GPLINKS_API_KEY = '2469484d258897da1dc9edaf4face6f466301f39'
AROLINKS_API_KEY = '9ebb1dc3ef10cfbe1d433e2ba98c3d023b843468'

# 🔍 GPLinks URL Extractor
def extract_gplinks(text):
    return re.findall(r'(https?://gplinks\.co/\S+)', text)

# 🚀 GPLinks API
def bypass_gplink(url):
    try:
        res = requests.get(f"https://gplinks.co/api?api={GPLINKS_API_KEY}&url={url}")
        data = res.json()
        return data['shortenedUrl']
    except:
        return None

# 🎯 AroLinks API
def make_arolink(original_url):
    try:
        res = requests.get(f"https://arolinks.com/api?api={AROLINKS_API_KEY}&url={original_url}")
        data = res.json()
        return data['shortenedUrl']
    except:
        return None

# 🧠 Main Bot Logic
def handle(update, context):
    text = update.message.text
    urls = extract_gplinks(text)
    if urls:
        for url in urls:
            bypassed = bypass_gplink(url)
            if bypassed:
                arolink = make_arolink(bypassed)
                if arolink:
                    update.message.reply_text(f'🔗 Converted Link: {arolink}')
                else:
                    update.message.reply_text("❌ AroLinks me issue aaya.")
            else:
                update.message.reply_text("❌ GPLinks bypass nahi hua.")
    else:
        update.message.reply_text("🧐 Koi GPLinks URL nahi mila.")

# ▶️ Bot Start
def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text, handle))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
