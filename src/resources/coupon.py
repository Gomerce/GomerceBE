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
from validators.auth import requires_auth


class CouponResource(Resource):
    """ coupon functionalities """

    @staticmethod
    @swag_from("../swagger/coupon/get_one.yml")
    @requires_auth('get:coupon')
    def get_one(coupon_id):
        """ Return a coupon based on id provided"""
        try:
            coupon = CouponRepository.get_one(coupon_id=coupon_id)
            if not coupon:
                return jsonify({"message": f" coupon with the id {coupon_id} not found"})
            data = {
                "id": coupon.id,
                "code": coupon.code,
                "amount": coupon.amount,
                "expires_at": coupon.expires_at,
                "created_at": coupon.created_at,
                "updated_at": coupon.updated_at,
            }
            return jsonify({"data": data})
        except DataNotFound as e:
            abort(404, e.message)
        except Exception:
            abort(500)

    @staticmethod
    @swag_from("../swagger/coupon/get_all.yml")
    @requires_auth('get:coupons')
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
    @swag_from("../swagger/coupon/put.yml")
    @requires_auth('patch:coupon')
    def update_coupon(coupon_id, code, amount, expires_at):
        """ Update a copon """
        repo = CouponRepository()
        coupon = repo.update(
            coupon_id=coupon_id, code=code, amount=amount, expires_at=expires_at
        )
        data = {
            "id": coupon.id,
            "code": coupon.code,
            "amount": coupon.amount,
            "expires_at": coupon.expires_at,
            "created_at": coupon.created_at,
            "updated_at": coupon.updated_at,
        }

        return jsonify({"data": data})

    @staticmethod
    @parse_params(
        Argument("code", location="json",
                 help="The code of the coupon."),
        Argument("amount", location="json",
                 help="The amount of the coupon."),
        Argument("expires_at", location="json",
                 help="The expires_at of the coupon."),
    )
    @swag_from("../swagger/coupon/post.yml")
    @requires_auth('post:coupon')
    def post(amount, code, expires_at):
        """ Create a coupon based on the provided information """
        coupon = CouponRepository.create(
            amount, code, expires_at
        )
        return jsonify({"data": coupon.json})

    @swag_from("../swagger/coupon/delete.yml")
    @requires_auth('delete:coupon')
    def delete(coupon_id):
        """ delete a coupoun via the provided id """
        CouponRepository.delete(coupon_id=coupon_id)
        return jsonify({"message": "coupon successfully deleted"})
