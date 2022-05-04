from functools import wraps

from flask import Blueprint, flash, jsonify, make_response, redirect, render_template, request, url_for

from users.models import User

users_blueprint = Blueprint("users", __name__, url_prefix="/users", template_folder="templates")


def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_cookie = request.cookies.get("auth", "")
        user = User.from_base64(auth_cookie)
        if not user:
            return redirect(url_for("users.login"))
        request.my_user = user
        return func(*args, **kwargs)
    return wrapper

def authorize(func):
    @authenticate
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = request.my_user
        if not user.is_admin:
            return jsonify(""), 403
        return func(*args, **kwargs)
    return wrapper



@users_blueprint.route("/", methods=["GET"])
@authorize
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
            flash("User exist")
            return redirect(url_for("users.signup"))

        if password1 != password2:
            flash("Passwords dont match")
            return redirect(url_for("users.signup"))

        user = User(name=name, email=email)
        user.set_password(password1)
        user.save()
        return redirect(url_for("users.login"))


@users_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if not user:
            return redirect(url_for("users.login"))
        
        if not user.check_password(password):
            return redirect(url_for("users.login"))

        base64user = user.to_base64(password)

        res = make_response(redirect(url_for("users.profile")))
        res.set_cookie("auth", base64user)
        return res
        
@users_blueprint.route("/logout", methods=["GET"])
def logout():
    res = make_response(redirect(url_for("users.login")))
    res.delete_cookie("auth")
    return res


@users_blueprint.route("/profile", methods=["GET"])
@authenticate
def profile():
    print("CURRENT_USER", request.my_user)
    res = make_response(render_template("profile.html", user=request.my_user))
    return res
    
