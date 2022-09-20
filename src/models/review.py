"""
Define the Review model
"""
from . import db
from .abc import BaseModel, MetaBaseModel
from datetime import datetime


class Review(db.Model, BaseModel, metaclass=MetaBaseModel):
    """ The Review model """

    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(255))
    rating = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    seller_id = db.Column(db.Integer, db.ForeignKey('sellers.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))

