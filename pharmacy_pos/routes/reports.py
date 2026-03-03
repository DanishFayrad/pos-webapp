from flask import Blueprint, jsonify, request
from models import db, Sale, SaleItem, Medicine, Stock
from sqlalchemy import func
from datetime import datetime, date, timedelta

reports_bp = Blueprint('reports', __name__)

# ─────────────────────────────────────────
# 1️⃣ Daily Sales Report
# ─────────────────────────────────────────
@reports_bp.route('/reports/daily-sales', methods=['GET'])
def daily_sales_report():
    today = date.today()

    total_sales = db.session.query(
        func.sum(Sale.total_amount)
    ).filter(
        func.date(Sale.sale_date) == today
    ).scalar() or 0

    total_transactions = db.session.query(
        func.count(Sale.sale_id)
    ).filter(
        func.date(Sale.sale_date) == today
    ).scalar()

    return jsonify({
        "date": str(today),
        "total_sales": float(total_sales),
        "total_transactions": total_transactions
    })


# ─────────────────────────────────────────
# 2️⃣ Monthly Sales Report
# ─────────────────────────────────────────
@reports_bp.route('/reports/monthly-sales', methods=['GET'])
def monthly_sales_report():
    today = date.today()

    total_sales = db.session.query(
        func.sum(Sale.total_amount)
    ).filter(
        func.extract('month', Sale.sale_date) == today.month,
        func.extract('year', Sale.sale_date) == today.year
    ).scalar() or 0

    total_transactions = db.session.query(
        func.count(Sale.sale_id)
    ).filter(
        func.extract('month', Sale.sale_date) == today.month,
        func.extract('year', Sale.sale_date) == today.year
    ).scalar()

    return jsonify({
        "month": today.month,
        "year": today.year,
        "total_sales": float(total_sales),
        "total_transactions": total_transactions
    })


# ─────────────────────────────────────────
# 3️⃣ Top Selling Medicines
# ─────────────────────────────────────────
@reports_bp.route('/reports/top-medicines', methods=['GET'])
def top_medicines():
    results = db.session.query(
        Medicine.medicine_name,
        func.sum(SaleItem.quantity).label('total_sold')
    ).join(SaleItem, SaleItem.medicine_id == Medicine.medicine_id
    ).group_by(Medicine.medicine_name
    ).order_by(func.sum(SaleItem.quantity).desc()
    ).limit(10).all()

    data = [{"medicine": r.medicine_name, "total_sold": r.total_sold} for r in results]

    return jsonify({"top_medicines": data})


# ─────────────────────────────────────────
# 4️⃣ Low Stock Report
# ─────────────────────────────────────────
@reports_bp.route('/reports/low-stock', methods=['GET'])
def low_stock_report():
    results = db.session.query(
        Medicine.medicine_name,
        Stock.quantity,
        Stock.branch_id
    ).join(Stock, Stock.medicine_id == Medicine.medicine_id
    ).filter(Stock.quantity < 10).all()

    data = [{"medicine": r.medicine_name, "quantity": r.quantity, "branch_id": r.branch_id} for r in results]

    return jsonify({"low_stock_medicines": data})


# ─────────────────────────────────────────
# 5️⃣ Expiry Report (30 days)
# ─────────────────────────────────────────
@reports_bp.route('/reports/expiry', methods=['GET'])
def expiry_report():
    today = date.today()
    next_30_days = today + timedelta(days=30)

    results = db.session.query(
        Medicine.medicine_name,
        Stock.expiry_date,
        Stock.quantity,
        Stock.branch_id
    ).join(Stock, Stock.medicine_id == Medicine.medicine_id
    ).filter(
        Stock.expiry_date != None,
        Stock.expiry_date <= next_30_days,
        Stock.expiry_date >= today
    ).all()

    data = [{"medicine": r.medicine_name, "expiry_date": str(r.expiry_date), "quantity": r.quantity, "branch_id": r.branch_id} for r in results]

    return jsonify({"expiring_medicines": data})


# ─────────────────────────────────────────
# 6️⃣ Revenue by Branch
# ─────────────────────────────────────────
@reports_bp.route('/reports/revenue-by-branch', methods=['GET'])
def revenue_by_branch():
    results = db.session.query(
        Sale.branch_id,
        func.sum(Sale.total_amount).label('total_revenue'),
        func.count(Sale.sale_id).label('total_sales')
    ).group_by(Sale.branch_id).all()

    data = [{"branch_id": r.branch_id, "total_revenue": float(r.total_revenue), "total_sales": r.total_sales} for r in results]

    return jsonify({"revenue_by_branch": data})
