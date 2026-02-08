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


from playwright.sync_api import sync_playwright
import re
from datetime import datetime

def get_dc_rub():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://dc.tj/", timeout=60000)

        # интизор мешавем то RUB пайдо шавад
        page.wait_for_selector("text=RUB")

        # блоки RUB-ро мегирем
        rub_block = page.locator("text=RUB").first.locator("..")
        text = rub_block.inner_text()

        print("DEBUG DC BLOCK:", text)  # барои тафтиш

        # ҷустуҷӯи 2 рақам
        nums = re.findall(r"\d+\.\d+", text)

        sell = nums[0]  # Продажа
        buy  = nums[1]  # Покупка

        browser.close()

        return buy, sell
