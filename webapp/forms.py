from logging import raiseExceptions
from flask.app import Flask
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.core import IntegerField, SelectField
from wtforms.fields.simple import PasswordField, SubmitField
from wtforms.validators import Email, Length, EqualTo, DataRequired, ValidationError
from webapp.models import User, InterstellarTraveller
from wtforms.fields.html5 import DateField
from datetime import date


class RegisterForm(FlaskForm):
    # Query the DB for existing username or email address.

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError(
                "Username already exists. Please try a different username"
            )

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(
            email_address=email_address_to_check.data
        ).first()
        if email_address:
            raise ValidationError(
                "Email already in use. Please use a different email adress."
            )

    username = StringField(
        label="Username:", validators=[Length(min=8, max=30), DataRequired()]
    )
    name = StringField(
        label="Name:", validators=[Length(min=1, max=30), DataRequired()]
    )
    email_address = StringField(label="E-mail:", validators=[Email(), DataRequired()])
    password = PasswordField(
        label="Password:", validators=[Length(min=6), DataRequired()]
    )
    confirm_password = PasswordField(
        label="Confirm Password:", validators=[EqualTo("password"), DataRequired()]
    )
    submit = SubmitField(label="Create Account")


class LoginForm(FlaskForm):
    username = StringField(label="Username:", validators=[DataRequired()])
    password = PasswordField(label="Password:", validators=[DataRequired()])
    submit = SubmitField(label="Login")


class CosmonautForm(FlaskForm):
    age = IntegerField(label="Age", validators=[DataRequired()])
    previous_experience = SelectField(
        label="Do you have previous interstellar travel experience?",
        choices=["Yes", "No"],
        validators=[DataRequired()],
    )
    destination = SelectField(
        label="Please tell us where would you like to go?:",
        validators=[DataRequired()],
        choices=[
            "Proxima Centauri System",
            "TRAPPIST-1 System",
            "Kepler-1649 System",
            "Teegarden's Star System",
            "Kepler-452 System",
        ],
    )
    departure_date = DateField(
        label="When would you like to depart?",
        validators=[DataRequired()],
        default=date.today,
    )
    return_date = DateField(
        label="When would you like to return?", validators=[DataRequired()]
    )
    blackhole_visit = SelectField(
        label="Would you like a tour to the nearest black hole aswell?",
        choices=["Yes", "No"],
    )
    submit = SubmitField(label="Book")

    def validate_age(self, attempted_age):
        if attempted_age.data < 18 or attempted_age.data > 150:
            raise ValidationError(
                "You cannot book an interstellar vacation with that age. Only those older than 18 and younger than 150 years can book a vacation like this."
            )

    def validate_departure_date(self, attempted_departure):
        if (
            attempted_departure.data >= self.return_date.data
            or attempted_departure.data < date.today()
        ):
            raise ValidationError(
                "Travelling through time yet isn't possible. Pick a departure date that is not in the past and that is before the return date."
            )
        booked_slots = InterstellarTraveller.query.filter_by(
            departure_date=attempted_departure.data, destination=self.destination.data
        ).count()
        if booked_slots >= 5:
            raise ValidationError(
                f"There are no available slots on {self.destination.data} for this departure date, please pick another date to start your interstellar journey!"
            )
