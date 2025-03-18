from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(280), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin, customer, technician

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    purchase_date = db.Column(db.Date, nullable=False)
    warranty_duration = db.Column(db.Integer, nullable=False)  # in months

class RepairRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(50), default="Pending")  # Pending, In Progress, Completed
    cost_estimate = db.Column(db.Float, default=0.0)
    technician_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
