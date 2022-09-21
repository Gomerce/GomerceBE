"""
Define the OrderDetails model
"""
from . import db
from .abc import BaseModel, MetaBaseModel


class OrderDetails(db.Model, BaseModel, metaclass=MetaBaseModel):
    """OrderDetails Model"""

    __tablename__ = "order_details"

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    sku = db.Column(db.String(50), nullable=False)

    #foreign keys
    # order_id = db.Column(db.Integer, db.ForeignKey('Order.id'), nullable=False)
    # product_id = db.Column(db.Integer, db.ForeignKey('Product.id'), nullable=False)
