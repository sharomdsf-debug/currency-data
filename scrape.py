from playwright.sync_api import sync_playwright
import re
from datetime import datetime

def get_humo_rub(page):
    page.goto("https://humo.tj/ru/", timeout=60000)

    # интизор мешавем блоки курсҳо
    page.wait_for_selector("text=Курсы валют")

    text = page.inner_text("body")

    # ҷустуҷӯи сатри RUB
    match = re.search(r"1\s*RUB\s*([\d.]+)\s*([\d.]+)", text)

    if match:
        buy  = match.group(1)
        sell = match.group(2)
    else:
        buy = sell = "0.0000"

    return {
        "bank": "Хумо",
        "currency": "RUB",
        "buy": buy,
        "sell": sell,
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M")
    }


# ---- ИҶРО ----
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    humo = get_humo_rub(page)

    browser.close()

print(humo)
