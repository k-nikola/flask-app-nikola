from abc import abstractmethod
from werkzeug import datastructures
from webapp import app
from flask import render_template, request, redirect, url_for, flash
from webapp.forms import LoginForm, RegisterForm
from webapp.models import User
from webapp import db
from flask_login import login_user, logout_user


@app.route("/")
@app.route("/home")
def index():
    return render_template("index.html")

@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/register", methods=["POST","GET"])
def register():
    form = RegisterForm()
    
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              name=form.name.data,
                              email_address=form.email_address.data,
                              password=form.password.data,
                              )
        #Adds the new user to the database, and then commits the changes
        db.session.add(user_to_create)
        db.session.commit()
        #Logs in newly created user, and redirects the user to index page
        login_user(user_to_create)
        flash(f"Successfully created an account. Now logged in as {user_to_create.username}", category="info")
        return redirect(url_for('index'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating an user: {err_msg}', category="danger")
    return render_template("register.html", form=form)



@app.route("/login", methods=["POST","GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        #checking if the user exists, and if the password is correct, through the check password function defined in user model.
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f"Success! You are logged in as: {attempted_user.username}", category="success")
            return redirect(url_for('index'))
        else:
            flash("Username or password not correct. Please try again!", category="danger")
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    flash("Successfully logged out.", category="info")
    return redirect(url_for("index"))