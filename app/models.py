from abc import ABC, abstractmethod
from sqlalchemy import func
from sqlalchemy.dialects.sqlite import DATETIME

from app import db


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(DATETIME, server_default=func.now())
    
    def to_json(self):
        pass

