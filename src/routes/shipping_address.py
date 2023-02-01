"""
Defines the blueprint for the shipping address
"""
from flask import Blueprint

from resources import ShippingAddressResource

SHIPPING_ADDRESS_BLUEPRINT = Blueprint("shipping_address", __name__)

SHIPPING_ADDRESS_BLUEPRINT.route(
    "/shipping_addresses", methods=['GET'])(ShippingAddressResource.get_all)
SHIPPING_ADDRESS_BLUEPRINT.route("/shipping_addresses/<int:address_id>",
                                 methods=['GET'])(ShippingAddressResource.get_one)
SHIPPING_ADDRESS_BLUEPRINT.route("/shipping_addresses",
                                 methods=['POST'])(ShippingAddressResource.post)
SHIPPING_ADDRESS_BLUEPRINT.route("/shipping_addresses/<int:address_id>",
                                 methods=['PUT'])(ShippingAddressResource.update_address)
SHIPPING_ADDRESS_BLUEPRINT.route("/shipping_addresses/<int:address_id>",
                                 methods=['DELETE'])(ShippingAddressResource.delete)