"""
Define the Coupon model
"""


from datetime import datetime

from sqlalchemy import Numeric

from . import db
from .abc import BaseModel, MetaBaseModel


class Coupon(db.Model, BaseModel, metaclass=MetaBaseModel):
    """ The Coupon model """

    __tablename__ = "coupons"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), nullable=False, unique=True)
    amount = db.Column(Numeric(precision=15, scale=2), nullable=False)
    expires_at = db.Column(
        db.DateTime(), default=datetime.utcnow, nullable=False)
    created_at = db.Column(
        db.DateTime(), default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow)

    # Relationship
    orders = db.relationship("Order", backref="coupons", lazy=True)
