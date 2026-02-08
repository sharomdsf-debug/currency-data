def get_dc_rub(page):
    page.goto("https://dc.tj/", timeout=60000)
    page.wait_for_selector("text=RUB")

    text = page.inner_text("body")
    lines = [l.strip() for l in text.splitlines() if l.strip()]

    sell = buy = "0.0000"

    for i, line in enumerate(lines):
        if "RUB" in line and i + 2 < len(lines):
            sell = lines[i + 1].replace("TJS", "").strip()
            buy  = lines[i + 2].replace("TJS", "").strip()
            break

    return {
        "bank": "Dushanbe City",
        "currency": "RUB",
        "buy": buy,
        "sell": sell,
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
