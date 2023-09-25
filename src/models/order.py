"""
Define the Order model
"""


from datetime import datetime

from sqlalchemy import Numeric

from . import db
from .abc import BaseModel, MetaBaseModel


class Order(db.Model, BaseModel, metaclass=MetaBaseModel):
    """ The Order model """

    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    total_cost = db.Column(Numeric(precision=15, scale=2), nullable=False)
    tax = db.Column(Numeric(precision=15, scale=2), nullable=False)
    delivery_status = db.Column(db.Boolean, nullable=False, default=False)
    delivered_at = db.Column(db.DateTime, nullable=False)

    # Foreign Key
    customer_id = db.Column(db.Integer, db.ForeignKey(
        "customers.id"), nullable=False)
    shipping_address_id = db.Column(db.Integer, db.ForeignKey(
        "shipping_addresses.id"), nullable=False)
    coupon_id = db.Column(db.Integer, db.ForeignKey(
        "coupons.id"), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey(
        "sellers.id"), nullable=False)

    # Relationship
    payment_details = db.relationship(
        "PaymentDetail", backref="orders", lazy=True)
    order_details = db.relationship("OrderDetail", backref="orders", lazy=True)
    statuses = db.relationship("Status", backref="orders", lazy=True)
