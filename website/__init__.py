from os import path
from flask import Flask
import os
from flask_login import LoginManager

# Try to import Flask-SQLAlchemy; make it optional so app still runs if package is missing.
try:
    from flask_sqlalchemy import SQLAlchemy
    db = SQLAlchemy()
except Exception:
    db = None

DB_NAME = "database.db"

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    # ensure SECRET_KEY is set so flash() (which uses the session) works
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret')

    # initialize db only if Flask-SQLAlchemy is installed
    if db is not None:
        # configure a default sqlite database if one isn't set
        # use an absolute path to avoid issues with working directory and spaces
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.db')
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        app.config.setdefault('SQLALCHEMY_DATABASE_URI', f"sqlite:///{db_path}")
        app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
        db.init_app(app)

        # import models so SQLAlchemy registers the metadata, then create tables
        with app.app_context():
            from . import models  # registers model classes
            db.create_all()

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # initialize login manager with the app (do not call init_app at module import time)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Database created!')

@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(int(user_id))