"""
Defines the blueprint for the coupon
"""
from flask import Blueprint

from resources import CouponResource

COUPON_BLUEPRINT = Blueprint("coupon", __name__)

COUPON_BLUEPRINT.route(
    "/coupons", methods=['GET'])(CouponResource.get_all)
COUPON_BLUEPRINT.route("/coupons", methods=['POST'])(CouponResource.post)
COUPON_BLUEPRINT.route("/coupons/<int:coupon_id>",
                         methods=['GET'])(CouponResource.get_one)