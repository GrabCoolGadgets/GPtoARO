import re
import requests
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# Keys
TELEGRAM_BOT_TOKEN = "7917551868:AAGwsx2ptetUGD5jYttRtbZG9SpCWFEWEHs"
AROLINKS_API_KEY = "9ebb1dc3ef10cfbe1d433e2ba98c3d023b843468"

# Extract links from message
def extract_links(text):
    return re.findall(r"(https?://[^\s]+)", text)

# ✅ Real Bypass GPLinks using browser automation
def bypass_gplink(link):
    try:
        options = uc.ChromeOptions()
        options.headless = True
        options.add_argument("--no-sandbox")
        driver = uc.Chrome(options=options)

        driver.get(link)

        # Wait for 'Get Link' button to appear
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "go_link"))
        )
        final_button = driver.find_element(By.ID, "go_link")
        final_url = final_button.get_attribute("href")

        driver.quit()
        return final_url
    except Exception as e:
        print("Bypass Error:", e)
        return None

# AroLinks Convert
def convert_to_arolink(url):
    try:
        res = requests.get(
            f"https://arolinks.com/api?api={AROLINKS_API_KEY}&url={url}"
        )
        data = res.json()
        if data["status"] == "success":
            return data["shortenedUrl"]
        else:
            return None
    except:
        return None

# Telegram handler
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    links = extract_links(text)

    if not links:
        await update.message.reply_text("❌ Koi link nahi mila.")
        return

    for link in links:
        if "gplinks.co" not in link:
            await update.message.reply_text("❗ Sirf GPLinks link bhejo.")
            continue

        await update.message.reply_text("🔄 Bypassing GPLinks...")

        destination = bypass_gplink(link)

        if not destination:
            await update.message.reply_text("❌ Bypass failed.")
            return

        await update.message.reply_text(f"✅ Found: {destination}")

        arolink = convert_to_arolink(destination)

        if arolink:
            await update.message.reply_text(f"✅ AroLink: {arolink}")
        else:
            await update.message.reply_text("❌ AroLink convert failed.")

# Start bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    print("🤖 Bot Started")
    app.run_polling()
