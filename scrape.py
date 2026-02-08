from playwright.sync_api import sync_playwright
import json, re
from datetime import datetime


def get_alif_rub(page):
    page.goto("https://alif.tj/", timeout=60000)
    page.wait_for_timeout(5000)

    text = page.inner_text("body")

    match = re.search(r"1\s*RUB\s*([\d.]+)\s*([\d.]+)", text)
    if match:
        buy = match.group(1)
        sell = match.group(2)
    else:
        buy = sell = "0.0000"

    return {
        "bank": "Алиф Бонк",
        "currency": "RUB",
        "buy": buy,
        "sell": sell,
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M")
    }


def get_dc_rub(page):
    page.goto("https://dc.tj/", timeout=60000)

    # интизор мешавем то ҷадвал бор шавад
    page.wait_for_selector("text=Валюта")

    # сатри RUB
    row = page.locator("text=RUB").locator("xpath=ancestor::div[1]")
    text = row.inner_text()

    import re
    numbers = re.findall(r"\d+\.\d+", text)

    if len(numbers) >= 2:
        sell = numbers[0]   # Продажа
        buy  = numbers[1]   # Покупка
    else:
        sell = buy = "0.0000"

    return {
        "bank": "Dushanbe City11",
        "currency": "RUB",
        "buy": buy,
        "sell": sell,
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
