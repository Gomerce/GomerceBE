"""
Define the Status model
"""
from uuid import uuid4
from sqlalchemy import UUID

from . import db
from .abc import BaseModel, MetaBaseModel


class Status(db.Model, BaseModel, metaclass=MetaBaseModel):
    """"
    The Status Model
    """

    __tablename__ = "statuses"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    status = db.Column(db.String(100), nullable=False)

    # Foreign Key
    order_id = db.Column(UUID(as_uuid=True), db.ForeignKey(
        'orders.id'), nullable=False)
