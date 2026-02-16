import requests
import json
import os
from datetime import datetime

GROK_API_KEY = os.getenv("GROK_API_KEY")

if not GROK_API_KEY:
    raise ValueError("GROK_API_KEY is not set in GitHub Secrets")

BANKS = [
    {"name": "Alif", "url": "https://alif.tj/ru"},
    {"name": "Humo", "url": "https://humo.tj/ru/"},
    {"name": "Dushanbe City", "url": "https://dc.tj/"},
    {"name": "Imon", "url": "https://imon.tj/"},
    {"name": "Eskhata", "url": "https://eskhata.com/"}
]

def fetch_html(url):
    try:
        response = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=20
        )
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"HTML fetch error: {e}")
        return None


def extract_with_grok(html, bank_name):
    if not html:
        return {
            "bank": bank_name,
            "rub_buy": None,
            "rub_sell": None,
            "updated": datetime.now().strftime("%Y-%m-%d %H:%M")
        }

    prompt = f"""
Аз HTML-и бонки {bank_name} қурби 1 RUB ба TJS-ро ёб.
Ҳам харид (buy, покупка) ва ҳам фурӯш (sell, продажа).
Фақат JSON баргардон, ҳеҷ матни дигар набошад.

Формат:
{{
  "bank": "{bank_name}",
  "rub_buy": 0.12,
  "rub_sell": 0.13,
  "updated": "2026-02-16 21:00"
}}

HTML:
{html[:25000]}
"""

    try:
        response = requests.post(
            "https://api.x.ai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROK_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "grok-4-1-fast",
                "messages": [
                    {"role": "system", "content": "Ту танҳо JSON бармегардонӣ."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0,
                "max_tokens": 300
            },
            timeout=40
        )

        if response.status_code != 200:
            print(f"API error {bank_name}: {response.text}")
            return None

        content = response.json()["choices"][0]["message"]["content"].strip()

        # тоза кардани
        if content.startswith("
"):
            content = content.replace("
            content = content.replace("
", "")
            content = content.strip()

        data = json.loads(content)

        if "updated" not in data:
            data["updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")

        return data

    except Exception as e:
        print(f"Grok parsing error ({bank_name}): {e}")
        return None


# ================= MAIN =================

results = []

for bank in BANKS:
    print(f"Processing {bank['name']}")
    html = fetch_html(bank["url"])
    rate = extract_with_grok(html, bank["name"])

    if rate:
        results.append(rate)
    else:
        results.append({
            "bank": bank["name"],
            "rub_buy": None,
            "rub_sell": None,
            "updated": datetime.now().strftime("%Y-%m-%d %H:%M")
        })

final_data = {
    "last_updated": datetime.now().isoformat(),
    "rates": results
}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(final_data, f, ensure_ascii=False, indent=2)

print("Done")
