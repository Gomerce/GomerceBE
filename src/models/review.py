"""
Define the Review model
"""

from datetime import datetime
from uuid import uuid4
from sqlalchemy import UUID

from . import db
from .abc import BaseModel, MetaBaseModel


class Review(db.Model, BaseModel, metaclass=MetaBaseModel):
    """ The Review model """

    __tablename__ = "reviews"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    comment = db.Column(db.Text(), nullable=False)
    images = db.Column(db.String(100))
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow)

    # Foreign Key
    sellers_id = db.Column(UUID(as_uuid=True), db.ForeignKey(
        'sellers.id'), nullable=False)
    products_id = db.Column(UUID(as_uuid=True), db.ForeignKey(
        'products.id'), nullable=False)
