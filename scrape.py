def extract_with_grok(html, bank_name):
    if not html:
        return {"bank": bank_name, "rub_buy": None, "rub_sell": None, "updated": datetime.now().strftime("%Y-%m-%d %H:%M")}

    prompt = f"""Ту эксперт ҳастӣ дар қурби асъорҳои бонкҳои Тоҷикистон.
Аз ин HTML қурби 1 RUB ба TJS-ро барор (ҳатман харид ва фурӯш).
Калимаҳо барои ҷустуҷӯ: RUB, рубль, покупка, продажа, харид, фурӯш, buy, sell, курс.

Фақат JSON баргардон, ҳеҷ матни дигар набошад ва ҳеҷ кавычкаи иловагӣ нагузор:

{{
  "bank": "{bank_name}",
  "rub_buy": 0.1200,
  "rub_sell": 0.1220,
  "updated": "2026-02-16 21:00"
}}

HTML (бо ҳама чиз):
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
                    {"role": "system", "content": "Ту фақат JSON чист бармегардонӣ. Ҳеҷ матни иловагӣ набошад."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.0,
                "max_tokens": 300
            },
            timeout=40
        )

        if resp.status_code != 200:
            print(f"API error {resp.status_code} for {bank_name}: {resp.text[:200]}")
            return {"bank": bank_name, "rub_buy": None, "rub_sell": None, "updated": datetime.now().strftime("%Y-%m-%d %H:%M")}

        raw_content = resp.json()["choices"][0]["message"]["content"].strip()

        # Тоза кардани
        if raw_content.startswith("
json"):
            raw_content = raw_content[7:].strip()  # 7 ҳарф барои
        if raw_content.startswith("
"):
            raw_content = raw_content[3:].strip()
        if raw_content.endswith("
            raw_content = raw_content[:-3].strip()

        # Агар ҳанӯз 
бошад, нест кун
        raw_content = raw_content.replace("`", "").strip()

        try:
            data = json.loads(raw_content)
        except json.JSONDecodeError as json_err:
            print(f"JSON decode error for {bank_name}: {json_err}")
            print("Raw content was:", raw_content[:300])
            return {"bank": bank_name, "rub_buy": None, "rub_sell": None, "updated": datetime.now().strftime("%Y-%m-%d %H:%M")}

        # Агар updated набошад, илова кун
        if "updated" not in data:
            data["updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")

        return data

    except Exception as e:
        print(f"General error for {bank_name}: {str(e)}")
        return {"bank": bank_name, "rub_buy": None, "rub_sell": None, "updated": datetime.now().strftime("%Y-%m-%d %H:%M")}
