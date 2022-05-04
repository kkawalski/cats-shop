from base64 import b64encode, b64decode

from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.models import BaseModel

class User(BaseModel):
    __tablename__ = "users"
    
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))

    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password = generate_password_hash(password, method="sha256")

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_base64(self, password):
        return b64encode(f"{self.email}:{password}".encode())

    @classmethod
    def create_admin(cls, name, email, password):
        admin = cls(name=name, email=email, is_admin=True)
        admin.set_password(password)
        admin.save()
        return admin


    @classmethod
    def from_base64(cls, base64user):
        try:
            base64string = b64decode(base64user).decode()
            email, password = base64string.split(":")
            user = cls.query.filter_by(email=email).first()
            if not user or not user.check_password(password):
                return None
            return user
        except ValueError as e:
            return None


    def to_json(self):
        return {
            "name": self.name
        }

    def __repr__(self) -> str:
        return f"<User {self.name}>"
