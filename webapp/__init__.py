import re

#pip install flask
from flask import Flask

#pip install mysqlclient
#pip install flask-sqlalchemy
from flask_sqlalchemy import SQLAlchemy

# from datetime import datetime

#pip install flask_bcrypt, for cripting the password
from flask_bcrypt import Bcrypt

#pip install flask_login
from flask_login import LoginManager


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://nikola:asdasd@192.168.138.128:3306/flask-nikola"
app.config["SECRET_KEY"] = "dcf8275b3b04f25160897be"
db = SQLAlchemy(app)
#Used to hash passwords
bcrypt = Bcrypt(app)


#Creating a loggin manager for the app.
login_manager = LoginManager(app)



from webapp import routes