from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('db_uri').strip("''")
app.config["SECRET_KEY"] = os.getenv('secret_key').strip("''")
db = SQLAlchemy(app)
#Used to hash passwords
bcrypt = Bcrypt(app)


#Creating a loggin manager for the app.
login_manager = LoginManager(app)

#Telling login manager where the login page is located
login_manager.login_view = "login"
login_manager.login_message_category = "info"

from webapp import routes