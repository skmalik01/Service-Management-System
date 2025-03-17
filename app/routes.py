from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.models import db, Customer, Technician, Enrollment
from app.schemas import CustomerSchema, TechnicianSchema, EnrollmentSchema
from app.auth import  role_required

main = Blueprint('main', __name__)

@main.route('/product', methods=['POST'])
@role_required("admin")
def add_product():
    try:
        claims = get_jwt() 
        current_user_id = get_jwt_identity()  
        
        if claims["role"] not in ["admin"]:
            return jsonify({"message": "Only admin can add product"}), 403
        
    except Exception as e:
        return jsonify({"error": f"Authentication error: {str(e)}"}), 401
    
    data = request.get_json()
    required_fields = ["first_name", "warranty_status", "warranty_duration", "purchased_date"]
    empty_fields = [field for field in required_fields if field not in data or not data[field].strip()]
    
    if empty_fields:
        return jsonify({"message": f"These fields cannot be empty: {', '.join(empty_fields)}"}), 400
    
    existing_product = Customer.query.filter_by(first_name=data["first_name"]).first()
    if existing_product:
        return jsonify({"message": "Email already exists. Please use a different email."}), 400
        
    new_product = Customer(
        first_name=data['first_name'],
        warranty_status=data['warranty_status'],
        warranty_duration=data["warranty_duration"],
        purchased_date=data['purchased_date']
    )
    
    db.session.add(new_product)
    db.session.commit()
    return jsonify(CustomerSchema().dump(new_product)), 201