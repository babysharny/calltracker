from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from config import basedir
import os
# from flask.ext.flaskcolor import Color
# from flask.ext.color
# from flask.ext.color 
from flaskext import color

from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object('config')
color.init_app(app)


lm = LoginManager()
lm.init_app(app)
lm.login_view = "login"

oid = OpenID(os.path.join(basedir, 'tmp'))

db = SQLAlchemy(app)



from app import views, models
