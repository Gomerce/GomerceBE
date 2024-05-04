"""
Define the Product Category model
"""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import UUID

from . import db
from .abc import BaseModel, MetaBaseModel


class ProductCategory(db.Model, BaseModel, metaclass=MetaBaseModel):
    """ The Product Category model """

    __tablename__ = "product_categories"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = db.Column(db.String(100), nullable=False)
    sku = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow)

    # Relationship
    products = db.relationship(
        'Product', backref='product_categories', lazy=True)

    products_subcategories = db.relationship(
        'ProductSubcategory', backref='product_categories', lazy=True)
