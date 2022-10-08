"""
    Define the stores models
"""

from . import db
from .abc import BaseModel, MetaBaseModel
from datetime import datetime


class Store(db.Model, BaseModel,  metaclass=MetaBaseModel):

    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    address = db.Column(db.Text)
    phone = db.Column(db.String(15))
    email = db.Column(db.String(100), nullable=False, unique=True)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow)
    email_verified = db.Column(db.Boolean)
    phone_verified = db.Column(db.Boolean )
    seller = db.relationship('Seller', backref='stores', uselist=False)

