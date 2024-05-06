# 3rd-part packages
from flask import Flask
from flask_mongoengine import MongoEngine
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
)
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename


import os
from flask import send_from_directory

# app = Flask(__name__)
# @app.errorhandler(404)
# def custom_404(e):
#     return render_template("404.html"), 404

# for spotify API
# CLIENT_ID = "9ae0c155811a4e77bd42962005ff53fd"
# CLIENT_SECRET = "cd53d4d5f41c497e979cbdfd8c459371"

# local
from .client import SpotifyAPI

# 
db = MongoEngine()
login_manager = LoginManager()
bcrypt = Bcrypt()
spotify_client = SpotifyAPI()

from .users.routes import users
from .main.routes import main

def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_pyfile("config.py", silent=False)
    if test_config is not None:
        app.config.update(test_config)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(main)
    app.register_blueprint(users)

    return app