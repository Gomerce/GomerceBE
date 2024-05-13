"""authentication.py

Keyword arguments:
argument -- description
Return: return_description
"""

from flask import Blueprint

from resources import AuthenticationResource

AuthenticationBlueprint = Blueprint("authentication", __name__)

AuthenticationBlueprint.route(
    "/auth/login", methods=['POST'])(AuthenticationResource.login)
