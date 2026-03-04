import psycopg2
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from config import Config

jwt = JWTManager()
db = SQLAlchemy()  # <-- add this for models

def get_db():
    """Direct psycopg2 connection (used for raw SQL queries)"""
    conn = psycopg2.connect(
        host=Config.DB_HOST,
        database=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        port=Config.DB_PORT
    )
    return conn