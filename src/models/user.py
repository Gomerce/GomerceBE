"""
Define the User model
"""
import uuid
from . import db
from .abc import BaseModel, MetaBaseModel
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, BaseModel, metaclass=MetaBaseModel):
    """ The User model """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    username = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.Text())
    first_name = db.Column(db.String(300))
    last_name = db.Column(db.String(300))
    admin = db.Column(db.Boolean)
    date_updated = db.Column(db.DateTime(), default=datetime.utcnow)
    date_created = db.Column(db.DateTime(), default=datetime.utcnow)

    def __init__(self, first_name, last_name, age=None):
        """ Create a new User """
        self.user_id = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.age = age

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
