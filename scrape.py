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
    if len(tds) < 4:
        continue

    bank = tds[0]
    # Дар ҷадвали NBT сутунҳои RUB одатан 2-юм ва 3-юм ҳастанд
    rub_buy = tds[2].replace(",", ".")
    rub_sell = tds[3].replace(",", ".")

    banks.append({
        "bank": bank,
        "currency": "RUB",
        "buy": rub_buy,
        "sell": rub_sell,
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M")
    })

data = {
    "source": "National Bank of Tajikistan",
    "updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
    "banks": banks
}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("OK. Banks:", len(banks))
