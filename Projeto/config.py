import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "chave-secreta"
    SQLALCHEMY_DATABASE_URI = "sqlite:///fintrack.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
