from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

app = Flask(__name__)

def bypass_gplink(url):
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)

        time.sleep(10)  # wait for JS to load

        final_url = driver.current_url
        driver.quit()

        return final_url

    except Exception as e:
        return f"❌ Error: {str(e)}"

@app.route("/bypass", methods=["GET"])
def bypass():
    url = request.args.get("url")
    if not url:
        return jsonify({"status": "error", "message": "No URL provided."})

    result = bypass_gplink(url)
    if "http" in result:
        return jsonify({"status": "success", "destination": result})
    else:
        return jsonify({"status": "error", "message": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
