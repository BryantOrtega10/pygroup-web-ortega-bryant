from datetime import datetime
from app.db import db, ma
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    rol_id = db.Column(db.Integer, db.ForeignKey('rol.id'), default=2)


class Rol(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())


class RolSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Rol


def create_user(username, password):
    user = User(username=username, password=generate_password_hash(password, method="sha256"))
    db.session.add(user)
    db.session.commit()
    return user



def get_user_by_username(username):
    user = User.query.filter_by(
            username=username
        ).first()
    return user


def get_user(username, password):
    user = get_user_by_username(username)
    if not user or not check_password_hash(user.password, password):
        return None
    return user


def update_user(id, username):
    user = User.query.filter_by(id=id).first()
    user.username = username
    db.session.add(user)
    db.session.commit()
    return user

def update_password(id, password):
    user = User.query.filter_by(id=id).first()
    user.password = generate_password_hash(password, method="sha256")
    db.session.add(user)
    db.session.commit()
    return user
