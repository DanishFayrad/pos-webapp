from datetime import date

def run_safety_checks(medicine, stock, quantity):
    warnings = []

    if stock is None:
        warnings.append("This medicine is not available at this branch.")
        return warnings

    if stock.expiry_date and stock.expiry_date < date.today():
        warnings.append("This medicine has expired and is not eligible for sale.")

    if stock.quantity < quantity:
        warnings.append("Insufficient stock available for the selected medicine.")

    return warnings