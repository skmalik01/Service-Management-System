from datetime import datetime
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    warranty_status = db.Column(db.String(100), nullable=False)
    warranty_duration = db.Column(db.String(100), unique=True, nullable=False)
    purchased_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, first_name, warranty_status, warranty_duration):
        self.first_name = first_name
        self.warranty_status = warranty_status
        self.warranty_duration = warranty_duration

class Technician(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    in_progress = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, first_name, in_progress, completed):
        self.first_name = first_name
        self.in_progress = in_progress
        self.completed = completed

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    technician_id = db.Column(db.Integer, db.ForeignKey('technician.id'), nullable=False)

    customer = db.relationship('Customer', backref=db.backref('enrollments', lazy=True))
    technician = db.relationship('Technician', backref=db.backref('enrollments', lazy=True))

    def __init__(self, customer_id, technician_id):
        self.customer_id = customer_id
        self.technician_id = technician_id

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)