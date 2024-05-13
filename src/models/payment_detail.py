"""
Define the Payment Detail model
"""


from datetime import datetime
from uuid import uuid4


from sqlalchemy import Numeric, UUID


from . import db
from .abc import BaseModel, MetaBaseModel


class PaymentDetail(db.Model, BaseModel, metaclass=MetaBaseModel):
    """ The Payment Details model """

    __tablename__ = "payment_details"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    amount = db.Column(Numeric(precision=15, scale=2), nullable=False)
    status = db.Column(db.String(10))
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow)

    # Foreign Key
    orders_id = db.Column(UUID(as_uuid=True), db.ForeignKey(
        'orders.id'), nullable=False)
    payment_methods_id = db.Column(UUID(as_uuid=True), db.ForeignKey(
        'payment_methods.id'), nullable=False)

    # Relationship
    # orders = db.relationship('Order', backref='payment_details', lazy=True)
