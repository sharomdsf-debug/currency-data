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

    # интизор мешавем то блоки RUB намоён шавад
    page.wait_for_selector("text=RUB")

    # блоки RUB
    rub_row = page.locator("text=RUB").first.locator("xpath=ancestor::*[self::div or self::tr][1]")

    # ҳамаи рақамҳои дохили он блок
    nums = re.findall(r"\d+\.\d+", rub_row.inner_text())

    if len(nums) >= 2:
        sell = nums[0]  # Продажа
        buy  = nums[1]  # Покупка
    else:
        sell = buy = "0.0000"

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
    banks_data.append(get_alif_rub(page))
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
