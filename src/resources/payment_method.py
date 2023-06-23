"""
Define the resources for the payment method
"""
from flasgger import swag_from
from flask import abort, jsonify
from flask_restful import Resource
from flask_restful.reqparse import Argument

from repositories import PaymentMethodRepository
from utils import parse_params
from utils.errors import DataNotFound
from validators.auth import requires_auth


class PaymentMethodResource(Resource):
    """ methods relative to the payment method """

    @staticmethod
    @swag_from("../swagger/payment_method/get_one.yml")
    @requires_auth('get:payment_method')
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
    @requires_auth('get:payment_methods')
    def get_all():
        """ Return all payment method key information based on the query parameter """
        payment_methods = PaymentMethodRepository.getAll()
        return jsonify({"data": payment_methods})

    @staticmethod
    @swag_from("../swagger/payment_method/put.yml")
    @parse_params(
        Argument("name", location="json",
                help="The name of the payment."),
        Argument("currency", location="json",
                help="The currency of the payment."),
    )
    @requires_auth('patch:payment_method')
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
    @swag_from("../swagger/payment_method/post.yml")
    @parse_params(
        Argument("name", location="json",
                help="The name of the payment."),
        Argument("currency", location="json",
                help="The currency of the payment."),
    )
    @requires_auth('post:payment_method')
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

    @swag_from("../swagger/payment_method/delete.yml")
    @requires_auth('delete:payment_method')
    def delete(method_id):
        """ delete a payment via the provided id """
        PaymentMethodRepository.delete(method_id=method_id)
        return jsonify({"message": "payment successfully deleted"})
