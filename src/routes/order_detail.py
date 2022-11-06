"""
Defines the blueprint for the order details
"""
from flask import Blueprint

from resources import OrderDetailResource

ORDER_DETAIL_BLUEPRINT = Blueprint("order_detail", __name__)

ORDER_DETAIL_BLUEPRINT.route(
    "/order-details", methods=['GET'])(OrderDetailResource.get_all)
ORDER_DETAIL_BLUEPRINT.route("/order-details/<int:detail_id>",
                         methods=['GET'])(OrderDetailResource.get_one)
