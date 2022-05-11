from sqlalchemy import func

from app import db


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, server_default=func.now())
    
    def to_json(self):
        pass

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

