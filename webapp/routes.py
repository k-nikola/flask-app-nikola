from webapp import app
from flask import render_template, request, redirect, url_for, flash, Markup
from webapp.forms import CosmonautForm, LoginForm, RegisterForm
from webapp.models import InterstellarTraveller, User
from webapp import db
from flask_login import login_user, logout_user, current_user, login_required
from datetime import date


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


@app.route("/book", methods=["POST","GET"])
@login_required
def book():
    form = CosmonautForm()
    if form.validate_on_submit():
        attempted_traveller = InterstellarTraveller.query.filter_by(id=current_user.id).first()
        if not attempted_traveller:
            if form.departure_date.data<form.return_date.data and form.departure_date.data>=date.today():
                if 18<=form.age.data<150:
                    traveller_to_create=InterstellarTraveller(
                            id = current_user.id,
                            age = form.age.data,
                            previous_experience = form.previous_experience.data,
                            destination = form.destination.data,
                            departure_date = form.departure_date.data,
                            return_date = form.return_date.data,
                            blackhole_tour = form.blackhole_visit.data
                        )
                    db.session.add(traveller_to_create)
                    db.session.commit()
                    flash("Success! Your form has been submitted. Bon voyage!", category='success')
                    return redirect(url_for('index'))
                else:
                    flash("You cannot book an interstellar vacation with that age. Only those older than 18 and younger than 150 years can book a vacation like this.", category="danger")
            else:
                flash("Travelling through time yet isn't possible. Pick a departure date that is not in the past and that is before the return date.", category="danger")
        else:
            flash(Markup("Already registered for an interstellar vacation. At this moment you cannot book more than one vacation.Click <a href='/reservation'>here</a> to review your reservation."),category="danger")
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with your booking: {err_msg}', category="danger")
    return render_template("book.html", form=form)

@app.route("/reservation", methods=["POST","GET"])
@login_required
def reservation():
    current_traveller = InterstellarTraveller.query.filter_by(id=current_user.id).first()
    if request.method == "POST":
        flash("Succesfully cancelled the reservation, you will be redirected to the home page.",category="info")
        db.session.delete(current_traveller)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("reservation.html", current_traveller=current_traveller)
