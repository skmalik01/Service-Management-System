from flask import jsonify, make_response
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies
from app.models import User, Product, RepairRequest, db
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

def check_warranty(product_id):
    product = Product.query.get(product_id)
    if not product:
        return {"error": "Product not found"}, 404

    warranty_end_date = product.purchase_date + timedelta(days=product.warranty_duration * 30)
    return {"status": "Valid" if datetime.today().date() <= warranty_end_date else "Expired"}

def submit_repair_request(product_id, customer_id):
    product = Product.query.get(product_id)
    if not product:
        return {"error": "Product not found"}, 404

    request = RepairRequest(product_id=product.id, customer_id=customer_id)
    db.session.add(request)
    db.session.commit()
    return {"message": "Repair request submitted", "request_id": request.id}

def register_user(username, password, role):
    if role not in ["admin", "customer", "technician"]:
        return {"error": "Invalid role"}, 400

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password, role=role)
    db.session.add(new_user)
    db.session.commit()
    return {"message": f"{role.capitalize()} registered successfully"}

def login_user(username, password):
    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=str(user.id), additional_claims={"role": user.role})

    response = make_response(jsonify({"message": "Login successful"}))
    set_access_cookies(response, access_token)  
    return response

def logout_user():
    response = make_response(jsonify({"message": "Logged out successfully"}))
    unset_jwt_cookies(response)  
    return response
