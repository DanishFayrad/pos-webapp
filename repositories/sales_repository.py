from extensions import get_db
from datetime import datetime

# ✅ CREATE SALE
def create_sale(branch_id, user_id, total_amount):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO sales (branch_id, performed_by, sale_date, total_amount)
        VALUES (%s, %s, %s, %s)
        RETURNING sale_id
    """, (branch_id, user_id, datetime.utcnow(), total_amount))

    sale_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return sale_id


# ✅ ADD SALE ITEM
def add_sale_item(sale_id, medicine_id, quantity, unit_price, subtotal):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO sale_items (sale_id, medicine_id, quantity, unit_price, subtotal)
        VALUES (%s, %s, %s, %s, %s)
    """, (sale_id, medicine_id, quantity, unit_price, subtotal))

    conn.commit()
    cur.close()
    conn.close()


# ✅ CHECK STOCK
def get_stock_quantity(branch_id, medicine_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT quantity
        FROM stock
        WHERE branch_id = %s AND medicine_id = %s
    """, (branch_id, medicine_id))

    row = cur.fetchone()
    cur.close()
    conn.close()
    return row[0] if row else 0


# ✅ REDUCE STOCK
def reduce_stock(branch_id, medicine_id, quantity):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        UPDATE stock
        SET quantity = quantity - %s,
            last_updated = CURRENT_TIMESTAMP
        WHERE branch_id = %s AND medicine_id = %s
    """, (quantity, branch_id, medicine_id))

    conn.commit()
    cur.close()
    conn.close()


# ✅ CHECK MEDICINE INFO
def get_medicine_info(medicine_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT requires_prescription, unit_price
        FROM medicines
        WHERE medicine_id = %s
    """, (medicine_id,))

    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


# ✅ LOG AI WARNING
def log_ai_warning(sale_id, medicine_id, message):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO ai_safety_logs (sale_id, medicine_id, warning_message)
        VALUES (%s, %s, %s)
    """, (sale_id, medicine_id, message))

    conn.commit()
    cur.close()
    conn.close()

    

# ✅ GET VALID (NON-EXPIRED) STOCK FROM BATCHES
def get_valid_batch_quantity(branch_id, medicine_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT COALESCE(SUM(quantity), 0)
        FROM stock_batches
        WHERE branch_id = %s
          AND medicine_id = %s
          AND (expiry_date IS NULL OR expiry_date >= CURRENT_DATE)
    """, (branch_id, medicine_id))

    qty = cur.fetchone()[0]

    cur.close()
    conn.close()
    return qty


# ✅ CHECK NEAR EXPIRY (for AI warning)
def check_near_expiry_batches(branch_id, medicine_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT COUNT(*)
        FROM stock_batches
        WHERE branch_id = %s
          AND medicine_id = %s
          AND expiry_date BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '30 days'
    """, (branch_id, medicine_id))

    count = cur.fetchone()[0]

    cur.close()
    conn.close()
    return count > 0