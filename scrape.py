import requests
import json
import os
import time
from datetime import datetime

GROK_API_KEY = os.getenv("GROK_API_KEY")
if not GROK_API_KEY:
    raise ValueError("GROK_API_KEY дар GitHub Secrets нест!")

# Фақат 1 бонк барои тест
BANK = {"name": "Alif", "url": "https://alif.tj/ru"}

print(f"🔄 Санҷиш барои {BANK['name']} оғоз шуд...")

prompt = f"""Қурби 1 RUB ба TJS-ро аз саҳифаи {BANK['url']} барор (харид/покупка ва фурӯш/продажа).
Ҳамон тавр ки қаблан дуруст гуфтӣ. Фақат JSON баргардон:

{{
  "bank": "{BANK['name']}",
  "rub_buy": 0.1225,
  "rub_sell": 0.1249,
  "updated": "2026-02-16 18:00"
}}

Ҳеҷ матни дигар нанавис."""

try:
    # Интизорӣ барои Grok вақт дошта бошад
    time.sleep(60)  # 60 сония (1 дақиқа) интизорӣ

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
        timeout=120  # timeout-и request-ро 2 дақиқа кун
    )

    if resp.status_code != 200:
        print(f"Хато API {resp.status_code}: {resp.text[:200]}")
        data = {"bank": BANK["name"], "rub_buy": None, "rub_sell": None, "updated": datetime.now().strftime("%Y-%m-%d %H:%M")}
    else:
        content = resp.json()["choices"][0]["message"]["content"].strip()
        # Тоза кардани ```json
        if content.startswith("```json"): content = content[7:].strip()
        if content.startswith("```"): content = content[3:].strip()
        if content.endswith("```"): content = content[:-3].strip()

        data = json.loads(content)
        data["updated"] = data.get("updated", datetime.now().strftime("%Y-%m-%d %H:%M"))
        print(f"Удачно барои {BANK['name']}: {data}")

except Exception as e:
    print(f"Хато умумӣ: {str(e)}")
    data = {"bank": BANK["name"], "rub_buy": None, "rub_sell": None, "updated": datetime.now().strftime("%Y-%m-%d %H:%M")}

final_data = {
    "last_updated": datetime.now().isoformat(),
    "rates": [data]
}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(final_data, f, ensure_ascii=False, indent=2)

print("✅ data.json барои Alif нав шуд!")
