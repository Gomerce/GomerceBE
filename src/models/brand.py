"""
Define the Product Category model
"""

from tokenize import Name
from . import db
from .abc import BaseModel, MetaBaseModel
from datetime import datetime

class Brand(db.Model, BaseModel, metaclass=MetaBaseModel):
    """ The Brand model """

    __tablename__ = "brands"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(100))
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow)

    #Foregn Keys
    product_categories_id = db.Column(db.Integer, db.ForeignKey('product_categories.id'), nullable=False)

    #Relationship
    products = db.relationship('Product', backref='brands', lazy=True)