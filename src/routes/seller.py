"""
Defines the blueprint for the sellers
"""
from flask import Blueprint

from resources import SellerResource

SELLER_BLUEPRINT = Blueprint("seller", __name__)

SELLER_BLUEPRINT.route(
    "/sellers", methods=['GET'])(SellerResource.get_all)
SELLER_BLUEPRINT.route("/sellers", methods=['POST'])(SellerResource.post)
SELLER_BLUEPRINT.route("/sellers/<int:seller_id>",
                       methods=['GET'])(SellerResource.get_one)
