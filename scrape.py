from datetime import datetime

def get_eskhata_rub(page):
    rub_buy = rub_sell = "0.0000"

    def handle_response(response):
        nonlocal rub_buy, rub_sell
        try:
            ct = response.headers.get("content-type", "")
            if "application/json" not in ct:
                return

            data = response.json()

            # Вариант 1: рӯйхати объектҳо
            if isinstance(data, list):
                for item in data:
                    code = (item.get("code") or item.get("currency") or "").upper()
                    if code == "RUB":
                        rub_buy  = str(item.get("buy")  or item.get("purchase") or rub_buy)
                        rub_sell = str(item.get("sell") or item.get("sale")     or rub_sell)

            # Вариант 2: объекти дохилаш list дорад
            if isinstance(data, dict):
                for v in data.values():
                    if isinstance(v, list):
                        for item in v:
                            code = (item.get("code") or item.get("currency") or "").upper()
                            if code == "RUB":
                                rub_buy  = str(item.get("buy")  or item.get("purchase") or rub_buy)
                                rub_sell = str(item.get("sell") or item.get("sale")     or rub_sell)
        except:
            pass

    page.on("response", handle_response)

    page.goto("https://eskhata.com/", timeout=60000)
    page.wait_for_timeout(8000)  # вақт медиҳем, XHR-ҳо биёянд

    return {
        "bank": "Эсхата",
        "currency": "RUB",
        "buy": rub_buy,
        "sell": rub_sell,
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
