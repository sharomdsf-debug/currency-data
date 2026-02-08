from playwright.sync_api import sync_playwright
import json
from datetime import datetime


def get_dc_rub(page):
    page.goto("https://dc.tj/", timeout=60000)

    # интизор мешавем ҷадвал бор шавад
    page.wait_for_selector("text=RUB")

    # тамоми матни саҳифаро мегирем
    text = page.inner_text("body")

    # ҷудо мекунем қисми RUB
    lines = text.splitlines()

    sell = buy = "0.0000"

    for i, line in enumerate(lines):
        if "RUB" in line:
            # 2 сатри баъдӣ рақамҳоянд
            sell = lines[i + 1].replace("TJS", "").strip()
            buy  = lines[i + 2].replace("TJS", "").strip()
            break

    return {
        "bank": "Dushanbe City",
        "currency": "RUB",
        "buy": buy,
        "sell": sell,
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M")
    }


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    banks_data = []
    banks_data.append(get_dc_rub(page))

    browser.close()


data = {
    "source": "Auto Banks",
    "updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
    "banks": banks_data
}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("UPDATED:", data)
