from playwright.sync_api import sync_playwright
import json, re
from datetime import datetime

# ---------------- ALIF ----------------
def get_alif_rub(page):
    page.goto("https://alif.tj/", timeout=120000)
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(8000)

    text = page.inner_text("body")
    match = re.search(r"1\s*RUB\s*([\d.]+)\s*([\d.]+)", text)

    buy = match.group(1) if match else "0.0000"
    sell = match.group(2) if match else "0.0000"

    return {
        "bank": "Alif",
        "currency": "RUB",
        "buy": buy,
        "sell": sell,
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M")
    }


# ---------------- DUSHANBE CITY ----------------
def get_dc_rub(page):
    page.goto("https://dc.tj/", timeout=120000)
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(8000)

    text = page.inner_text("body")
    match = re.search(r"RUB\s*([\d.]+)\s*TJS\s*([\d.]+)", text)

    sell = match.group(1) if match else "0.0000"
    buy = match.group(2) if match else "0.0000"

    return {
        "bank": "Dushanbe City",
        "currency": "RUB",
        "buy": buy,
        "sell": sell,
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M")
    }


# ---------------- HUMO ----------------
def get_humo_rub(page):
    page.goto("https://humo.tj/ru/", timeout=120000)
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(8000)

    text = page.inner_text("body")

    # 1 RUB 0.1205 0.1230
    match = re.search(r"1\s*RUB\s*([\d.]+)\s*([\d.]+)", text)

    buy = match.group(1) if match else "0.0000"
    sell = match.group(2) if match else "0.0000"

    return {
        "bank": "Humo",
        "currency": "RUB",
        "buy": buy,
        "sell": sell,
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M")
    }


# ---------------- MAIN ----------------
with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--no-sandbox", "--disable-dev-shm-usage"]
    )

    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
    )

    page = context.new_page()

    banks = []
    banks.append(get_alif_rub(page))
    banks.append(get_dc_rub(page))
    banks.append(get_humo_rub(page))

    browser.close()


data = {
    "source": "Auto Banks",
    "updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
    "banks": banks
}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("UPDATED:", data)
