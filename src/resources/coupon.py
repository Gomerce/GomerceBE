"""
Define the resources for the Coupon
"""
from flask import jsonify, abort
from flasgger import swag_from
from flask_restful import Resource
from flask_restful.reqparse import Argument
from repositories import CouponRepository
from utils import parse_params
from utils.errors import DataNotFound


class CouponResource(Resource):
    """ methods relative to the coupon """

    @staticmethod
    @swag_from("../swagger/coupon/get_one.yml")
    def get_one(coupon_id):
        """ Return a coupon key information based on coupon_id """

        try:
            coupon = CouponRepository.get_one(coupon_id=coupon_id)
            return jsonify({"data": coupon.json})
        except DataNotFound as e:
            abort(404, e.message)
        except Exception:
            abort(500)

    @staticmethod
    @swag_from("../swagger/coupon/get_all.yml")
    def get_all():
        """ Return all coupon key information based on the query parameter """
        coupon = CouponRepository.get_all()
        return jsonify({"data": coupon})

    @staticmethod
    @parse_params(
        Argument("code", location="json",
                 help="The code of the coupon."),
        Argument("amount", location="json",
                 help="The amount of the coupon."),
        Argument("expires_at", location="json",
                 help="The expires_at of the coupon."),
    )
    def update_coupon(coupon_id, code, amount, expires_at):
        """ Update a copon based on the provided information """
        repository = CouponRepository()
        coupon = repository.update(
            coupon_id=coupon_id, code=code, amount=amount, expires_at=expires_at
        )
        return jsonify({"data": coupon.json})

    @staticmethod
    @parse_params(
        Argument("code", location="json",
                 help="The code of the coupon."),
        Argument("amount", location="json",
                 help="The amount of the coupon."),
        Argument("expires_at", location="json",
                 help="The expires_at of the coupon."),
    )
    def post(amount, code, expires_at):
        """ Create a coupon based on the provided information """
        coupon = CouponRepository.create(
            amount, code, expires_at
        )
        return jsonify({"data": coupon.json})
