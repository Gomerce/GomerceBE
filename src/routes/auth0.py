"""
Defines the blueprint for the auth for admin and customer
"""
from flask import Blueprint

from resources import Auth0Resource

AUTH0_BLUEPRINT = Blueprint("auth0", __name__)

AUTH0_BLUEPRINT.route("/login", methods=['POST'])(Auth0Resource.login)
AUTH0_BLUEPRINT.route("/logout", methods=['POST'])(Auth0Resource.logout)
# AUTH0_BLUEPRINT.route("/register", methods=['POST'])(Auth0Resource.register_user)
AUTH0_BLUEPRINT.route("/callback", methods=['POST'])(Auth0Resource.callback)
