import requests
import json
import os
import time
from datetime import datetime

GROK_API_KEY = os.getenv("GROK_API_KEY")
if not GROK_API_KEY:
    raise ValueError("GROK_API_KEY дар GitHub Secrets нест!")

BANKS = [
    {"name": "Alif", "url": "https://alif.tj/ru"},
    {"name": "Humo", "url": "https://humo.tj/ru/"},
    {"name": "DC", "url": "https://dc.tj/"},
    {"name": "Imon", "url": "https://imon.tj/"},
    {"name": "Eskhata", "url": "https://eskhata.com/"},
]

rates = []

for bank in BANKS:
    print(f"🔄 Дар ҳолати пурсидан барои {bank['name']} ...")
    
    prompt = f"""Қурби 1 RUB ба TJS-ро аз саҳифаи {bank['url']} барор (харид/покупка ва фурӯш/продажа).
Ҳамон тавр ки қаблан дуруст гуфтӣ. Фақат JSON баргардон:

{{
  "bank": "{bank['name']}",
  "rub_buy": 0.1225,
  "rub_sell": 0.1249,
  "updated": "2026-02-16 18:00"
}}

Ҳеҷ матни дигар нанавис."""

    try:
        resp = requests.post(
            "https://api.x.ai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROK_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "grok-4-1-fast",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.0,
                "max_tokens": 300
            },
            timeout=60
        )

        if resp.status_code != 200:
            print(f"Хато API {resp.status_code} барои {bank['name']}: {resp.text[:200]}")
            rates.append({"bank": bank["name"], "rub_buy": None, "rub_sell": None, "updated": datetime.now().strftime("%Y-%m-%d %H:%M")})
        else:
            content = resp.json()["choices"][0]["message"]["content"].strip()
            # Тоза кардани ```json
            if content.startswith("```json"): content = content[7:].strip()
            if content.startswith("```"): content = content[3:].strip()
            if content.endswith("```"): content = content[:-3].strip()

            data = json.loads(content)
            data["updated"] = data.get("updated", datetime.now().strftime("%Y-%m-%d %H:%M"))
            rates.append(data)
            print(f"Удачно барои {bank['name']}: {data}")

    except Exception as e:
        print(f"Хато умумӣ барои {bank['name']}: {str(e)}")
        rates.append({"bank": bank["name"], "rub_buy": None, "rub_sell": None, "updated": datetime.now().strftime("%Y-%m-%d %H:%M")})

    time.sleep(8)  # 8 сония интизорӣ байни request-ҳо (то сервер overheat нашавад)

final_data = {
    "last_updated": datetime.now().isoformat(),
    "rates": rates
}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(final_data, f, ensure_ascii=False, indent=2)

print("✅ data.json аз Grok пурра нав шуд!")
