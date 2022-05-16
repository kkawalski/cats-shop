import datetime
import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///index.db")
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=1)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(minutes=15)
    JWT_IDENTITY_CLAIM = "id"
    # JWT_HEADER_TYPE = "JWT"