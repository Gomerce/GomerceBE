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

    @staticmethod
    @parse_params(
        Argument("method_id", location="json",
                 help="The method_id of the payment."),
        Argument("name", location="json",
                 help="The name of the payment."),
        Argument("currency", location="json",
                 help="The currency of the payment."),
    )
    def update(method_id, name, currency):
        """ Update a payment method """
        order = PaymentMethodRepository().update(
            method_id=method_id,
            name=name,
            currency=currency,
        )
        return jsonify({"data": order.json})

    @staticmethod
    @parse_params(
        Argument("name", location="json",
                 help="The name of the payment."),
        Argument("currency", location="json",
                 help="The currency of the payment."),
    )
    def post(name, currency):
        """ Create an order detail """
        payment = PaymentMethodRepository.create(
            name=name,
            currency=currency
        )
        return jsonify({"data": payment.json})

    def delete(method_id):
        """ delete a payment via the provided id """
        PaymentMethodRepository.delete(method_id=method_id)
        return jsonify({"message": "payment successfully deleted"})
