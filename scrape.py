def get_eskhata_rub(page):
    page.goto("https://eskhata.com/", timeout=60000)

    # интизор мешавем то блоки "Курсы валют" бор шавад
    page.wait_for_selector("text=Курсы валют")

    # сатри RUB дар ҷадвал
    row = page.locator("tr:has-text('RUB')")

    buy  = row.locator("td").nth(1).inner_text().strip()   # Банк покупает
    sell = row.locator("td").nth(2).inner_text().strip()   # Банк продает

    return {
        "bank": "Эсхата",
        "currency": "RUB",
        "buy": buy,
        "sell": sell,
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
