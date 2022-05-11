from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, ValidationError
from wtforms.fields import StringField, SubmitField

from cats.models import Cat


class CatForm(FlaskForm):
    name = StringField(label="Name", validators=[DataRequired()])
    submit = SubmitField(label="Create")

    def validate_name(self, name):
        cat = Cat.query.filter_by(name=name.data).first()
        if cat is not None:
            raise ValidationError("Use another name")
