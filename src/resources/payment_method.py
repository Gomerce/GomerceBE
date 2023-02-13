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
            data = {
                "id": payment_method.id,
                "name": payment_method.name,
                "currency": payment_method.currency,
            }
            return jsonify({"data": data})
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
        print(order)
        return jsonify({"message": f"data updated"})

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
        data = {
            "id": payment.id,
            "name": payment.name,
            "currency": payment.currency,
        }
        return jsonify({"data": data})

    def delete(method_id):
        """ delete a payment via the provided id """
        PaymentMethodRepository.delete(method_id=method_id)
        return jsonify({"message": "payment successfully deleted"})
