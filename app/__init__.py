from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:malik0112@localhost:5000/service_system'
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['JWT_SECRET_KEY'] = 'jwtsecretkey'
app.config['JWT_TOKEN_LOCATION'] = ['cookies']  
app.config['JWT_COOKIE_SECURE'] = False  
app.config['JWT_COOKIE_CSRF_PROTECT'] = False 
app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token'

db = SQLAlchemy(app)
jwt = JWTManager(app)

from app import routes

with app.app_context():
    db.create_all()
