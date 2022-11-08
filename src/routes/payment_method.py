"""
Defines the blueprint for the payment methods
"""
from flask import Blueprint

from resources import PaymentMethodResource

PAYMENT_METHOD_BLUEPRINT = Blueprint("payment_method", __name__)

PAYMENT_METHOD_BLUEPRINT.route(
    "/payment-methods", methods=['GET'])(PaymentMethodResource.get_all)
PAYMENT_METHOD_BLUEPRINT.route("/payment-methods/<int:detail_id>",
                         methods=['GET'])(PaymentMethodResource.get_one)
