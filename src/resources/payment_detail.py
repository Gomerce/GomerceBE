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
from validators.auth import requires_auth


class PaymentDetailResource(Resource):
    """ methods relative to the payment detail """

    @staticmethod
    @swag_from("../swagger/payment_detail/get_one.yml")
    @requires_auth('get:payment_detail')
    def get_one(payment_id):
        """ Return a payment detail key information based on payment_id """

        try:
            payment_detail = PaymentDetailRepository.get(payment_id=payment_id)
            if not payment_detail:
                return jsonify({"message": f" Payment Details with the id {payment_id} not found"})
            data = {
                "id": payment_detail.id,
                "amount": payment_detail.amount,
                "status": payment_detail.status,
                "created_at": payment_detail.created_at,
                "updated_at": payment_detail.updated_at,
                "orders_id": payment_detail.orders_id,
                "payment_methods_id": payment_detail.payment_methods_id,
            }
            return jsonify({"data": data})
        except DataNotFound as e:
            abort(404, e.message)
        except Exception:
            abort(500)

    @staticmethod
    @swag_from("../swagger/payment_detail/get_all.yml")
    @requires_auth('get:payment_details')
    def get_all():
        """ Return all payment detail key information based on the query parameter """
        payment_details = PaymentDetailRepository.getAll()
        return jsonify({"data": payment_details})

    @staticmethod
    @swag_from("../swagger/payment_detail/put.yml")
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
    @requires_auth('patch:payment_detail')
    def update(payment_id, amount, status, orders_id, payment_methods_id):
        """ Update a payment details """
        order = PaymentDetailRepository().update(
            payment_id=payment_id,
            amount=amount,
            status=status,
            orders_id=orders_id,
            payment_methods_id=payment_methods_id,
        )
        data = {
            "id": order.id,
            "amount": order.amount,
            "status": order.status,
            "created_at": order.created_at,
            "updated_at": order.updated_at,
            "orders_id": order.orders_id,
            "payment_methods_id": order.payment_methods_id,
        }
        return jsonify({"data": data})

    @staticmethod
    @swag_from("../swagger/payment_detail/post.yml")
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
    @requires_auth('post:payment_detail')
    def post(amount, status, orders_id, payment_methods_id):
        """ Create an order detail """
        payment = PaymentDetailRepository.create(
            amount=amount,
            status=status,
            orders_id=orders_id,
            payment_methods_id=payment_methods_id,
        )
        data = {
            "id": payment.id,
            "amount": payment.amount,
            "status": payment.status,
            "created_at": payment.created_at,
            "updated_at": payment.updated_at,
            "orders_id": payment.orders_id,
            "payment_methods_id": payment.payment_methods_id,
        }
        return jsonify({"data": data})

    @swag_from("../swagger/payment_detail/delete.yml")
    @requires_auth('delete:payment_detail')
    def delete(payment_id):
        """ delete a payment via the provided id """
        PaymentDetailRepository.delete(payment_id=payment_id)
        return jsonify({"message": "payment successfully deleted"})
