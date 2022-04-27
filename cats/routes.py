from flask import Blueprint, jsonify

from cats.models import Cat

cats_blueprint = Blueprint("cats", __name__, url_prefix="/cats")


@cats_blueprint.route("/", methods=["GET"])
def cats_list():
    cats = Cat.query.all()
    return jsonify([cat.to_json() for cat in cats])
