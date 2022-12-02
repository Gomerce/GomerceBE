"""
Defines the blueprint for the stores
"""
from flask import Blueprint

from resources import StoreResource

STORE_BLUEPRINT = Blueprint("stores", __name__)
STORE_BLUEPRINT.route(
    "/stores", methods=['GET'])(StoreResource.get_all)
STORE_BLUEPRINT.route("/stores", methods=['POST'])(StoreResource.post)
STORE_BLUEPRINT.route("/stores/<int:store_id>",
                         methods=['GET'])(StoreResource.get_one)
