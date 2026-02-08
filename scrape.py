from playwright.sync_api import sync_playwright
import json, re
from datetime import datetime


def get_alif_rub(page):
    page.goto("https://alif.tj/", timeout=60000)
    page.wait_for_timeout(5000)
    text = page.inner_text("body")

    match = re.search(r"1\s*RUB\s*([\d.]+)\s*([\d.]+)", text)
    buy, sell = match.groups() if match else ("0.0000", "0.0000")

    return {
        "bank": "Алиф Бонк",
        "currency": "RUB",
        "buy": buy,
        "sell": sell,
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M")
    }


def get_dc_rub(page):
    page.goto("https://dc.tj/", timeout=60000)
    page.wait_for_timeout(6000)
    text = page.inner_text("body")

    match = re.search(r"RUB\s*([\d.]+)\s*TJS\s*([\d.]+)", text)
    sell, buy = match.groups() if match else ("0.0000", "0.0000")

    return {
        "bank": "Dushanbe City",
        "currency": "RUB",
        "buy": buy,
        "sell": sell,
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M")
    }


def get_humo_rub(page):
    page.goto("https://humo.tj/ru/", timeout=60000)
    page.wait_for_timeout(5000)
    text = page.inner_text("body")

    match = re.search(r"1\s*RUB\s*([\d.]+)\s*([\d.]+)", text)
    buy, sell = match.groups() if match else ("0.0000", "0.0000")

    return {
        "bank": "Хумо",
        "currency": "RUB",
        "buy": buy,
        "sell": sell,
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M")
    }


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    banks_data = [
        get_alif_rub(page),
        get_dc_rub(page),
        get_humo_rub(page)
    ]

    browser.close()


data = {
    "source": "Auto Banks",
    "updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
    "banks": banks_data
}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("UPDATED:", data)
