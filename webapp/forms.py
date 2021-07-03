#pip install flask-wtf
from enum import unique
from flask.app import Flask
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.simple import PasswordField, SubmitField
# pip install email_validator
from wtforms.validators import Email, Length, EqualTo, DataRequired, ValidationError
from webapp.models import User
class RegisterForm(FlaskForm):
    #Query the DB for existing username or email address.
    
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError("Username already exists. Please try a different username")
    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError("Username already exists. Please try a different username")
    
    username = StringField(label='Username:', validators=[Length(min=8, max=30), DataRequired()])
    name = StringField(label='Name:',validators=[Length(min=1, max=30), DataRequired()])
    email_address = StringField(label='E-mail:',validators=[Email(),DataRequired()])
    password = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    confirm_password = PasswordField(label='Confirm Password:', validators=[EqualTo('password'),DataRequired()])
    submit = SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    username = StringField(label='Username:',validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Login')
    