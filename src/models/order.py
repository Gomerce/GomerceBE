
"""
Define the Orders model
"""
from . import db
from .abc import BaseModel, MetaBaseModel
from datetime import datetime


class Orders(db.Model, BaseModel, metaclass=MetaBaseModel):
    """ The Orders model """

    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    total_cost = db.Column(db.Float, nullable=False)
    tax = db.Column(db.Float, nullable=False)
    delivery_status = db.Column(db.Boolean, nullable=False, default=False)
    delivered_at = db.Column(db.DateTime, nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey("status.id"), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
    shipping_address_id = db.Column(db.Integer, db.ForeignKey("shipping_addresses.id"), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey("sellers.id"), nullable=False)
    coupon_id = db.Column(db.Integer, db.ForeignKey("coupons.id"), nullable=False)
    cart_id = db.Column(db.Integer, db.ForeignKey("cart.id"), nullable=False)
    payment_details = db.relationship("payment_details", backref="orders", lazy=True)
    order_details =  db.relationship("order_details", backref="orders", lazy=True)


