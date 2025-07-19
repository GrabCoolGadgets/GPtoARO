import requests
from bs4 import BeautifulSoup
import re

def bypass_gplinks(gplink_url):
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        response = session.get(gplink_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        meta = soup.find("meta", attrs={"http-equiv": "refresh"})
        if meta:
            redirect_url = meta["content"].split("url=")[-1]
            return redirect_url

        scripts = soup.find_all("script")
        for script in scripts:
            if script.string and "window.location.href" in script.string:
                match = re.search(r'window\.location\.href\s*=\s*"(.*?)"', script.string)
                if match:
                    return match.group(1)

    except Exception as e:
        print("❌ Error:", e)

    return None

if __name__ == "__main__":
    gplink = input("Paste GPLinks URL: ")
    destination = bypass_gplinks(gplink)
    if destination:
        print("✅ Final destination link
