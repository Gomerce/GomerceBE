"""
Defines the blueprint for the users
"""
from flask import Blueprint

from ..resources import UserResource

USER_BLUEPRINT = Blueprint("user", __name__)

USER_BLUEPRINT.route("/user", methods=['GET'])(UserResource.get_all)
USER_BLUEPRINT.route("/user", methods=['POST'])(UserResource.post)
USER_BLUEPRINT.route("/user/<int:user_id>", methods=['GET'])(UserResource.get_one)
