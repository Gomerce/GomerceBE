"""
Define the Admin model
"""


from datetime import datetime
from uuid import uuid4

from sqlalchemy import UUID

from werkzeug.security import check_password_hash, generate_password_hash

from . import db
from .abc import BaseModel, MetaBaseModel


class Admin(db.Model, BaseModel, metaclass=MetaBaseModel):
    """ The Admin model """

    __tablename__ = "admins"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    username = db.Column(db.String(32), nullable=False, unique=True)
    first_name = db.Column(db.String(300))
    last_name = db.Column(db.String(300))
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(15))
    password = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow)
    email_verified = db.Column(db.Boolean, default=False)
    phone_verified = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        """ This function defines password setting for users """

        self.password = generate_password_hash(password)

    def check_password(self, password):
        """ This function defines confirm's the password setting for users """

        return check_password_hash(self.password, password)
