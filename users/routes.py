from flask import Blueprint, jsonify

from users.models import User

users_blueprint = Blueprint("users", __name__, url_prefix="/users", template_folder="templates")


@users_blueprint.route("/", methods=["GET"])
def cats_list():
    users = User.query.all()
    return jsonify([user.to_json() for user in users])
