import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_ECHO'] = False
SECRET_KEY = os.environ.get('SECRET_KEY', "(\x81a\x9e\x1e\xd6'\xcc]\x8a<\xaa\x1d\xa2\xf2\xfc\xabM\x92U\xa1\xfa\xac\xc6")
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
api_bp = Blueprint('api', __name__)
api = Api(api_bp)
app.register_blueprint(api_bp, url_prefix='/api')
from api import route
