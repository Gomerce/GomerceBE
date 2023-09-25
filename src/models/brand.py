"""
Define the Product Category model
"""

from datetime import datetime

from . import db
from .abc import BaseModel, MetaBaseModel


class Brand(db.Model, BaseModel, metaclass=MetaBaseModel):
    """ The Brand model """

    __tablename__ = "brands"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(100))
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow)

    # Relationship

    products = db.relationship('Product', backref='brands', lazy=True)
