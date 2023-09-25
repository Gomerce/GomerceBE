"""
Define the Cart model
"""

from datetime import datetime

from sqlalchemy import Numeric

from . import db
from .abc import BaseModel, MetaBaseModel


class Cart(db.Model, BaseModel, metaclass=MetaBaseModel):
    """ The Cart model """

    __tablename__ = "carts"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    unit_price = db.Column(Numeric(precision=15, scale=2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_cost = db.Column(Numeric(precision=15, scale=2), nullable=False)

    # Foreign Key
    customer_id = db.Column(db.Integer, db.ForeignKey(
        "customers.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey(
        "products.id"), nullable=False)
