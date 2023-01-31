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
    def get_one(payment_id):
        """ Return a payment detail key information based on payment_id """

        try:
            payment_detail = PaymentDetailRepository.get(payment_id=payment_id)
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

    @staticmethod
    @parse_params(
        Argument("payment_id", location="json",
                 help="The payment_id of the payment."),
        Argument("amount", location="json",
                 help="The amount of the payment."),
        Argument("status", location="json",
                 help="The status of the payment."),
        Argument("orders_id", location="json",
                 help="The orders_id of the payment."),
        Argument("payment_methods_id", location="json",
                 help="The payment_methods_id of the payment."),
    )
    def update(payment_id, amount, status, orders_id, payment_methods_id):
        """ Update a payment details """
        order = PaymentDetailRepository().update(
            payment_id=payment_id,
            amount=amount,
            status=status,
            orders_id=orders_id,
            payment_methods_id=payment_methods_id,
        )
        return jsonify({"data": order.json})

    @staticmethod
    @parse_params(
        Argument("amount", location="json",
                 help="The amount of the payment."),
        Argument("status", location="json",
                 help="The status of the payment."),
        Argument("orders_id", location="json",
                 help="The orders_id of the payment."),
        Argument("payment_methods_id", location="json",
                 help="The payment_methods_id of the payment."),
    )
    def post(amount, status, orders_id, payment_methods_id):
        """ Create an order detail """
        payment = PaymentDetailRepository.create(
            amount=amount,
            status=status,
            orders_id=orders_id,
            payment_methods_id=payment_methods_id,
        )
        return jsonify({"data": payment.json})

    def delete(payment_id):
        """ delete a payment via the provided id """
        PaymentDetailRepository.delete(payment_id=payment_id)
        return jsonify({"message": "payment successfully deleted"})
