"""
Define the resources for the order detail
"""
from flask import jsonify, abort
from flasgger import swag_from
from flask_restful import Resource
from flask_restful.reqparse import Argument
from repositories import OrderDetailRepository
from utils import parse_params
from utils.errors import DataNotFound


class OrderDetailResource(Resource):
    """ methods relative to the order detail """

    @staticmethod
    @swag_from("../swagger/order_detail/get_one.yml")
    def get_one(detail_id):
        """ Return an order key information based on order_id """

        try:
            order_detail = OrderDetailRepository.get(detail_id=detail_id)
            return jsonify({"data": order_detail.json})
        except DataNotFound as e:
            abort(404, e.message)
        except Exception:
            abort(500)

    @staticmethod
    @swag_from("../swagger/order_detail/get_all.yml")
    def get_all():
        """ Return all order detail key information based on the query parameter """
        order_details = OrderDetailRepository.getAll()
        return jsonify({"data": order_details})
