"""
    Define the sellers models
"""

from lib2to3.pytree import Base
from . import db
from .abc import BaseModel, MetaBaseModel
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash


class Seller(db.Model, BaseModel, metaclass=MetaBaseModel):

    __tablename__ ='sellers'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False, unique=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone = db.Column(db.String(15))
    email = db.Column(db.String(100), nullable=False, unique=True)
    password=(db.Text())
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow)
    rating = db.Column(db.Integer )
    email_verified = db.Column(db.Boolean)
    phone_verified = db.Column(db.Boolean )
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

