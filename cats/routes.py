from flask import Blueprint, jsonify, redirect, render_template, url_for, request
from flask_login import login_required
from flask_jwt_extended import jwt_required
from marshmallow.exceptions import ValidationError

from cats.models import Cat
from cats.forms import CatForm
from cats.shemas import CatShema, cat_schema, cats_schema, cat_model_schema, cats_model_schema

cats_blueprint = Blueprint("cats", __name__, url_prefix="/cats", template_folder="templates")


@cats_blueprint.route("/", methods=["GET", "POST"])
@login_required
def cats_list():
    cats = Cat.query.all()
    form = CatForm()
    if form.validate_on_submit():
        cat = Cat(name=form.name.data).save()
        return redirect(url_for("cats.cats_list"))
    return render_template("cats.html", form=form, cats=cats)


@cats_blueprint.route("/api", methods=["GET", "POST"])
# @jwt_required()
def cats_list_api():
    if request.method == "GET":
        cats = Cat.query.all()
        return jsonify(cats_model_schema.dump(cats))
    if request.method == "POST":
        try:
            json_data = request.get_json()
            cats_data = cat_schema.load(json_data)
            print("CATS DATA")
            cat = Cat(**cats_data).save()
            return cat_schema.jsonify(cat)
        except ValidationError as e:
            return jsonify(e.normalized_messages())


