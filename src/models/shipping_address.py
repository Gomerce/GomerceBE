"""
Define the Shipping Address model
"""


from datetime import datetime

from uuid import uuid4

from sqlalchemy import UUID


from . import db
from .abc import BaseModel, MetaBaseModel


class ShippingAddress(db.Model, BaseModel, metaclass=MetaBaseModel):
    """ The Shipping Address model """

    __tablename__ = "shipping_addresses"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    country = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(70), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    street_name = db.Column(db.String(300), nullable=False)
    zipcode = db.Column(db.String(50))
    phone = db.Column(db.String(15), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow)

    # Relationship
    orders = db.relationship('Order', backref='shipping_addresses', lazy=True)
