"""
Defines the blueprint for the orders
"""
from flask import Blueprint

from resources import OrderResource

ORDER_BLUEPRINT = Blueprint("orders", __name__)

ORDER_BLUEPRINT.route(
    "/orders", methods=['GET'])(OrderResource.get_all)
ORDER_BLUEPRINT.route("/orders",
                      methods=['POST'])(OrderResource.post)
ORDER_BLUEPRINT.route("/orders/<int:order_id>",
                      methods=['GET'])(OrderResource.get_one)
ORDER_BLUEPRINT.route("/orders/<int:order_id>",
                      methods=["DELETE"])(OrderResource.delete)
ORDER_BLUEPRINT.route("/orders/<int:order_id>",
                      methods=['PUT'])(OrderResource.update_order)
