import os

from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app():

    dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    load_dotenv(dotenv_path)

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['CSRF_SESSION_KEY'] = os.environ.get('CSRF_SESSION_KEY')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

    db.init_app(app)

    from app.controllers import base as base_module
    app.register_blueprint(base_module)

    Migrate(app, db)

    return app


from app import models
