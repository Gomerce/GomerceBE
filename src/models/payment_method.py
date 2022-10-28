"""
Define the PaymentMethod model
"""
from locale import currency
from . import db
from datetime import datetime
# from sqlalchemy_utils import CurrencyType, Currency


class PaymentMethod(db.Model):
    __tablename__ = 'payment_methods'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    currency = db.Column(db.String(30), nullable=False)
    # currency = db.Column(CurrencyType)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow)

    # relationship
    payment_details = db.relationship(
        'PaymentDetail', backref="payment_methods", lazy=True)


# def __init__(self, name='',currency=''):
#     self.name = name
#     self.currency = currency


# payment = PaymentMethod()

# payment.currency = Currency('NGN')

# db.session.add(payment)
# db.session.commit()


# to see the sign of any currency

# payment.currency # Currency('NGN')
# payment.currency.name # Nigerian Naira
