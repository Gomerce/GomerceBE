"""
Define the Store model
"""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import UUID

from . import db
from .abc import BaseModel, MetaBaseModel


class Store(db.Model, BaseModel, metaclass=MetaBaseModel):
    """"
    The Store Model
    """

    __tablename__ = "stores"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = db.Column(db.String(50), nullable=False, unique=True)
    address = db.Column(db.String)
    phone = db.Column(db.String(15))
    email = db.Column(db.String(100))
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow)
    email_verified = db.Column(db.Boolean, default=False)
    phone_verified = db.Column(db.Boolean, default=False)

    # Foreign Key
    sellers_id = db.Column(UUID(as_uuid=True), db.ForeignKey(
        'sellers.id'), nullable=False)
