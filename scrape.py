from playwright.sync_api import sync_playwright
import json
from datetime import datetime

BANKS = [
    {"name": "Alif", "url": "https://alif.tj/ru", "buy_sel": ".buy-price", "sell_sel": ".sell-price"},
    {"name": "Humo", "url": "https://humo.tj/ru/", "buy_sel": ".buy-rate", "sell_sel": ".sell-rate"},
    {"name": "DC", "url": "https://dc.tj/", "buy_sel": ".buy-value", "sell_sel": ".sell-value"},
    {"name": "Imon", "url": "https://imon.tj/", "buy_sel": ".purchase", "sell_sel": ".sale"},
    {"name": "Eskhata", "url": "https://eskhata.com/", "buy_sel": "td.buy", "sell_sel": "td.sell"},
]

rates = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    for bank in BANKS:
        try:
            page.goto(bank["url"], wait_until="networkidle", timeout=60000)
            page.wait_for_timeout(10000)  # 10 сония барои JS

            # Ҷустуҷӯи умумӣ барои RUB
            rub_element = page.query_selector('text=/RUB|рубль/i')
            if rub_element:
                parent = rub_element.evaluate_handle("el => el.closest('tr') or el.closest('.currency-item') or el.closest('div')")
                if parent:
                    buy = parent.query_selector(bank["buy_sel"] or 'text[содержит("покупка") or "buy" or "харид"] ~ span, td')
                    sell = parent.query_selector(bank["sell_sel"] or 'text[содержит("продажа") or "sell" or "фурӯш"] ~ span, td')

                    rub_buy = float(buy.inner_text().strip().replace(',', '.')) if buy else None
                    rub_sell = float(sell.inner_text().strip().replace(',', '.')) if sell else None

                    rates.append({
                        "bank": bank["name"],
                        "rub_buy": rub_buy,
                        "rub_sell": rub_sell,
                        "updated": datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
                    print(f"{bank['name']} тайёр: {rub_buy} / {rub_sell}")
            else:
                rates.append({"bank": bank["name"], "rub_buy": None, "rub_sell": None, "updated": datetime.now().strftime("%Y-%m-%d %H:%M")})

        except Exception as e:
            print(f"Хато {bank['name']}: {str(e)}")
            rates.append({"bank": bank["name"], "rub_buy": None, "rub_sell": None, "updated": datetime.now().strftime("%Y-%m-%d %H:%M")})

    browser.close()

final_data = {
    "last_updated": datetime.now().isoformat(),
    "rates": rates
}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(final_data, f, ensure_ascii=False, indent=2)

print("Тайёр!")
