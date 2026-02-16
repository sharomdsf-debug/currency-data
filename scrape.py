import requests
import json
import os
import time
from datetime import datetime

GROK_API_KEY = os.getenv("GROK_API_KEY")

BANKS = [
    {"name": "Alif", "url": "https://alif.tj/ru"},
    {"name": "Humo", "url": "https://humo.tj/ru/"},
    {"name": "DC", "url": "https://dc.tj/"},
    {"name": "Imon", "url": "https://imon.tj/"},
    {"name": "Eskhata", "url": "https://eskhata.com/"}
]

rates = []

for bank in BANKS:
    print(f"🔄 {bank['name']} - оғоз шуд...")

    prompt = f"""Қурби 1 RUB ба TJS (харид ва фурӯш)-ро аз {bank['url']} барор. 
Саҳифаро кушо, JS-ро иҷро кун ва дақиқ барор. 
Фақат JSON баргардон."""

    try:
        time.sleep(25)   # 25 сония интизорӣ — барои Grok вақт дошта бошад

        resp = requests.post(
            "https://api.x.ai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROK_API_KEY}", "Content-Type": "application/json"},
            json={
                "model": "grok-4-1-fast",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.0,
                "max_tokens": 400
            },
            timeout=120
        )

        content = resp.json()["choices"][0]["message"]["content"].strip()
        if "```" in content:
            content = content.split("```json")[-1].split("```")[0].strip()

        data = json.loads(content)
        rates.append(data)
        print(f"✅ {bank['name']} тайёр")

    except Exception as e:
        print(f"❌ Хато {bank['name']}: {str(e)}")
        rates.append({"bank": bank["name"], "rub_buy": None, "rub_sell": None, "updated": datetime.now().strftime("%Y-%m-%d %H:%M")})

final_data = {
    "last_updated": datetime.now().isoformat(),
    "rates": rates
}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(final_data, f, ensure_ascii=False, indent=2)

print("🎉 Тайёр! Процесс {0} дақиқа вақт гирифт".format(int(time.time() - time.time())))  # вақт нишон медиҳад
