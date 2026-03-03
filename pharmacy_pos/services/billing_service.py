def calculate_total(items):
    subtotal = 0

    for item in items:
        item_subtotal = item['unit_price'] * item['quantity']
        subtotal += item_subtotal

    tax = subtotal * 0.05
    total = subtotal + tax

    return {
        "subtotal": round(subtotal, 2),
        "tax": round(tax, 2),
        "total": round(total, 2)
    }