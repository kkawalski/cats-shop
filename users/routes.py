from functools import wraps

from flask import Blueprint, flash, jsonify, make_response, redirect, render_template, request, url_for
from flask_login import login_user, logout_user

from app import login_manager
from users.models import User
from users.forms import LoginForm, RegisterForm

users_blueprint = Blueprint("users", __name__, url_prefix="/users", template_folder="templates")


@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()


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


@users_blueprint.route("/login_cookie", methods=["GET", "POST"])
def login_cookie():
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
        
@users_blueprint.route("/logout_cookie", methods=["GET"])
def logout_cookie():
    res = make_response(redirect(url_for("users.login")))
    res.delete_cookie("auth")
    return res


@users_blueprint.route("/profile_cookie", methods=["GET"])
@authenticate
def profile():
    print("CURRENT_USER", request.my_user)
    res = make_response(render_template("profile.html", user=request.my_user))
    return res


@users_blueprint.route("login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("users.login"))
        login_user(user)
        return redirect(url_for("cats.cats_list"))
    return render_template("login.html", form=form)


@users_blueprint.route("logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for("users.login"))
    

@users_blueprint.route("register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password1.data)
        user.save()
        return redirect(url_for("users.login"))
    return render_template("register.html", form=form)
