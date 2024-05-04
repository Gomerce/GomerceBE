"""
Define the Product model
"""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import Numeric, UUID

from . import db
from .abc import BaseModel, MetaBaseModel


class Product(db.Model, BaseModel, metaclass=MetaBaseModel):
    """ The Product model """

    __tablename__ = "products"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = db.Column(db.String(300), nullable=False)
    price = db.Column(Numeric(precision=15, scale=2), nullable=False)
    quantity = db.Column(db.Integer)
    short_desc = db.Column(db.String(500), nullable=False)
    long_desc = db.Column(db.Text())
    rating = db.Column(db.Integer)
    thumbnail = db.Column(db.String(100))
    image = db.Column(db.String(100))
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), onupdate=datetime.utcnow)

    # Foreign Key
    sellers_id = db.Column(UUID(as_uuid=True), db.ForeignKey(
        'sellers.id'), nullable=False)
    product_categories_id = db.Column(UUID(as_uuid=True), db.ForeignKey(
        'product_categories.id'), nullable=False)
    product_subcategories_id = db.Column(UUID(as_uuid=True), db.ForeignKey(
        'product_subcategories.id'), nullable=False)
    brand_id = db.Column(UUID(as_uuid=True), db.ForeignKey(
        'brands.id'), nullable=False)

    # Relationship
    reviews = db.relationship('Review', backref='products', lazy=True)
    order_details = db.relationship(
        'OrderDetail', backref='products', lazy=True)
