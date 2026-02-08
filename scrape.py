def get_eskhata_rub(page):
    rub_buy = rub_sell = "0.0000"

    def handle_response(response):
        nonlocal rub_buy, rub_sell

        url = response.url
        if "rate" in url.lower() or "currency" in url.lower():
            try:
                data = response.json()

                # Эсхата одатан чунин формат медиҳад:
                # [{"code":"RUB","buy":0.1180,"sell":0.1200}, ...]
                for item in data:
                    if item.get("code") == "RUB":
                        rub_buy  = str(item.get("buy"))
                        rub_sell = str(item.get("sell"))
            except:
                pass

    page.on("response", handle_response)

    page.goto("https://eskhata.com/", timeout=60000)
    page.wait_for_timeout(8000)

    return {
        "bank": "Эсхата",
        "currency": "RUB",
        "buy": rub_buy,
        "sell": rub_sell,
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
