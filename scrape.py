from playwright.sync_api import sync_playwright
import json
from datetime import datetime

BANKS = [
    {"name": "Alif",      "url": "https://alif.tj/ru"},
    {"name": "Humo",      "url": "https://humo.tj/ru/"},
    {"name": "DC",        "url": "https://dc.tj/"},
    {"name": "Imon",      "url": "https://imon.tj/"},
    {"name": "Eskhata",   "url": "https://eskhata.com/"},
]

def scrape_bank(page, bank):
    try:
        page.goto(bank["url"], wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(5000)  # 5 сония интизор барои JS

        # Ҷустуҷӯи rates (selector-ҳои умумӣ, агар тағйир ёбад — ислоҳ кун)
        # Масалан, барои RUB ҷустуҷӯ кун
        rub_row = page.query_selector('text=/RUB|Рубль/i')  # ё selector-и дақиқтар
        if rub_row:
            row = rub_row.evaluate_handle("el => el.closest('tr') or el.closest('div.row')")
            if row:
                buy = row.query_selector('text[contains(., "покупка") or contains(., "buy") or contains(., "харид")] ~ td') 
                sell = row.query_selector('text[contains(., "продажа") or contains(., "sell") or contains(., "фурӯш")] ~ td')
                rub_buy = buy.inner_text().strip() if buy else None
                rub_sell = sell.inner_text().strip() if sell else None

                return {
                    "bank": bank["name"],
                    "rub_buy": float(rub_buy.replace(',', '.')) if rub_buy else None,
                    "rub_sell": float(rub_sell.replace(',', '.')) if rub_sell else None,
                    "updated": datetime.now().strftime("%Y-%m-%d %H:%M")
                }

        print(f"Rates пайдо нашуд барои {bank['name']}")
        return {"bank": bank["name"], "rub_buy": None, "rub_sell": None, "updated": datetime.now().strftime("%Y-%m-%d %H:%M")}

    except Exception as e:
        print(f"Хато дар {bank['name']}: {str(e)}")
        return {"bank": bank["name"], "rub_buy": None, "rub_sell": None, "updated": datetime.now().strftime("%Y-%m-%d %H:%M")}

# ================== MAIN ==================
rates = []
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    page = context.new_page()

    for bank in BANKS:
        print(f"Рафт {bank['name']} ...")
        rate = scrape_bank(page, bank)
        rates.append(rate)

    browser.close()

final_data = {
    "last_updated": datetime.now().isoformat(),
    "rates": rates
}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(final_data, f, ensure_ascii=False, indent=2)

print("✅ data.json нав шуд бо Playwright!")
