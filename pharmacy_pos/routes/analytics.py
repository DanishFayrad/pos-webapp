from flask import Blueprint, jsonify
from models import db, Sale, SaleItem, Medicine, AISafetyLog
from sqlalchemy import func
from datetime import date, timedelta

analytics_bp = Blueprint('analytics', __name__)


# ─────────────────────────────────────────
# 1️⃣ Total Revenue (All Time)
# ─────────────────────────────────────────
@analytics_bp.route('/analytics/total-revenue', methods=['GET'])
def total_revenue():
    revenue = db.session.query(
        func.sum(Sale.total_amount)
    ).scalar() or 0

    return jsonify({
        "total_revenue_all_time": float(revenue)
    })


# ─────────────────────────────────────────
# 2️⃣ Total Sales Count
# ─────────────────────────────────────────
@analytics_bp.route('/analytics/total-sales-count', methods=['GET'])
def total_sales_count():
    count = db.session.query(
        func.count(Sale.sale_id)
    ).scalar()

    return jsonify({
        "total_sales_count": count
    })


# ─────────────────────────────────────────
# 3️⃣ Most Sold Medicine
# ─────────────────────────────────────────
@analytics_bp.route('/analytics/most-sold-medicine', methods=['GET'])
def most_sold_medicine():
    result = db.session.query(
        Medicine.medicine_name,
        func.sum(SaleItem.quantity).label('total_sold')
    ).join(SaleItem, SaleItem.medicine_id == Medicine.medicine_id
    ).group_by(Medicine.medicine_name
    ).order_by(func.sum(SaleItem.quantity).desc()
    ).first()

    if not result:
        return jsonify({"message": "No sales data found"}), 404

    return jsonify({
        "most_sold_medicine": result.medicine_name,
        "total_sold": result.total_sold
    })


# ─────────────────────────────────────────
# 4️⃣ Prescription Medicine %
# ─────────────────────────────────────────
@analytics_bp.route('/analytics/prescription-percentage', methods=['GET'])
def prescription_percentage():
    total = db.session.query(
        func.count(SaleItem.sale_item_id)
    ).scalar() or 0

    prescription = db.session.query(
        func.count(SaleItem.sale_item_id)
    ).join(Medicine, Medicine.medicine_id == SaleItem.medicine_id
    ).filter(Medicine.requires_prescription == True).scalar() or 0

    percentage = (prescription / total * 100) if total > 0 else 0

    return jsonify({
        "total_items_sold": total,
        "prescription_items_sold": prescription,
        "prescription_percentage": round(percentage, 2)
    })


# ─────────────────────────────────────────
# 5️⃣ AI Warnings Frequency
# ─────────────────────────────────────────
@analytics_bp.route('/analytics/ai-warnings', methods=['GET'])
def ai_warnings_frequency():
    total_warnings = db.session.query(
        func.count(AISafetyLog.log_id)
    ).scalar()

    top_warnings = db.session.query(
        AISafetyLog.warning_message,
        func.count(AISafetyLog.log_id).label('frequency')
    ).group_by(AISafetyLog.warning_message
    ).order_by(func.count(AISafetyLog.log_id).desc()
    ).all()

    data = [{"warning": w.warning_message, "frequency": w.frequency} for w in top_warnings]

    return jsonify({
        "total_warnings": total_warnings,
        "warnings_breakdown": data
    })


# ─────────────────────────────────────────
# 6️⃣ Last 7 Days Sales Trend
# ─────────────────────────────────────────
@analytics_bp.route('/analytics/weekly-trend', methods=['GET'])
def weekly_trend():
    today = date.today()
    seven_days_ago = today - timedelta(days=7)

    results = db.session.query(
        func.date(Sale.sale_date).label('sale_day'),
        func.sum(Sale.total_amount).label('daily_revenue'),
        func.count(Sale.sale_id).label('daily_transactions')
    ).filter(
        Sale.sale_date >= seven_days_ago
    ).group_by(
        func.date(Sale.sale_date)
    ).order_by(
        func.date(Sale.sale_date)
    ).all()

    data = [{
        "date": str(r.sale_day),
        "revenue": float(r.daily_revenue),
        "transactions": r.daily_transactions
    } for r in results]

    return jsonify({
        "last_7_days_trend": data
    })
