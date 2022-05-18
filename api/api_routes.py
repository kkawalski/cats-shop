from flask import request
from flask_restx import Resource

from app import api
from api.rest_models import model, cat_model, user_model
from cats.models import Cat
from cats.shemas import cat_schema
from users.models import User



@api.route('/api/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

    def post(self):
        return {"ping": "pong"}


class TodoDao(object):
    def __init__(self, todo_id, task):
        self.todo_id = todo_id
        self.task = task

        # This field will not be sent in the response
        self.status = 'active'

@api.route('/api/todo')
class Todo(Resource):
    @api.marshal_with(model)
    def get(self, **kwargs):
        return TodoDao(todo_id='my_todo', task='Remember the milk')


@api.route("/api/cats")
class CatLoist(Resource):
    @api.marshal_with(cat_model)
    def get(self, **kwargs):
        return Cat.query.all()

    @api.expect([cat_model])
    @api.marshal_with(cat_model)
    def post(self, *args, **kwargs):
        print("ARGS", args)
        print("KWARGS", kwargs)
        json_data = request.json
        cats_data = cat_schema.load(json_data)
        cat = Cat(**cats_data).save()
        return cat, 201
        

@api.route("/api/users/<int:user_id>")
class UserDetail(Resource):
    @api.marshal_with(user_model)
    def get(self, user_id, *args, **kwargs):
        return User.query.get(user_id)

