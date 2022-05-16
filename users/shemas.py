from marshmallow import fields
from marshmallow.validate import Length

from app import ma
from users.models import User

from cats.shemas import cats_schema


class UserListSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

user_list_schema = UserListSchema()
users_list_schema = UserListSchema(many=True)


class UserRetrieveSchema(ma.SQLAlchemyAutoSchema):
    cats = ma.Nested(cats_schema)
    class Meta:
        model = User

user_retrieve_schema = UserRetrieveSchema()
users_retrieve_schema = UserRetrieveSchema(many=True)
