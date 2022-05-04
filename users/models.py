from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.models import BaseModel

class User(BaseModel):
    __tablename__ = "users"
    
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def set_password(self, password):
        self.password = generate_password_hash(password, method="sha256")

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_json(self):
        return {
            "name": self.name
        }

    def __repr__(self) -> str:
        return f"<User {self.name}>"
