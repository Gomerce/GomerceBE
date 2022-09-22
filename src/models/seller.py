"""
Define the Seller model
"""
from . import db
from .abc import BaseModel, MetaBaseModel
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash


class Seller(db.Model, BaseModel, metaclass=MetaBaseModel):
    """ The Customer model """

    __tablename__ = "sellers"

    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer)
    first_name = db.Column(db.String(300))
    last_name = db.Column(db.String(300))
    username = db.Column(db.String(32), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    email_verified = db.Column(db.Boolean)
    phone = db.Column(db.String(15))
    password = db.Column(db.Text())
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
