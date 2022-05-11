from flask_wtf import FlaskForm

from wtforms import EmailField, PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired, EqualTo, ValidationError

from users.models import User


class LoginForm(FlaskForm):
    email = EmailField(label="Email", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Sign In")


class RegisterForm(FlaskForm):
    email = EmailField(label="Email", validators=[DataRequired()])
    name = StringField(label="Email", validators=[DataRequired()])
    password1 = PasswordField(label="Password", 
                              validators=[DataRequired()])
    password2 = PasswordField(label="Re-enter password", 
                              validators=[DataRequired(), EqualTo("password1")])
    submit = SubmitField(label="Sign Up")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("This email already exists")