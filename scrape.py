import re
from datetime import datetime
from playwright.sync_api import sync_playwright

BANKS = [
    {
        "name": "Alif Bank",
        "url": "https://alif.tj/",
    }
]

def extract_rub_sell(text):
    # Ҷустуҷӯи RUB ва рақами наздик (мисол: RUB 0.1234)
    m = re.search(r"RUB[^0-9]*([\d.,]+)", text, re.IGNORECASE)
    if not m:
        return None
    return float(m.group(1).replace(",", "."))

def main():
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        for bank in BANKS:
            try:
                page.goto(bank["url"], timeout=60000)
                page.wait_for_load_state("networkidle")
                page.wait_for_timeout(5000)  # интизор JS

                body_text = page.inner_text("body")
                rate = extract_rub_sell(body_text)

                if rate:
                    results.append({"bank": bank["name"], "sell": rate})
                else:
                    print("RUB not found for", bank["name"])

            except Exception as e:
                print("Error:", bank["name"], e)

        browser.close()

    data = {
        "currency": "RUB_TJS",
        "type": "sell",
        "updated": datetime.utcnow().strftime("%Y-%m-%d %H:%M"),
        "banks": results
    }

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
