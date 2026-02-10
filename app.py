import os
import requests
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

class App:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['SECRET_KEY'] = 'secret_key'
        self.db = SQLAlchemy(self.app)
        self.ma = Marshmallow(self.app)
        self.bcrypt = Bcrypt(self.app)
        self.jwt = JWTManager(self.app)
        CORS(self.app)

    def run(self):
        self.app.run(debug=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

def create_user(username, password):
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return user

def authenticate_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and self.bcrypt.check_password_hash(user.password, password):
        return user
    return None

def generate_token(user):
    return create_access_token(identity=user.id)

def verify_token(token):
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        return user
    except:
        return None

app = App()
app.run()