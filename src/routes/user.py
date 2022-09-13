"""
Defines the blueprint for the users
"""
from flask import Blueprint
from flask_restful import Api
from utils import errors

from resources import UserResource, UsersResource

USER_BLUEPRINT = Blueprint("user", __name__)
api = Api(USER_BLUEPRINT, errors=errors)
api.add_resource(UserResource, "/users/<int:user_id>")
api.add_resource(UsersResource, "/users")
