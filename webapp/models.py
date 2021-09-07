from enum import unique
from webapp import db, bcrypt, login_manager

# Importing methods for login
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# User inherits from UserMixin for built in login functions
class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    name = db.Column(db.String(length=30), nullable=False)
    # surname = db.Column(db.String(length=40), nullable=False)
    email_address = db.Column(db.String(length=60), nullable=False, unique=True)
    password_crypted = db.Column(db.String(length=60), nullable=False)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, unencrypted_password):
        self.password_crypted = bcrypt.generate_password_hash(
            unencrypted_password
        ).decode("utf-8")

    def check_password_correction(self, attempted_password):
        # bcrypt.check_password_has returns true or false!
        return bcrypt.check_password_hash(self.password_crypted, attempted_password)

    interstellar_travellers = db.relationship(
        "InterstellarTraveller", backref="it_id", lazy=True
    )


class InterstellarTraveller(db.Model):
    id = db.Column(db.Integer(), db.ForeignKey("user.id"), primary_key=True)
    age = db.Column(db.Integer())
    previous_experience = db.Column(db.String(length=3))
    destination = db.Column(db.String(length=30))
    departure_date = db.Column(db.Date())
    return_date = db.Column(db.Date())
    blackhole_tour = db.Column(db.String(length=3))
