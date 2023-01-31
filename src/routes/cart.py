"""
Defines the blueprint for the cart
"""
from flask import Blueprint

from resources import CartResource

CART_BLUEPRINT = Blueprint("cart", __name__)

CART_BLUEPRINT.route(
    "/carts/<int:customer_id>", methods=['GET'])(CartResource.get_all)
CART_BLUEPRINT.route("/carts", methods=['POST'])(CartResource.post)
CART_BLUEPRINT.route("/carts/<int:cart_id>",
                     methods=['GET'])(CartResource.get_one)
CART_BLUEPRINT.route("/carts/<int:cart_id>",
                     methods=["DELETE"])(CartResource.delete)
CART_BLUEPRINT.route("/carts/<int:cart_id>",
                     methods=["PUT"])(CartResource.update)
