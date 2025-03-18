# app/routes.py
from flask import request, jsonify
from app import app, db
from app.models import User, Product, RepairRequest
from app.controllers import check_warranty, submit_repair_request, register_user
from app.auth import role_required
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash

@app.route('/admin/register', methods=['POST'])
@jwt_required()
@role_required("admin")
def register():
    data = request.json
    return jsonify(register_user(data['username'], data['password'], data['role']))

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity={"id": user.id, "role": user.role})
    return jsonify({"access_token": access_token})

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
    data = request.json
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
    data = request.json
    repair_request = RepairRequest.query.get(request_id)
    if not repair_request:
        return jsonify({"error": "Repair request not found"}), 404

    repair_request.status = data['status']
    db.session.commit()
    return jsonify({"message": "Ticket status updated"})
