"""
Define the Product Category model
"""

from tokenize import Name
from . import db
from .abc import BaseModel, MetaBaseModel
from datetime import datetime


class ProductCategory(db.Model, BaseModel, metaclass=MetaBaseModel):
    """ The Product Category model """

    __tablename__ = "product_categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    sku = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow)

    # Relationship
    products = db.relationship(
        'Product', backref='product_categories', lazy=True)

    products_subcategories = db.relationship(
        'ProductSubcategory', backref='product_categories', lazy=True)
