from playwright.sync_api import sync_playwright
import json
import re
from datetime import datetime


def get_humo_rub(page):
    page.goto("https://humo.tj/ru/", timeout=60000)
    page.wait_for_timeout(5000)

    text = page.inner_text("body")

    # сатри RUB чунин аст:
    # 1 RUB 0.1205 0.1230
    match = re.search(r"1\s*RUB\s*([\d.]+)\s*([\d.]+)", text)

    if not match:
        print("RUB NOT FOUND")
        return None

    buy = match.group(1)
    sell = match.group(2)

    return {
        "bank": "Humo",
        "currency": "RUB",
        "buy": buy,
        "sell": sell,
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M")
    }


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    banks = []

    humo = get_humo_rub(page)
    if humo:
        banks.append(humo)

    browser.close()

data = {
    "source": "Auto Banks",
    "updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
    "banks": banks
}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("UPDATED:", data)
