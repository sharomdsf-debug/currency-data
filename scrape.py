import requests
from datetime import datetime

def get_eskhata_rub():
    rub_buy = rub_sell = "0.0000"

    try:
        url = "https://meta.eskhata.com/api/PublicWebPlugin/GetSettings"
        r = requests.get(url, timeout=10)

        # Агар сервер error дод — мегузарем
        if r.status_code != 200:
            return {
                "bank": "Эсхата",
                "currency": "RUB",
                "buy": rub_buy,
                "sell": rub_sell,
                "updated": datetime.now().strftime("%Y-%m-%d %H:%M")
            }

        try:
            data = r.json()
        except:
            return {
                "bank": "Эсхата",
                "currency": "RUB",
                "buy": rub_buy,
                "sell": rub_sell,
                "updated": datetime.now().strftime("%Y-%m-%d %H:%M")
            }

        # Ҷустуҷӯи RUB дар JSON
        if isinstance(data, dict):
            for v in data.values():
                if isinstance(v, list):
                    for item in v:
                        if str(item.get("code","")).upper() == "RUB":
                            rub_buy  = str(item.get("buy", rub_buy))
                            rub_sell = str(item.get("sell", rub_sell))

    except:
        pass

    return {
        "bank": "Эсхата",
        "currency": "RUB",
        "buy": rub_buy,
        "sell": rub_sell,
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
