import requests
import json
import os
import time
from datetime import datetime
from playwright.sync_api import sync_playwright

GROK_API_KEY = os.getenv("GROK_API_KEY")
if not GROK_API_KEY:
    raise ValueError("GROK_API_KEY не найден!")

BANKS = [
    {"name": "Alif", "url": "https://alif.tj/ru"},
    {"name": "Humo", "url": "https://humo.tj/ru/"},
    {"name": "DC", "url": "https://dc.tj/"},
    {"name": "Imon", "url": "https://imon.tj/"},
    {"name": "Eskhata", "url": "https://eskhata.com/"},
]

rates = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(user_agent="Mozilla/5.0")
    page = context.new_page()

    for bank in BANKS:
        print(f"🔄 Кушодани {bank['name']} ...")
        
        page.goto(bank["url"], wait_until="networkidle", timeout=60000)
        time.sleep(8)  # JS-ро иҷро кунад

        full_html = page.content()  # HTML-и пурра бо JS

        prompt = f"""Аз ин HTML қурби 1 RUB ба TJS (харид ва фурӯш)-ро барор. 
Ҳамон тавр ки дар чат дуруст гуфтӣ. Фақат JSON баргардон:

{{
  "bank": "{bank['name']}",
  "rub_buy": 0.1225,
  "rub_sell": 0.1249,
  "updated": "2026-02-16 18:00"
}}

HTML:
{full_html[:35000]}"""   # 35к ҳарф — кофӣ аст

        try:
            time.sleep(12)  # Grok-ро интизор шав

            resp = requests.post(
                "https://api.x.ai/v1/chat/completions",
                headers={"Authorization": f"Bearer {GROK_API_KEY}", "Content-Type": "application/json"},
                json={
                    "model": "grok-4-1-fast",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.0,
                    "max_tokens": 400
                },
                timeout=90
            )

            content = resp.json()["choices"][0]["message"]["content"].strip()
            if content.startswith("```json"): content = content[7:].strip()
            if content.startswith("```"): content = content[3:].strip()
            if content.endswith("```"): content = content[:-3].strip()

            data = json.loads(content)
            rates.append(data)
            print(f"✅ {bank['name']} тайёр")

        except Exception as e:
            print(f"Хато {bank['name']}: {str(e)}")
            rates.append({"bank": bank["name"], "rub_buy": None, "rub_sell": None, "updated": datetime.now().strftime("%Y-%m-%d %H:%M")})

        time.sleep(15)  # байни бонкҳо 15 сония

    browser.close()

final_data = {
    "last_updated": datetime.now().isoformat(),
    "rates": rates
}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(final_data, f, ensure_ascii=False, indent=2)

print("🎉 Тайёр! data.json нав шуд")
