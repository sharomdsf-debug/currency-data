import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

URL = "https://nbt.tj/tj/kurs/kurs_kommer_bank.php"
headers = {"User-Agent": "Mozilla/5.0"}

resp = requests.get(URL, headers=headers, timeout=30)
resp.encoding = "utf-8"
soup = BeautifulSoup(resp.text, "html.parser")

banks = []

table = soup.find("table")
if not table:
    raise RuntimeError("Table not found")

rows = table.find_all("tr")

for r in rows[1:]:
    tds = [td.get_text(strip=True) for td in r.find_all("td")]
    if len(tds) < 3:
        continue

    bank_name = tds[0]

    # RUB → TJS (харид)
    rub_buy_raw = tds[2].replace(",", ".").strip()

    try:
        rub_buy = float(rub_buy_raw)
    except ValueError:
        continue

    # 0.0000-ҳоро намегирем (мисли kurs.tj)
    if rub_buy <= 0:
        continue

    banks.append({
        "bank": bank_name,
        "currency": "RUB",
        "buy": round(rub_buy, 4),
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M")
    })

data = {
    "source": "National Bank of Tajikistan",
    "updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
    "banks": banks
}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("OK. RUB → TJS banks:", len(banks))
