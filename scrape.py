import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

HEADERS = {"User-Agent": "Mozilla/5.0"}

# Конфиг: ФАҚАТ бонкҳое, ки HTML доранд
# selector-ҳоро агар лозим шавад, иваз мекунӣ
BANKS = [
    {
        "name": "Ориёнбонк",
        "url": "https://oriyonbonk.tj/",
        # мисол: дар ҷадвал RUB дар сатри алоҳида меояд
        "row_contains": "RUB",
        "buy_col_index": 1,   # индекс сутуни харид (0-based)
        "table_selector": "table",  # selector ҷадвал
    },
    {
        "name": "Амонатбонк",
        "url": "https://www.amonatbonk.tj/",
        "row_contains": "RUB",
        "buy_col_index": 1,
        "table_selector": "table",
    },
    # Бонкҳои дигарро ИН ҶО илова кун, агар HTML дошта бошанд
]

def fetch_html(url):
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.encoding = "utf-8"
    return r.text

def parse_rub_buy(html, cfg):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.select_one(cfg["table_selector"])
    if not table:
        return None

    for tr in table.find_all("tr"):
        tds = [td.get_text(strip=True) for td in tr.find_all("td")]
        if not tds:
            continue
        # сатре, ки RUB дорад
        if cfg["row_contains"] in " ".join(tds):
            try:
                raw = tds[cfg["buy_col_index"]].replace(",", ".")
                val = float(raw)
                # агар барои 100 RUB навишта бошад → ба 1 RUB табдил деҳ
                if val > 1:
                    val = round(val / 100, 4)
                return val
            except Exception:
                return None
    return None

results = []
now = datetime.now().strftime("%Y-%m-%d %H:%M")

for b in BANKS:
    try:
        html = fetch_html(b["url"])
        buy = parse_rub_buy(html, b)
        if buy is None:
            continue
        results.append({
            "bank": b["name"],
            "currency": "RUB",
            "buy": buy,          # 1 RUB = X TJS
            "updated": now
        })
    except Exception:
        continue

data = {
    "source": "Banks (HTML only)",
    "updated": now,
    "banks": results
}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("OK. Banks parsed:", len(results))
