"""
Define the Seller model
"""
import uuid
from . import db
from .abc import BaseModel, MetaBaseModel
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash


class Seller(db.Model, BaseModel, metaclass=MetaBaseModel):
    """ The Order model """

    __tablename__ = "sellers"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(300))
    last_name = db.Column(db.String(300))
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(15))
    username = db.Column(db.String(32), nullable=False, unique=True)
    password = db.Column(db.Text(), nullable=False)
    rating = db.Column(db.Integer)
    email_verified = db.Column(db.Boolean)
    phone_verified = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    # Relationship
    reviews = db.relationship('Review', backref='sellers', lazy=True)
    stores = db.relationship('Store', backref='sellers', lazy=True)
    orders = db.relationship('Order', backref='sellers', lazy=True)
