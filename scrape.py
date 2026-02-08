from playwright.sync_api import sync_playwright
import json, re
from datetime import datetime

def get_alif_rub():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://alif.tj/", timeout=60000)

        page.wait_for_timeout(5000)

        text = page.inner_text("body")

        # Ҷустуҷӯи сатри RUB
        match = re.search(r"1\s*RUB\s*([\d.]+)\s*([\d.]+)", text)

        if match:
            buy = match.group(1)
            sell = match.group(2)
        else:
            buy = sell = "0.0000"

        browser.close()
        return buy, sell


buy, sell = get_alif_rub()

data = {
    "source": "Auto Banks",
    "updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
    "banks": [
        {
            "bank": "Алиф Бонк",
            "currency": "RUB",
            "buy": buy,
            "sell": sell,
            "updated": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
    ]
}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("ALIF RUB:", buy, sell)
