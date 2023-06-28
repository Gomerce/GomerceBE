"""
Define the Product Subcategory model
"""

from tokenize import Name
from . import db
from .abc import BaseModel, MetaBaseModel
from datetime import datetime


class ProductSubcategory(db.Model, BaseModel, metaclass=MetaBaseModel):
    """ The Product Subcategory model """

    __tablename__ = "product_subcategories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    sku = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), onupdate=datetime.utcnow)

    # Foreign Key
    product_categories_id = db.Column(db.Integer, db.ForeignKey(
        'product_categories.id'), nullable=False)

    # Relationship
    products = db.relationship(
        'Product', backref='product_subcategories', lazy=True)
