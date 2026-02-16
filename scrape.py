import requests
import json
import os
import time
from datetime import datetime

GROK_API_KEY = os.getenv("GROK_API_KEY")

BANKS = [
    "Alif: https://alif.tj/ru",
    "Humo: https://humo.tj/ru/",
    "DC: https://dc.tj/",
    "Imon: https://imon.tj/",
    "Eskhata: https://eskhata.com/"
]

rates = []

for bank in BANKS:
    prompt = f"""Қурби 1 RUB ба TJS (харид ва фурӯш)-ро аз ин бонк барор. 
Саҳифаро кушо, JS-ро иҷро кун ва дақиқ барор.

Бонк: {bank}

Фақат JSON баргардон."""

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
                "tools": [{"type": "web_search"}],   # ← Ин ҳамон "умность"-и чат аст!
                "temperature": 0.0,
                "max_tokens": 400
            },
            timeout=90
        )

        content = resp.json()["choices"][0]["message"]["content"].strip()
        # Тоза кардани ```json
        if "```" in content:
            content = content.split("```json")[-1].split("```")[0].strip()

        data = json.loads(content)
        rates.append(data)
        print(f"✅ {bank} тайёр")

    except Exception as e:
        print(f"Хато {bank}: {e}")
        rates.append({"bank": bank.split(":")[0], "rub_buy": None, "rub_sell": None, "updated": datetime.now().strftime("%Y-%m-%d %H:%M")})

    time.sleep(12)  # 12 сония байни requestҳо

final_data = {
    "last_updated": datetime.now().isoformat(),
    "rates": rates
}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(final_data, f, ensure_ascii=False, indent=2)

print("🎉 Тайёр! data.json нав шуд")
