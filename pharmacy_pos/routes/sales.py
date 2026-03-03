from flask import Blueprint, request, jsonify
from datetime import datetime
from models import db, Sale, SaleItem, Stock, Medicine, Payment, AISafetyLog, Prescription
from services.billing_service import calculate_total
from services.safety_service import run_safety_checks
from sqlalchemy import func

sales_bp = Blueprint('sales', __name__)


@sales_bp.route('/sale/create', methods=['POST'])
def create_sale():
    try:
        data = request.get_json()

        branch_id = data.get('branch_id')
        user_id = data.get('user_id')
        cart = data.get('cart')
        payment_method = data.get('payment_method')
        prescription_data = data.get('prescription')

        # -----------------------------
        # Basic Validations
        # -----------------------------
        if not branch_id or not user_id or not payment_method:
            return jsonify({
                "status": "error",
                "message": "Missing required fields."
            }), 400

        if not cart or len(cart) == 0:
            return jsonify({
                "status": "error",
                "message": "Cart cannot be empty."
            }), 400

        items_for_billing = []
        safety_warnings = []

        # -----------------------------
        # Step 1 — Validate Cart Items
        # -----------------------------
        for item in cart:
            medicine_id = item.get('medicine_id')
            quantity = item.get('quantity')

            medicine = Medicine.query.get(medicine_id)
            if not medicine:
                return jsonify({
                    "status": "error",
                    "message": f"Medicine ID {medicine_id} not found."
                }), 404

            stock = Stock.query.filter_by(
                medicine_id=medicine_id,
                branch_id=branch_id
            ).first()

            if not stock:
                return jsonify({
                    "status": "error",
                    "message": "Stock record not found for this branch."
                }), 404

            # Prescription check
            if medicine.requires_prescription and not prescription_data:
                return jsonify({
                    "status": "error",
                    "message": f"{medicine.medicine_name} requires a prescription. Please provide prescription details."
                }), 400

            # Run AI Safety Checks
            warnings = run_safety_checks(medicine, stock, quantity)

            if warnings:
                safety_warnings.append({
                    "medicine": medicine.medicine_name,
                    "warnings": warnings
                })

                for warning in warnings:
                    log = AISafetyLog(
                        sale_id=None,
                        medicine_id=medicine.medicine_id,
                        warning_message=warning,
                        log_time=datetime.now()
                    )
                    db.session.add(log)

                continue

            # Add for billing
            items_for_billing.append({
                "medicine_id": medicine.medicine_id,
                "unit_price": float(medicine.unit_price),
                "quantity": quantity
            })

        # -----------------------------
        # If warnings exist → Block Sale
        # -----------------------------
        if safety_warnings:
            db.session.commit()
            return jsonify({
                "status": "blocked",
                "warnings": safety_warnings
            }), 400

        # -----------------------------
        # Step 2 — Calculate Total
        # -----------------------------
        billing_data = calculate_total(items_for_billing)

        # -----------------------------
        # Step 3 — Create Sale
        # -----------------------------
        new_sale = Sale(
            branch_id=branch_id,
            performed_by=user_id,
            sale_date=datetime.now(),
            total_amount=billing_data["total"]
        )
        db.session.add(new_sale)
        db.session.flush()

        # -----------------------------
        # Step 4 — Save Sale Items & Deduct Stock
        # -----------------------------
        for item in items_for_billing:
            subtotal = item["unit_price"] * item["quantity"]

            sale_item = SaleItem(
                sale_id=new_sale.sale_id,
                medicine_id=item["medicine_id"],
                quantity=item["quantity"],
                unit_price=item["unit_price"],
                subtotal=subtotal
            )
            db.session.add(sale_item)

            stock = Stock.query.filter_by(
                medicine_id=item["medicine_id"],
                branch_id=branch_id
            ).first()

            if stock.quantity < item["quantity"]:
                raise Exception("Stock inconsistency detected.")

            stock.quantity -= item["quantity"]

        # -----------------------------
        # Step 5 — Save Payment
        # -----------------------------
        payment = Payment(
            sale_id=new_sale.sale_id,
            payment_method=payment_method,
            payment_status="completed",
            payment_date=datetime.now()
        )
        db.session.add(payment)

        # -----------------------------
        # Step 6 — Save Prescription
        # -----------------------------
        has_prescription_medicine = any(
            Medicine.query.get(item["medicine_id"]).requires_prescription
            for item in items_for_billing
        )

        if has_prescription_medicine and prescription_data:
            prescription = Prescription(
                sale_id=new_sale.sale_id,
                patient_name=prescription_data.get('patient_name'),
                doctor_name=prescription_data.get('doctor_name'),
                prescription_date=prescription_data.get('prescription_date'),
                notes=prescription_data.get('notes')
            )
            db.session.add(prescription)

        # -----------------------------
        # Commit Transaction
        # -----------------------------
        db.session.commit()

        # -----------------------------
        # Invoice Structure
        # -----------------------------
        invoice = {
            "sale_id": new_sale.sale_id,
            "date": new_sale.sale_date,
            "items": items_for_billing,
            "subtotal": billing_data["subtotal"],
            "tax": billing_data["tax"],
            "total": billing_data["total"],
            "payment_method": payment_method
        }

        return jsonify({
            "status": "success",
            "sale_id": new_sale.sale_id,
            "invoice": invoice,
            "message": "Thank you for shopping with us!"
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ─────────────────────────────────────────
# 2️⃣ Sale Details API
# ─────────────────────────────────────────
@sales_bp.route('/sale/<int:sale_id>', methods=['GET'])
def get_sale_details(sale_id):
    try:
        sale = Sale.query.get(sale_id)

        if not sale:
            return jsonify({
                "status": "error",
                "message": f"Sale ID {sale_id} not found."
            }), 404

        sale_items = SaleItem.query.filter_by(sale_id=sale_id).all()

        items = []
        for item in sale_items:
            medicine = Medicine.query.get(item.medicine_id)
            items.append({
                "medicine_name": medicine.medicine_name,
                "quantity": item.quantity,
                "unit_price": float(item.unit_price),
                "subtotal": float(item.subtotal)
            })

        payment = Payment.query.filter_by(sale_id=sale_id).first()

        return jsonify({
            "status": "success",
            "sale_id": sale.sale_id,
            "branch_id": sale.branch_id,
            "performed_by": sale.performed_by,
            "sale_date": str(sale.sale_date),
            "total_amount": float(sale.total_amount),
            "items": items,
            "payment": {
                "method": payment.payment_method if payment else None,
                "status": payment.payment_status if payment else None,
                "date": str(payment.payment_date) if payment else None
            }
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ─────────────────────────────────────────
# 3️⃣ Sales History — Date Wise
# ─────────────────────────────────────────
@sales_bp.route('/sales/history/date', methods=['GET'])
def sales_history_by_date():
    try:
        date_str = request.args.get('date')

        if not date_str:
            return jsonify({
                "status": "error",
                "message": "Please provide date. Example: /sales/history/date?date=2026-02-26"
            }), 400

        filter_date = datetime.strptime(date_str, '%Y-%m-%d').date()

        sales = Sale.query.filter(
            func.date(Sale.sale_date) == filter_date
        ).all()

        data = [{
            "sale_id": s.sale_id,
            "branch_id": s.branch_id,
            "performed_by": s.performed_by,
            "sale_date": str(s.sale_date),
            "total_amount": float(s.total_amount)
        } for s in sales]

        return jsonify({
            "status": "success",
            "date": date_str,
            "total_sales": len(data),
            "sales": data
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ─────────────────────────────────────────
# 4️⃣ Sales History — Branch Wise
# ─────────────────────────────────────────
@sales_bp.route('/sales/history/branch', methods=['GET'])
def sales_history_by_branch():
    try:
        branch_id = request.args.get('branch_id')

        if not branch_id:
            return jsonify({
                "status": "error",
                "message": "Please provide branch_id. Example: /sales/history/branch?branch_id=1"
            }), 400

        sales = Sale.query.filter_by(branch_id=int(branch_id)).all()

        data = [{
            "sale_id": s.sale_id,
            "branch_id": s.branch_id,
            "performed_by": s.performed_by,
            "sale_date": str(s.sale_date),
            "total_amount": float(s.total_amount)
        } for s in sales]

        return jsonify({
            "status": "success",
            "branch_id": branch_id,
            "total_sales": len(data),
            "sales": data
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ─────────────────────────────────────────
# 5️⃣ Sales History — Cashier Wise
# ─────────────────────────────────────────
@sales_bp.route('/sales/history/cashier', methods=['GET'])
def sales_history_by_cashier():
    try:
        user_id = request.args.get('user_id')

        if not user_id:
            return jsonify({
                "status": "error",
                "message": "Please provide user_id. Example: /sales/history/cashier?user_id=1"
            }), 400

        sales = Sale.query.filter_by(performed_by=int(user_id)).all()

        data = [{
            "sale_id": s.sale_id,
            "branch_id": s.branch_id,
            "performed_by": s.performed_by,
            "sale_date": str(s.sale_date),
            "total_amount": float(s.total_amount)
        } for s in sales]

        return jsonify({
            "status": "success",
            "user_id": user_id,
            "total_sales": len(data),
            "sales": data
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500