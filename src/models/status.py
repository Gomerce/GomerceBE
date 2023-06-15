"""
Define the Status model
"""

from . import db
from .abc import BaseModel, MetaBaseModel
from sqlalchemy import ForeignKey


class Status(db.Model, BaseModel, metaclass=MetaBaseModel):
    """"
    The Status Model
    """

    __tablename__ = "statuses"

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(100), nullable=False)

    # Foreign Key
    order_id = db.Column(db.Integer, db.ForeignKey(
        'orders.id'), nullable=False)
