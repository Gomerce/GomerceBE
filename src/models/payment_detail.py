"""
Define the Payment Detail model
"""
from . import db
from .abc import BaseModel, MetaBaseModel
from datetime import datetime


class PaymentDetail(db.Model, BaseModel, metaclass=MetaBaseModel):
    """ The Payment Details model """

    __tablename__ = "payment_details"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, nullable=False, unique=True)
    amount = db.Column(db.Integer)
    status = db.Column(db.String(10))
    payment_initiated = db.Column(db.DateTime(), default=datetime.utcnow)
    paymentmethod_id = db.Column(db.Integer)
