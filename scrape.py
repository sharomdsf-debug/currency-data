import requests
import json
import os
from datetime import datetime

GROK_API_KEY = os.getenv("GROK_API_KEY")

if not GROK_API_KEY:
    raise ValueError("GROK_API_KEY not found")

BANKS = [
    {"name": "Alif", "url": "https://alif.tj/ru"},
    {"name": "Humo", "url": "https://humo.tj/ru/"},
    {"name": "Dushanbe City", "url": "https://dc.tj/"},
    {"name": "Imon", "url": "https://imon.tj/"},
    {"name": "Eskhata", "url": "https://eskhata.com/"}
]

def fetch_html(url):
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
        r.raise_for_status()
        return r.text
    except Exception as e:
        print("Fetch error:", e)
        return None


def extract_with_grok(html, bank_name):
    if not html:
        return None

    prompt = f"""
Аз HTML қурби 1 RUB ба TJS-ро ёб.
Фақат JSON баргардон.

{{
  "bank": "{bank_name}",
  "rub_buy": 0.12,
  "rub_sell": 0.13
}}

HTML:
{html[:15000]}
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
                    {"role": "system", "content": "Фақат JSON баргардон."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0,
                "max_tokens": 300
            },
            timeout=40
        )

        if response.status_code != 200:
            print("API error:", response.text)
            return None

        content = response.json()["choices"][0]["message"]["content"].strip()

        # Агар
        if content.startswith("
"):
            content = content.replace("
            content = content.replace("
", "")
            content = content.strip()

        data = json.loads(content)
        data["updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")

        return data

    except Exception as e:
        print("Parsing error:", e)
        return None


all_rates = []

for bank in BANKS:
    print("Processing:", bank["name"])
    html = fetch_html(bank["url"])
    result = extract_with_grok(html, bank["name"])

    if result:
        all_rates.append(result)
    else:
        all_rates.append({
            "bank": bank["name"],
            "rub_buy": None,
            "rub_sell": None,
            "updated": datetime.now().strftime("%Y-%m-%d %H:%M")
        })

final_data = {
    "last_updated": datetime.now().isoformat(),
    "rates": all_rates
}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(final_data, f, ensure_ascii=False, indent=2)

print("Done")
