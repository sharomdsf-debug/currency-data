import requests
import json
from datetime import datetime

def get_eskhata_rub():
    url = "https://meta.eskhata.com/api/PublicWebPlugin/GetSettings"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
        "Accept": "application/json",
        "Origin": "https://eskhata.com",
        "Referer": "https://eskhata.com/",
    }

    r = requests.get(url, headers=headers, timeout=20)

    data = r.json()

    rub_buy = rub_sell = "0.0000"

    # дар ҷавоб курсҳо ҳастанд, мо RUB-ро меҷӯем
    def search(obj):
        nonlocal rub_buy, rub_sell
        if isinstance(obj, dict):
            code = str(obj.get("code") or obj.get("currency") or "").upper()
            if code == "RUB":
                rub_buy = str(obj.get("buy") or obj.get("purchase") or rub_buy)
                rub_sell = str(obj.get("sell") or obj.get("sale") or rub_sell)
            for v in obj.values():
                search(v)
        elif isinstance(obj, list):
            for item in obj:
                search(item)

    search(data)

    return {
        "bank": "Эсхата",
        "currency": "RUB",
        "buy": rub_buy,
        "sell": rub_sell,
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

print(get_eskhata_rub())
