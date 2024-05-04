"""
Define the Order Detail model
"""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import UUID

from . import db
from .abc import BaseModel, MetaBaseModel


class OrderDetail(db.Model, BaseModel, metaclass=MetaBaseModel):
    """ The Order Detail model """

    __tablename__ = "order_details"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    sku = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow)

    # Foreign Key
    orders_id = db.Column(UUID(as_uuid=True), db.ForeignKey(
        'orders.id'), nullable=False)
    products_id = db.Column(UUID(as_uuid=True), db.ForeignKey(
        'products.id'), nullable=False)
    statuses_id = db.Column(UUID(as_uuid=True), db.ForeignKey(
        'statuses.id'), nullable=False)
