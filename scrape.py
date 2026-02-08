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
    page.wait_for_selector("text=RUB")

    rub_block = page.locator("text=RUB").first.locator("..")
    text = rub_block.inner_text()

    nums = re.findall(r"\d+\.\d+", text)
    if len(nums) >= 2:
        sell = nums[0]
        buy = nums[1]
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

    banks = []
    banks.append(get_alif_rub(page))
    banks.append(get_dc_rub(page))   # ← ҲАМИН ҶО КОР МЕКУНАД

    browser.close()


data = {
    "source": "Auto Banks",
    "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "banks": banks
}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("DONE:", banks)
