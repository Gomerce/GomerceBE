"""
Define the resources for the order
"""
from flask import jsonify, abort
from flasgger import swag_from
from flask_restful import Resource
from flask_restful.reqparse import Argument
from repositories import OrderRepository
from utils import parse_params
from utils.errors import DataNotFound


class OrderResource(Resource):
    """ methods relative to the order """

    @staticmethod
    @swag_from("../swagger/order/get_one.yml")
    def get_one(order_id):
        """ Return an order key information based on order_id """

        try:
            order = OrderRepository.get(order_id=order_id)
            return jsonify({"data": order.json})
        except DataNotFound as e:
            abort(404, e.message)
        except Exception:
            abort(500)

    @staticmethod
    @swag_from("../swagger/order/get_all.yml")
    def get_all():
        """ Return all order key information based on the query parameter """
        orders = OrderRepository.getAll()
        return jsonify({"data": orders})
