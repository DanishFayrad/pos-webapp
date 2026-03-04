import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret")

    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", 5432)
    DB_NAME = os.getenv("DB_NAME", "pharmacy_management")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    SQLALCHEMY_DATABASE_URI= f"postgresql://postgres:amna7799@localhost:5432/pharmacy_management"


    SQLALCHEMY_TRACK_MODIFICATIONS = False

