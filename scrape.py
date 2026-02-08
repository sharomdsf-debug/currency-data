from playwright.sync_api import sync_playwright
import json
from datetime import datetime


def get_humo_rub(page):
    page.goto("https://humo.tj/ru/", timeout=60000)
    page.wait_for_timeout(5000)

    rows = page.locator("text=RUB").locator("..")

    if rows.count() == 0:
        return None

    row = rows.first
    numbers = row.locator("xpath=.//text()[contains(.,'.')]").all_inner_texts()

    # Одатан 2 рақам аст: покупка, продажа
    buy = numbers[0].strip()
    sell = numbers[1].strip()

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
