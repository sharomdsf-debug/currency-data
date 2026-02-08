def get_dc_rub(page):
    page.goto("https://dc.tj/", timeout=60000)

    # интизор мешавем то ҷадвал бор шавад
    page.wait_for_selector("text=Курс валюты")

    # сатри RUB
    row = page.locator("text=RUB").first.locator("xpath=ancestor::div[contains(@class,'row') or contains(@class,'table')][1]")

    # Рақамҳо аз ҳамон сатри RUB
    nums = row.locator("text=TJS").all_inner_texts()

    if len(nums) >= 2:
        sell = nums[0].replace(" TJS","").strip()  # Продажа
        buy  = nums[1].replace(" TJS","").strip()  # Покупка
    else:
        sell = buy = "0.0000"

    return {
        "bank": "Dushanbe City",
        "currency": "RUB",
        "buy": buy,
        "sell": sell,
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
