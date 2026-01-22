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

    # НБТ: 100 RUB = X TJS
    raw_value = tds[2].replace(",", ".").strip()

    try:
        value_for_100 = float(raw_value)
    except ValueError:
        continue

    if value_for_100 <= 0:
        continue

    # ✅ ТАБДИЛ: 1 RUB = X / 100 TJS
    rub_to_tjs = round(value_for_100 / 100, 4)

    banks.append({
        "bank": bank_name,
        "currency": "RUB",
        "buy": rub_to_tjs,
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
