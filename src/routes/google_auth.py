"""
Defines the blueprint for the google auth
"""
from flask import Blueprint

from resources import GoogleResource

GOOGLE_BLUEPRINT = Blueprint("google_auth", __name__)

GOOGLE_BLUEPRINT.route(
    "/google_login", methods=['GET'])(GoogleResource.google_login)
GOOGLE_BLUEPRINT.route(
    "/callback", methods=['GET'])(GoogleResource.callback)