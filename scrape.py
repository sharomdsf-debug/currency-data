import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

URL = "https://kurs.tj"

headers = {
    "User-Agent": "Mozilla/5.0"
}

html = requests.get(URL, headers=headers, timeout=30).text
soup = BeautifulSoup(html, "html.parser")

banks = []

tables = soup.find_all("table")

for table in tables:
    rows = table.find_all("tr")
    for row in rows:
        cols = [c.get_text(strip=True) for c in row.find_all("td")]

        # интизори формат: Бонк | Асъор | Харид | Фурӯш
        if len(cols) >= 4:
            bank = cols[0]
            currency = cols[1]

            if currency.upper() == "RUB":
                banks.append({
                    "bank": bank,
                    "buy": cols[2],
                    "sell": cols[3],
                    "updated": datetime.now().strftime("%H:%M")
                })

data = {
    "updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
    "banks": banks
}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
