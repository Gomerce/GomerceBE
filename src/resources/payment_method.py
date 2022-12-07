"""
Define the resources for the payment method
"""
from flask import jsonify, abort
from flasgger import swag_from
from flask_restful import Resource
from flask_restful.reqparse import Argument
from repositories import PaymentMethodRepository
from utils import parse_params
from utils.errors import DataNotFound


class PaymentMethodResource(Resource):
    """ methods relative to the payment method """

    @staticmethod
    @swag_from("../swagger/payment_method/get_one.yml")
    def get_one(method_id):
        """ Return a payment method key information based on method_id """

        try:
            payment_method = PaymentMethodRepository.get(method_id=method_id)
            return jsonify({"data": payment_method.json})
        except DataNotFound as e:
            abort(404, e.message)
        except Exception:
            abort(500)

    @staticmethod
    @swag_from("../swagger/payment_method/get_all.yml")
    def get_all():
        """ Return all payment method key information based on the query parameter """
        payment_methods = PaymentMethodRepository.getAll()
        return jsonify({"data": payment_methods})
