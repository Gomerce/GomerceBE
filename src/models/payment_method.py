"""
Define the PaymentMethod model
"""


from datetime import datetime

from . import db


class PaymentMethod(db.Model):
    __tablename__ = 'payment_methods'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    currency = db.Column(db.String(30), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow)

    # relationship
    payment_details = db.relationship(
        'PaymentDetail', backref="payment_methods", lazy=True)
