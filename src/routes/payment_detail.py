"""
Defines the blueprint for the payment details
"""
from flask import Blueprint

from resources import PaymentDetailResource

PAYMENT_DETAIL_BLUEPRINT = Blueprint("payment_detail", __name__)

PAYMENT_DETAIL_BLUEPRINT.route(
    "/payment-details", methods=['GET'])(PaymentDetailResource.get_all)
PAYMENT_DETAIL_BLUEPRINT.route("/payment-details/<int:detail_id>",
                         methods=['GET'])(PaymentDetailResource.get_one)
