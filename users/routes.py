from flask import Blueprint, jsonify, redirect, render_template, request, url_for

from users.models import User

users_blueprint = Blueprint("users", __name__, url_prefix="/users", template_folder="templates")


@users_blueprint.route("/", methods=["GET"])
def users_list():
    users = User.query.all()
    return jsonify([user.to_json() for user in users])


@users_blueprint.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    if request.method == "POST":
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        name = request.form.get("name", "")

        user = User.query.filter(User.email == email).first()
        if user:
            return redirect(url_for("users.signup"))

        if password1 != password2:
            return redirect(url_for("users.signup"))

        user = User(name=name, email=email)
        user.set_password(password1)
        user.save()
        return redirect(url_for("users.login"))


@users_blueprint.route("/login", methods=["GET", "POST"])
def login():
    return "login"