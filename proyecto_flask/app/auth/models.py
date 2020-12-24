from datetime import datetime
from app.db import db, ma
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    rol_id = db.Column(db.Integer, db.ForeignKey('rol.id'), default=2)

class Rol(db.Model):
    """
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())


class RolSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Rol