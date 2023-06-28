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
from validators.auth import requires_auth


class OrderDetailResource(Resource):
    """ methods relative to the order detail """

    @staticmethod
    @swag_from("../swagger/order_detail/get_one.yml")
    @requires_auth('get:order_detail')
    def get_one(detail_id):
        """ Return an order key information based on order_id """

        try:
            order_detail = OrderDetailRepository.get(detail_id=detail_id)
            if not order_detail:
                return jsonify({"message": f" Order with the id {detail_id} not found"})
            print(order_detail)
            data = {
                "id": order_detail.id,
                "sku": order_detail.sku,
                "created_at": order_detail.created_at,
                "updated_at": order_detail.updated_at,
                "orders_id": order_detail.orders_id,
                "products_id": order_detail.products_id,
                "statuses_id": order_detail.statuses_id,
            }
            return jsonify({"data": data})
        except DataNotFound as e:
            abort(404, e.message)
        except Exception:
            abort(500)

    @staticmethod
    @swag_from("../swagger/order_detail/get_all.yml")
    @requires_auth('get:order_details')
    def get_all():
        """ Return all order detail key information based on the query parameter """
        order_details = OrderDetailRepository.getAll()
        return jsonify({"data": order_details})

    @staticmethod
    @parse_params(
        Argument("sku", location="json",
                 help="The sku of the order."),
        Argument("order_id", location="json",
                 help="The order_id of the order."),
        Argument("products_id", location="json",
                 help="The products_id of the order."),
        Argument("statuses_id", location="json",
                 help="The statuses of the order."),
    )
    @swag_from("../swagger/order_detail/put.yml")
    @requires_auth('patch:order_detail')
    def update(detail_id, sku, order_id, products_id, statuses_id):
        """ Update a order """
        order = OrderDetailRepository().update(
            detail_id=detail_id,
            sku=sku, order_id=order_id,
            products_id=products_id,
            statuses_id=statuses_id
        )

        data = {
            "id": order.id,
            "sku": order.sku,
            "created_at": order.created_at,
            "updated_at": order.updated_at,
            "orders_id": order.orders_id,
            "products_id": order.products_id,
            "statuses_id": order.statuses_id,
        }
        return jsonify({"data": data})

    @staticmethod
    @parse_params(
        Argument("sku", location="json",
                 help="The sku of the order."),
        Argument("products_id", location="json",
                 help="The products_id of the order."),
        Argument("orders_id", location="json",
                 help="The order of the order."),
        Argument("statuses_id", location="json",
                 help="The statuses of the order."),
    )
    @swag_from("../swagger/order_detail/post.yml")
    @requires_auth('post:order_detail')
    def post(sku, orders_id, products_id, statuses_id):
        """ Create an order detail """

        order = OrderDetailRepository.create(
            sku=sku, orders_id=orders_id,
            products_id=products_id,
            statuses_id=statuses_id,
        )
        data = {
            "id": order.id,
            "sku": order.sku,
            "created_at": order.created_at,
            "updated_at": order.updated_at,
            "orders_id": order.orders_id,
            "products_id": order.products_id,
            "statuses_id": order.statuses_id,
        }
        return jsonify({"data": data})

    @swag_from("../swagger/order_detail/delete.yml")
    @requires_auth('delete:order_detail')
    def delete(detail_id):
        """ delete a order via the provided id """
        OrderDetailRepository.delete(detail_id=detail_id)
        return jsonify({"message": "order successfully deleted"})
