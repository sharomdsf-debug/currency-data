def get_eskhata_rub(page):
    page.goto("https://eskhata.com/", timeout=60000)

    # интизор мешавем то ҷадвали курсҳо бор шавад
    page.wait_for_selector("text=Курсы валют")

    # сатри RUB-ро меёбем
    rub_row = page.locator("text=RUB").first.locator("..")

    text = rub_row.inner_text()

    # матн мисли:
    # RUB 0.1180 0.1200 0.1222
    import re
    nums = re.findall(r"\d+\.\d+", text)

    if len(nums) >= 2:
        buy = nums[0]   # Банк покупает
        sell = nums[1]  # Банк продает
    else:
        buy = sell = "0.0000"

    return {
        "bank": "Эсхата Банк",
        "currency": "RUB",
        "buy": buy,
        "sell": sell,
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
