"""
Define the Product Category model
"""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import UUID

from . import db
from .abc import BaseModel, MetaBaseModel


class Brand(db.Model, BaseModel, metaclass=MetaBaseModel):
    """ The Brand model """

    __tablename__ = "brands"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(100))
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow)

    # Relationship

    products = db.relationship('Product', backref='brands', lazy=True)
