import os

class Config:
    SECRET_KEY = "mine_secret_system_key"
    JWT_SECRET_KEY = "mine_malik_shaikh_jwt_secret_key"  
    JWT_ALGORITHM = "HS256"
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:malik0112@localhost:5111/service_system"
    JWT_TOKEN_LOCATION = ["cookies"]  
    JWT_COOKIE_SECURE = False 
    JWT_COOKIE_HTTPONLY = True  
    JWT_COOKIE_CSRF_PROTECT = False  