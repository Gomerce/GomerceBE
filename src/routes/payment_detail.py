"""
Defines the blueprint for the payment details
"""
from flask import Blueprint

from resources import PaymentDetailResource

PAYMENT_DETAIL_BLUEPRINT = Blueprint("payment_detail", __name__)

PAYMENT_DETAIL_BLUEPRINT.route(
    "/payment_details", methods=['GET'])(PaymentDetailResource.get_all)
PAYMENT_DETAIL_BLUEPRINT.route("/payment_details/<int:payment_id>",
                               methods=['GET'])(PaymentDetailResource.get_one)
PAYMENT_DETAIL_BLUEPRINT.route("/payment_details",
                               methods=['POST'])(PaymentDetailResource.post)
PAYMENT_DETAIL_BLUEPRINT.route("/payment_details/<int:payment_id>",
                               methods=["DELETE"])(PaymentDetailResource.delete)
PAYMENT_DETAIL_BLUEPRINT.route("/payment_details/<int:payment_id>",
                               methods=["PUT"])(PaymentDetailResource.update)
