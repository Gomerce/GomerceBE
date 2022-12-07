"""
Define the resources for the payment details
"""
from flask import jsonify, abort
from flasgger import swag_from
from flask_restful import Resource
from flask_restful.reqparse import Argument
from repositories import PaymentDetailRepository
from utils import parse_params
from utils.errors import DataNotFound


class PaymentDetailResource(Resource):
    """ methods relative to the payment detail """

    @staticmethod
    @swag_from("../swagger/payment_detail/get_one.yml")
    def get_one(detail_id):
        """ Return a payment detail key information based on detail_id """

        try:
            payment_detail = PaymentDetailRepository.get(detail_id=detail_id)
            return jsonify({"data": payment_detail.json})
        except DataNotFound as e:
            abort(404, e.message)
        except Exception:
            abort(500)

    @staticmethod
    @swag_from("../swagger/payment_detail/get_all.yml")
    def get_all():
        """ Return all payment detail key information based on the query parameter """
        payment_details = PaymentDetailRepository.getAll()
        return jsonify({"data": payment_details})
