import requests
import json
import os
from datetime import datetime

# ==============================
# API KEY
# ==============================
GROK_API_KEY = os.getenv("GROK_API_KEY")
if not GROK_API_KEY:
    raise ValueError("❌ GROK_API_KEY not found in GitHub Secrets!")

# ==============================
# BANK LIST
# ==============================
BANKS = [
    {"name": "Alif", "url": "https://alif.tj/ru"},
    {"name": "Humo", "url": "https://humo.tj/ru/"},
    {"name": "Dushanbe City", "url": "https://dc.tj/"},
    {"name": "Imon", "url": "https://imon.tj/"},
    {"name": "Eskhata", "url": "https://eskhata.com/"}
]

# ==============================
# FETCH HTML
# ==============================
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
        print(f"❌ Error fetching {url}: {e}")
        return None


# ==============================
# GROK EXTRACTION
# ==============================
def extract_with_grok(html, bank_name):
    if not html:
        return {
            "bank": bank_name,
            "rub_buy": None,
            "rub_sell": None,
            "updated": datetime.now().strftime("%Y-%m-%d %H:%M")
        }

    html_part = html[:25000]

    prompt = f"""
Ту эксперт ҳастӣ. Аз HTML-и бонки {bank_name} қурби 1 RUB ба TJS-ро барор.
Калимаҳо: RUB, Рубль, покупка, продажа, харид, фурӯш, buy, sell.
Фақат JSON баргардон, ҳеҷ матни дигар набошад.

Формат:

{{
  "bank": "{bank_name}",
  "rub_buy": 0.12,
  "rub_sell": 0.13,
  "updated": "2026-02-16 21:00"
}}

HTML:
{html_part}
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
                    {"role": "system", "content": "Фақат JSON баргардон. Ягон матни дигар набошад."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0,
                "max_tokens": 300
            },
            timeout=40
        )

        if response.status_code != 200:
            print(f"❌ API Error {bank_name}: {response.text}")
            return None

        content = response.json()["choices"][0]["message"]["content"].strip()

        # Агар
        if "
" in content:
            content = content.split("`")[-2].strip()

        data = json.loads(content)

        if "updated" not in data:
            data["updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")

        return data

    except Exception as e:
        print(f"❌ Grok parsing error ({bank_name}): {e}")
        return None


# ==============================
# MAIN
# ==============================
def main():
    rates = []

    for bank in BANKS:
        print(f"🔄 Checking {bank['name']}...")
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

    print("✅ data.json successfully updated!")


if name == "main":
    main()
