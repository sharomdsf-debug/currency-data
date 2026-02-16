from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import json
from datetime import datetime

BANKS = [
    {"name": "Alif", "url": "https://alif.tj/ru"},
    {"name": "Humo", "url": "https://humo.tj/ru/"},
    {"name": "DC", "url": "https://dc.tj/"},
    {"name": "Imon", "url": "https://imon.tj/"},
    {"name": "Eskhata", "url": "https://eskhata.com/"},
]

rates = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    for bank in BANKS:
        try:
            print(f"Рафт {bank['name']} ...")
            page.goto(bank["url"], wait_until="networkidle", timeout=60000)
            page.wait_for_timeout(8000)  # JS-ро иҷро кунад

            html = page.content()
            soup = BeautifulSoup(html, 'html.parser')

            # Ҷустуҷӯи умумӣ барои RUB (агар selector-и дақиқ лозим шавад — ислоҳ мекунем)
            rub_text = soup.find(string=lambda t: t and ('RUB' in t or 'Рубль' in t or 'руб' in t.lower()))
            if rub_text:
                parent = rub_text.find_parent(['tr', 'div', 'li', 'p'])
                if parent:
                    buy = parent.find(string=lambda t: t and ('покупка' in t or 'buy' in t or 'харид' in t))
                    sell = parent.find(string=lambda t: t and ('продажа' in t or 'sell' in t or 'фурӯш' in t))
                    rub_buy = buy.find_next('span' or 'td' or 'div').get_text(strip=True) if buy else None
                    rub_sell = sell.find_next('span' or 'td' or 'div').get_text(strip=True) if sell else None

                    rates.append({
                        "bank": bank["name"],
                        "rub_buy": float(rub_buy.replace(',', '.')) if rub_buy else None,
                        "rub_sell": float(rub_sell.replace(',', '.')) if rub_sell else None,
                        "updated": datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
                    print(f"{bank['name']} тайёр")
            else:
                print(f"RUB дар {bank['name']} пайдо нашуд")
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
