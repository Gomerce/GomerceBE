"""
Defines the blueprint for the products
"""
from flask import Blueprint

from resources import ProductResource

PRODUCT_BLUEPRINT = Blueprint("products", __name__)

PRODUCT_BLUEPRINT.route(
    "/products", methods=['GET'])(ProductResource.get_all)
PRODUCT_BLUEPRINT.route("/products", methods=['POST'])(ProductResource.post)
PRODUCT_BLUEPRINT.route("/products/<int:product_id>",
                         methods=['GET'])(ProductResource.get_one)
