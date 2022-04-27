from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes

from cats import cats_blueprint
from users import users_blueprint
app.register_blueprint(cats_blueprint)
app.register_blueprint(users_blueprint)
