from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# -------------------- Branch --------------------
class Branch(db.Model):
    __tablename__ = 'branches'

    branch_id = db.Column(db.Integer, primary_key=True)
    branch_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255))
    phone = db.Column(db.String(20))


# -------------------- User --------------------
class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.branch_id'), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50))
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.Text, nullable=False)

# -------------------- Supplier --------------------
class Supplier(db.Model):
    __tablename__ = 'suppliers'

    supplier_id = db.Column(db.Integer, primary_key=True)
    supplier_name = db.Column(db.String(100), nullable=False)
    contact_person = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    address = db.Column(db.String(255))


# -------------------- Medicine --------------------
class Medicine(db.Model):
    __tablename__ = 'medicines'

    medicine_id = db.Column(db.Integer, primary_key=True)
    medicine_name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    requires_prescription = db.Column(db.Boolean, default=False)


# -------------------- Stock --------------------
class Stock(db.Model):
    __tablename__ = 'stock'

    stock_id = db.Column(db.Integer, primary_key=True)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.branch_id'), nullable=False)
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicines.medicine_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    expiry_date = db.Column(db.Date)

# -------------------- Sale --------------------
class Sale(db.Model):
    __tablename__ = 'sales'

    sale_id = db.Column(db.Integer, primary_key=True)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.branch_id'), nullable=False)
    performed_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    sale_date = db.Column(db.DateTime, default=datetime.utcnow)
    total_amount = db.Column(db.Numeric(12, 2))


# -------------------- Sale Item --------------------
class SaleItem(db.Model):
    __tablename__ = 'sale_items'

    sale_item_id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey('sales.sale_id', ondelete='CASCADE'), nullable=False)
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicines.medicine_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    subtotal = db.Column(db.Numeric(12, 2))


# -------------------- Payment --------------------
class Payment(db.Model):
    __tablename__ = 'payments'

    payment_id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey('sales.sale_id'))
    payment_method = db.Column(db.String(50))
    payment_status = db.Column(db.String(50))
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)


# -------------------- Prescription --------------------
class Prescription(db.Model):
    __tablename__ = 'prescriptions'

    prescription_id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey('sales.sale_id', ondelete='CASCADE'), nullable=False)
    patient_name = db.Column(db.String(100))
    doctor_name = db.Column(db.String(100))
    prescription_date = db.Column(db.Date)
    notes = db.Column(db.Text)


# -------------------- Purchase --------------------
class Purchase(db.Model):
    __tablename__ = 'purchases'

    purchase_id = db.Column(db.Integer, primary_key=True)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.branch_id'), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.supplier_id'), nullable=False)
    recorded_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    purchase_date = db.Column(db.DateTime, default=datetime.utcnow)
    total_amount = db.Column(db.Numeric(12, 2))


# -------------------- AI Safety Log --------------------
class AISafetyLog(db.Model):
    __tablename__ = 'ai_safety_logs'

    log_id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey('sales.sale_id'))
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicines.medicine_id'))
    warning_message = db.Column(db.Text)
    log_time = db.Column(db.DateTime, default=datetime.utcnow)


# -------------------- Stock Batches --------------------
class StockBatch(db.Model):
    __tablename__ = 'stock_batches'

    batch_id = db.Column(db.Integer, primary_key=True)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.branch_id'), nullable=False)
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicines.medicine_id'), nullable=False)
    batch_number = db.Column(db.String(50))
    quantity = db.Column(db.Integer, nullable=False)
    cost_price = db.Column(db.Numeric(10, 2), nullable=False)
    expiry_date = db.Column(db.Date)


# -------------------- Purchase Items --------------------
class PurchaseItem(db.Model):
    __tablename__ = 'purchase_items'

    purchase_item_id = db.Column(db.Integer, primary_key=True)
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchases.purchase_id', ondelete='CASCADE'), nullable=False)
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicines.medicine_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    cost_price = db.Column(db.Numeric(10, 2))