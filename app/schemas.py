from marshmallow import Schema, fields

class CustomerSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    warranty_status = fields.Str(required=True)
    warranty_duration = fields.Str(unique=True, required=True)

class TechnicianSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    in_progress = fields.Str(required=True)
    completed = fields.Str(unique=True)

class EnrollmentSchema(Schema):
    id = fields.Int(dump_only=True)
    customer_id = fields.Int(required=True)
    technician_id = fields.Int(required=True)

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    role = fields.Str(required=True)