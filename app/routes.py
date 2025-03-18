from datetime import datetime
from flask import request, jsonify, make_response
from app import app, db
from app.models import User, Product, RepairRequest
from app.controllers import check_warranty, submit_repair_request, register_user, login_user, logout_user
from app.auth import role_required
from flask_jwt_extended import jwt_required, get_jwt_identity


@app.route('/admin/register', methods=['POST'])
@jwt_required()
@role_required("admin")
def register():
    data = request.get_json()
    return jsonify(register_user(data['username'], data['password'], data['role']))


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    response = login_user(data['username'], data['password'])
    return response  


@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    response = logout_user()
    return response  

@app.route('/add-product', methods=['POST'])
@jwt_required()
@role_required("admin")
def add_product():
    data = request.get_json()

    new_product = Product(
        name=data['name'],
        purchase_date=datetime.strptime(data['purchase_date'], "%Y-%m-%d").date(),
        warranty_duration=data['warranty_duration']
    )

    db.session.add(new_product)
    db.session.commit()

    return jsonify({"message": "Product added successfully!", "product_id": new_product.id}), 201


@app.route('/warranty-status/<int:product_id>', methods=['GET', 'POST'])
@jwt_required()
@role_required("customer")
def warranty_status(product_id):
    return jsonify(check_warranty(product_id))


@app.route('/submit-repair-request', methods=['POST'])
@jwt_required()
@role_required("customer")
def submit_request():
    user = get_jwt_identity()
    data = request.get_json()
    return jsonify(submit_repair_request(data['product_id'], user['id']))


@app.route('/repair-requests', methods=['GET'])
@jwt_required()
@role_required("admin")
def get_repair_requests():
    requests = RepairRequest.query.all()
    return jsonify([{"id": req.id, "status": req.status} for req in requests])


@app.route('/update-ticket-status/<int:request_id>', methods=['POST'])
@jwt_required()
@role_required("technician")
def update_ticket_status(request_id):
    data = request.get_json()
    repair_request = RepairRequest.query.get(request_id)
    if not repair_request:
        return jsonify({"error": "Repair request not found"}), 404

    repair_request.status = data['status']
    db.session.commit()
    return jsonify({"message": "Ticket status updated"})
