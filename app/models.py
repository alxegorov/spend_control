from app import db, login
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from time import time


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    active = db.Column(db.Boolean)
    cars = db.relationship('Car', backref='owner', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_activate_token(self):
        return jwt.encode({'auth_apply': self.id}, current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def activate_user(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['auth_apply']
            act_user = User.query.get(id)
            act_user.active = True
        except:
            return
        return act_user

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in}, current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    @property
    def is_active(self):
        return self.active


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class CarModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    manufacturer = db.Column(db.String(120), index=True)
    model = db.Column(db.String(120), index=True)
    fuel_type = db.Column(db.String(20), index=True)
    engine_volume = db.Column(db.Integer, index=True)
    engine_power = db.Column(db.Integer, index=True)
    cars = db.relationship('Car', backref='model', lazy='dynamic')


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trip = db.Column(db.Integer)
    car_model_id = db.Column(db.Integer, db.ForeignKey('car_model.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
