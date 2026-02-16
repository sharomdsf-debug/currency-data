import requests
import json
import os
from datetime import datetime

GROK_API_KEY = os.getenv("GROK_API_KEY")
if not GROK_API_KEY:
    raise ValueError("GROK_API_KEY дар GitHub Secrets гузошта нашудааст!")

# Рӯйхати бонкҳо
BANKS = [
    "Alif: https://alif.tj/ru",
    "Humo: https://humo.tj/ru/",
    "DC: https://dc.tj/",
    "Imon: https://imon.tj/",
    "Eskhata: https://eskhata.com/",
]

def ask_grok_for_rates():
    prompt = f"""Қурби 1 RUB ба TJS (харид ва фурӯш)-ро аз ин бонкҳо барор, ҳамон тавр ки қаблан дуруст гуфтӣ:

{BANKS}

Барои ҳар бонк:
- rub_buy (покупка / харид)
- rub_sell (продажа / фурӯш)
- updated (сана/вақт, агар бошад)

Фақат JSON баргардон, мисли ин:

{{
  "last_updated": "2026-02-16T18:00:00",
  "rates": [
    {{"bank": "Alif", "rub_buy": 0.1225, "rub_sell": 0.1249, "updated": "2026-02-16 10:40"}},
    {{"bank": "Humo", "rub_buy": 0.1219, "rub_sell": 0.1243, "updated": "2026-02-16"}}
  ]
}}

Ҳеҷ матни иловагӣ нанавис."""

    try:
        resp = requests.post(
            "https://api.x.ai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROK_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "grok-4-1-fast",  # ё "grok-4-latest" агар tier-ат иҷозат диҳад
                "messages": [
                    {"role": "system", "content": "Ту фақат JSON бармегардонӣ. Ҳеҷ чизи дигар нанавис."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.0,
                "max_tokens": 800
            },
            timeout=60
        )

        if resp.status_code != 200:
            print(f"API хато: {resp.status_code} - {resp.text}")
            return {"last_updated": datetime.now().isoformat(), "rates": []}

        content = resp.json()["choices"][0]["message"]["content"].strip()

        # Тоза кардани ```json
        if content.startswith("```json"):
            content = content[7:].strip()
        if content.startswith("```"):
            content = content[3:].strip()
        if content.endswith("```"):
            content = content[:-3].strip()

        data = json.loads(content)

        print("Grok ҷавоб дод:", data)
        return data

    except Exception as e:
        print(f"Хато дар API: {str(e)}")
        return {"last_updated": datetime.now().isoformat(), "rates": []}

# ================== ИҶРОИ АСОСӢ ==================
data = ask_grok_for_rates()

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✅ data.json аз Grok нав шуд!")
