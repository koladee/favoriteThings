import os
from flask import Flask


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY = os.environ.get('SECRET_KEY', "(\x81a\x9e\x1e\xd6'\xcc]\x8a<\xaa\x1d\xa2\xf2\xfc\xabM\x92U\xa1\xfa\xac\xc6")
app.config['SECRET_KEY'] = SECRET_KEY

from favorite_things import route