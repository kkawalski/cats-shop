import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///index.db")
    SECRET_KEY = os.getenv("SECRET_KEY")
