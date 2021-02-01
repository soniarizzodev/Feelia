"""
The flask application package.
"""
import os
from flask import Flask
from flask import request
from flask_login import LoginManager
from flask_babel import Babel
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
login = LoginManager(app)
babel = Babel(app)

app.secret_key = os.urandom(24)

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'])

import webapp.routes
