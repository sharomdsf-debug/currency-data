from playwright.sync_api import sync_playwright
import re, json
from datetime import datetime

def get_eskhata_rub():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # Мобилӣ месозем
        context = browser.new_context(
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
            viewport={"width": 390, "height": 844}
        )

        page = context.new_page()
        page.goto("https://eskhata.com/", timeout=60000)

        page.wait_for_timeout(5000)

        text = page.inner_text("body")

        # RUB блок
        match = re.search(
            r"RUB.*?Банк покупает\s*([\d.]+).*?Банк продает\s*([\d.]+)",
            text,
            re.S
        )

        if match:
            buy = match.group(1)
            sell = match.group(2)
        else:
            buy = sell = "0.0000"

        browser.close()

        return {
            "bank": "Эсхата",
            "currency": "RUB",
            "buy": buy,
            "sell": sell,
            "updated": datetime.now().strftime("%Y-%m-%d %H:%M")
        }


# -------- RUN --------
data = {
    "source": "Auto Banks",
    "updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
    "banks": [get_eskhata_rub()]
}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("ESKHATA:", data)
