import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5000").split(",")
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "!@?Sup€rS€cretK€y?@!")
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', SECRET_KEY)

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", "False").lower() == "true"

    MAX_LOGIN_ATTEMPTS = int(os.getenv("MAX_LOGIN_ATTEMPTS", 5))
    LOCKOUT_DURATION_MINUTES = int(os.getenv("LOCKOUT_DURATION_MINUTES", 20))
