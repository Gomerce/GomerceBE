"""
Defines the blueprint for the shipping address
"""
from flask import Blueprint

from resources import ShippingAddressResource

SHIPPING_ADDRESS_BLUEPRINT = Blueprint("shipping_address", __name__)

SHIPPING_ADDRESS_BLUEPRINT.route(
    "/shipping-addresses", methods=['GET'])(ShippingAddressResource.get_all)
SHIPPING_ADDRESS_BLUEPRINT.route("/shipping-addresses/<int:address_id>",
                         methods=['GET'])(ShippingAddressResource.get_one)
