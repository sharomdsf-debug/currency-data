import json
import os
from datetime import datetime

# ================== КАЛИД ==================
GROK_API_KEY = os.getenv("GROK_API_KEY")
if not GROK_API_KEY:
    raise ValueError("GROK_API_KEY дар GitHub Secrets гузошта нашудааст!")

# ================== РӮЙХАТИ БОНКҲО ==================
BANKS = [
    {"name": "Alif",      "url": "https://alif.tj/ru"},
    {"name": "Humo",      "url": "https://humo.tj/ru/"},
    {"name": "DC",        "url": "https://dc.tj/"},
    {"name": "Imon",      "url": "https://imon.tj/"},
    {"name": "Eskhata",   "url": "https://eskhata.com/"},
    # Агар бонкҳои дигар хоҳӣ, ҳамин ҷо илова кун
]

# ================== ФУНКЦИЯҲО ==================
def fetch_html(url):
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        r.raise_for_status()
        return r.text
    except Exception as e:
        print(f"HTML гирифтан нашуд {url}: {e}")
        return None

def extract_with_grok(html, bank_name):
    if not html:
        return {"bank": bank_name, "rub_buy": None, "rub_sell": None, "updated": datetime.now().strftime("%Y-%m-%d %H:%M")}

    prompt = f"""Ту эксперт ҳастӣ. Аз HTML-и бонки {bank_name} қурби 1 RUB ба TJS-ро барор (харид ва фурӯш).
Фақат JSON баргардон, ҳеҷ матни дигар набошад:

{{
  "bank": "{bank_name}",
  "rub_buy": 0.1200,
  "rub_sell": 0.1220,
  "updated": "2026-02-16 22:00"
}}

HTML:
{html[:28000]}"""

    try:
        resp = requests.post(
            "https://api.x.ai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROK_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "grok-4-1-fast",
                "messages": [
                    {"role": "system", "content": "Ту фақат JSON бармегардонӣ. Ҳеҷ матни иловагӣ набошад."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.0,
                "max_tokens": 300
            },
            timeout=40
        )

        if resp.status_code != 200:
            print(f"API хато {resp.status_code} барои {bank_name}")
            return None

        content = resp.json()["choices"][0]["message"]["content"].strip()

        # Тоза кардани 
json ва ```
        if content.startswith("
            content = content[7:].strip()
        if content.startswith("
"):
            content = content[3:].strip()
        if content.endswith("
            content = content[:-3].strip()

        data = json.loads(content)

        if "updated" not in data:
            data["updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")

        return data

    except Exception as e:
        print(f"Хато дар {bank_name}: {str(e)}")
        return None

# ================== АСОСИ КОД ==================
rates = []
for bank in BANKS:
    print(f"🔄 {bank['name']} - кор мекунад...")
    html = fetch_html(bank["url"])
    rate = extract_with_grok(html, bank["name"])
    
    if rate:
        rates.append(rate)
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

print("✅ data.json комилан нав шуд!")
