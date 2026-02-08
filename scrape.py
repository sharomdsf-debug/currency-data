import requests
import json
from datetime import datetime

def get_eskhata_rub():
    url = "https://meta.eskhata.com/api/PublicWebPlugin/GetSettings"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Referer": "https://eskhata.com/",
        "Origin": "https://eskhata.com"
    }

    rub_buy = "0.0000"
    rub_sell = "0.0000"

    try:
        r = requests.get(url, headers=headers, timeout=15)

        # агар сервер ҷавоб надод
        if r.status_code != 200:
            print("Server error:", r.status_code)
            return rub_buy, rub_sell

        data = r.json()

        # дохили JSON ҷустуҷӯи RUB
        def search(obj):
            nonlocal rub_buy, rub_sell

            if isinstance(obj, dict):
                code = str(obj.get("code") or obj.get("currency") or "").upper()
                if code == "RUB":
                    rub_buy  = str(obj.get("buy")  or obj.get("purchase") or rub_buy)
                    rub_sell = str(obj.get("sell") or obj.get("sale")     or rub_sell)

                for v in obj.values():
                    search(v)

            elif isinstance(obj, list):
                for item in obj:
                    search(item)

        search(data)

    except Exception as e:
        print("ERROR:", e)

    return rub_buy, rub_sell


buy, sell = get_eskhata_rub()

data = {
    "source": "Auto Banks",
    "updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
    "banks": [
        {
            "bank": "Эсхата",
            "currency": "RUB",
            "buy": buy,
            "sell": sell,
            "updated": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
    ]
}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("ESKHATA RUB:", buy, sell)
