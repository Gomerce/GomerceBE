"""
Define the Cart model
"""
import uuid
from . import db
from .abc import BaseModel, MetaBaseModel
from datetime import datetime


class Cart(db.Model, BaseModel, metaclass=MetaBaseModel):
    """ The Cart model """

    __tablename__ = "carts"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    unit_price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    total_cost = db.Column(db.Float, nullable=False)

    #Foreign Key
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)

    #Relationship
    # payment_details = db.relationship("PaymentDetail", backref="orders", lazy=True)
    # order_details =  db.relationship("OrderDetail", backref="orders", lazy=True)
    # statuses =  db.relationship("Status", backref="orders", lazy=True)

    
