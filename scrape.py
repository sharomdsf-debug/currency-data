import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

URL = "https://kurs.tj"

response = requests.get(URL, timeout=20)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

banks = []

for row in soup.find_all("tr"):
    cols = row.find_all("td")
    if len(cols) >= 4:
        bank = cols[0].get_text(strip=True)
        currency = cols[1].get_text(strip=True)

        if currency == "RUB":
            buy = cols[2].get_text(strip=True)
            sell = cols[3].get_text(strip=True)

            banks.append({
                "bank": bank,
                "buy": buy,
                "sell": sell,
                "updated": datetime.now().strftime("%H:%M")
            })

data = {
    "updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
    "banks": banks
}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
