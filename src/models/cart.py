"""
Define the Cart model
"""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import Numeric, UUID

from . import db
from .abc import BaseModel, MetaBaseModel


class Cart(db.Model, BaseModel, metaclass=MetaBaseModel):
    """ The Cart model """

    __tablename__ = "carts"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    unit_price = db.Column(Numeric(precision=15, scale=2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_cost = db.Column(Numeric(precision=15, scale=2), nullable=False)

    # Foreign Key
    customer_id = db.Column(UUID(as_uuid=True), db.ForeignKey(
        "customers.id"), nullable=False)
    product_id = db.Column(UUID(as_uuid=True), db.ForeignKey(
        "products.id"), nullable=False)
