"""
Defines the blueprint for the payment methods
"""
from flask import Blueprint

from resources import PaymentMethodResource

PAYMENT_METHOD_BLUEPRINT = Blueprint("payment_method", __name__)

PAYMENT_METHOD_BLUEPRINT.route(
    "/payment_methods", methods=['GET'])(PaymentMethodResource.get_all)
PAYMENT_METHOD_BLUEPRINT.route("/payment_methods/<int:method_id>",
                               methods=['GET'])(PaymentMethodResource.get_one)
PAYMENT_METHOD_BLUEPRINT.route("/payment_methods",
                               methods=['POST'])(PaymentMethodResource.post)
PAYMENT_METHOD_BLUEPRINT.route("/payment_methods/<int:method_id>",
                               methods=["DELETE"])(PaymentMethodResource.delete)
PAYMENT_METHOD_BLUEPRINT.route("/payment_methods/<int:method_id>",
                               methods=["PUT"])(PaymentMethodResource.update)