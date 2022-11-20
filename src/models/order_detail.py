"""
Define the Order Detail model
"""

from . import db
from .abc import BaseModel, MetaBaseModel
from datetime import datetime

class OrderDetail(db.Model, BaseModel, metaclass=MetaBaseModel):
    """ The Order Detail model """

    __tablename__ = "order_details"

    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow)

    #Foreign Key
    orders_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    products_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    statuses_id = db.Column(db.Integer, db.ForeignKey('statuses.id'), nullable=False)

    