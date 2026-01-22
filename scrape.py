import requests
from bs4 import BeautifulSoup

URL = "https://www.amonatbonk.tj/"
HEADERS = {"User-Agent": "Mozilla/5.0"}

r = requests.get(URL, headers=HEADERS, timeout=20)
r.encoding = "utf-8"

print("STATUS:", r.status_code)

soup = BeautifulSoup(r.text, "html.parser")

tables = soup.find_all("table")
print("TABLES FOUND:", len(tables))

for i, table in enumerate(tables):
    print(f"\n--- TABLE {i} ---")
    for tr in table.find_all("tr"):
        text = tr.get_text(" ", strip=True)
        if "RUB" in text or "руб" in text.lower():
            print("RUB ROW:", text)
