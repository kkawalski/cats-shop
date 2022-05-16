from app import db
from app.models import BaseModel

from users.models import User


class Cat(BaseModel):
    __tablename__ = "cats"

    name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", backref=db.backref("cats", lazy=True))

    def to_json(self):
        return {
            "name": self.name
        }

    def __repr__(self) -> str:
        return f"<Cat {self.name}>"