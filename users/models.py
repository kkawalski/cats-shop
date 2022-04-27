from app import db
from app.models import BaseModel

class User(BaseModel):
    __tablename__ = "users"
    
    name = db.Column(db.String(50), nullable=False)

    def to_json(self):
        return {
            "name": self.name
        }

    def __repr__(self) -> str:
        return f"<User {self.name}>"
