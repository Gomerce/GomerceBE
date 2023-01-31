"""
Defines the blueprint for the order details
"""
from flask import Blueprint

from resources import OrderDetailResource

ORDER_DETAIL_BLUEPRINT = Blueprint("order_detail", __name__)

ORDER_DETAIL_BLUEPRINT.route(
    "/order-order_details", methods=['GET'])(OrderDetailResource.get_all)
ORDER_DETAIL_BLUEPRINT.route("/order_details/<int:order_detail_id>",
                         methods=['POST'])(OrderDetailResource.post)
ORDER_DETAIL_BLUEPRINT.route("/order_details/<int:order_detail_id>",
                       methods=['GET'])(OrderDetailResource.get_one)
ORDER_DETAIL_BLUEPRINT.route("/order_details/<int:order_detail_id>",
                       methods=["DELETE"])(OrderDetailResource.delete)
ORDER_DETAIL_BLUEPRINT.route("/order_details/<int:order_detail_id>",
                       methods=["PUT"])(OrderDetailResource.update)
