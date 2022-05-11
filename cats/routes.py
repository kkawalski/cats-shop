from flask import Blueprint, jsonify, redirect, render_template, url_for
from flask_login import login_required

from cats.models import Cat
from cats.forms import CatForm

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

