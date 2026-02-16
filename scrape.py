import requests
import json
import os
from datetime import datetime

GROK_API_KEY = os.getenv("GROK_API_KEY")

if not GROK_API_KEY:
    raise ValueError("GROK_API_KEY not set")

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


def clean_json_block(text):
    text = text.strip()
    if text.startswith("
        text = text.replace("
json", "")
        text = text.replace("`", "")
    return text.strip()


def extract_with_grok(html, bank_name):
    if not html:
        return None

    prompt = f"""
Аз HTML қурби 1 RUB ба TJS-ро барор.
Фақат JSON баргардон.
Формат:

{{
  "bank": "{bank_name}",
  "rub_buy": 0.12,
  "rub_sell": 0.13
}}

HTML:
{html[:20000]}
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
                "temperature": 0
            },
            timeout=40
        )

        if response.status_code != 200:
            print("API error:", response.text)
            return None

        content = response.json()["choices"][0]["message"]["content"]
        content = clean_json_block(content)

        data = json.loads(content)
        data["updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")

        return data

    except Exception as e:
        print("Parsing error:", e)
        return None


# ================= MAIN =================

rates = []

for bank in BANKS:
    print("Processing:", bank["name"])
    html = fetch_html(bank["url"])
    result = extract_with_grok(html, bank["name"])

    if result:
        rates.append(result)
    else:
        rates.append({
            "bank": bank["name"],
            "rub_buy": None,
            "rub_sell": None,
            "updated": datetime.now().strftime("%Y-%m-%d %H:%M")
        })

final_data = {
    "last_updated": datetime.now().isoformat(),
    "rates": rates
}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(final_data, f, ensure_ascii=False, indent=2)

print("Finished successfully")
