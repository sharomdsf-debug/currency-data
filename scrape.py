import json
from datetime import datetime
from playwright.sync_api import sync_playwright

banks = []

def scrape_alif(page):
    page.goto("https://alif.tj/", timeout=60000)
    page.wait_for_timeout(5000)

    text = page.inner_text("body")

    # намунаи ҷустуҷӯ (метавонем баъд дақиқтар кунем)
    if "RUB" in text:
        banks.append({
            "bank": "Алиф Бонк",
            "currency": "RUB",
            "sell": "0.1200",
            "updated": datetime.now().strftime("%Y-%m-%d %H:%M")
        })

def scrape_spitamen(page):
    page.goto("https://spitamenbank.tj/", timeout=60000)
    page.wait_for_timeout(5000)

    text = page.inner_text("body")

    if "RUB" in text:
        banks.append({
            "bank": "Спитамен Банк",
            "currency": "RUB",
            "sell": "0.1200",
            "updated": datetime.now().strftime("%Y-%m-%d %H:%M")
        })

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    scrape_alif(page)
    scrape_spitamen(page)

    browser.close()

data = {
    "source": "Banks Auto",
    "updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
    "banks": banks
}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("DONE:", len(banks))
