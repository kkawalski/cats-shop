from flask_restx import fields
from sqlalchemy import Integer

from app import api

model = api.model('TodoModel', {
    'task': fields.String,
    'uri': fields.Url('hello_world'),
    'status': fields.String,
})

user_model = api.model("UserModel", {
    "id": fields.Integer,
    "name": fields.String,
    "email": fields.String,
})

cat_model = api.model("CatModel", {
    "id": fields.Integer,
    "name": fields.String,
    "user": fields.Nested(user_model),
})
