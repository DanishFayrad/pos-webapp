from repositories.sales_repository import (
    create_sale,
    add_sale_item,
    get_stock_quantity,
    reduce_stock,
    get_medicine_info,
    log_ai_warning
)
from repositories.sales_repository import (
    get_valid_batch_quantity,
    check_near_expiry_batches
)

# 🎯 MAIN SALE SERVICE
def create_sale_service(data, current_user):

    branch_id = current_user["branch_id"]
    user_id = current_user["user_id"]

    items = data.get("items", [])
    prescription = data.get("has_prescription", False)

    if not items:
        return {"error": "No items in sale"}, 400

    total_amount = 0

    # ✅ FIRST PASS — validations
    for item in items:
        medicine_id = item["medicine_id"]
        qty = item["quantity"]

        # ✅ expiry-aware stock check
        valid_qty = get_valid_batch_quantity(branch_id, medicine_id)

        if valid_qty < qty:
           return {
        "error": f"Medicine {medicine_id} is expired or insufficient valid stock"
    }, 400
        
        # ⚠️ near expiry warning
        if check_near_expiry_batches(branch_id, medicine_id):
          log_ai_warning(
        sale_id,
        medicine_id,
        "Medicine sold from near-expiry batch"
    )

        # medicine info
        requires_prescription, unit_price = get_medicine_info(medicine_id)

        # prescription check
        if requires_prescription and not prescription:
            return {"error": f"Medicine {medicine_id} requires prescription"}, 400

        total_amount += float(unit_price) * qty

    # ✅ CREATE SALE
    sale_id = create_sale(branch_id, user_id, total_amount)

    # ✅ SECOND PASS — insert items + reduce stock
    for item in items:
        medicine_id = item["medicine_id"]
        qty = item["quantity"]

        _, unit_price = get_medicine_info(medicine_id)
        subtotal = float(unit_price) * qty

        add_sale_item(sale_id, medicine_id, qty, unit_price, subtotal)
        reduce_stock(branch_id, medicine_id, qty)

        # AI safety example rule
        if qty > 10:
            log_ai_warning(
                sale_id,
                medicine_id,
                "Unusually high quantity sold"
            )

    return {
        "message": "Sale completed",
        "sale_id": sale_id,
        "total_amount": total_amount
    }, 201