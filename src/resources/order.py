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
from validators.auth import requires_auth


class OrderResource(Resource):
    """ methods relative to the order """

    @staticmethod
    @swag_from("../swagger/order/get_one.yml")
    @requires_auth('get:order')
    def get_one(order_id):
        """ Return an order key information based on order_id """

        try:
            order = OrderRepository.get(order_id=order_id)
            if not order:
                return jsonify({"message": f" Order with the id {order_id} not found"})
            data = {
                "id": order.id,
                "tax": order.tax,
                "total_cost": order.total_cost,
                "delivery_status": order.delivery_status,
                "delivered_at": order.delivered_at,
                "customer_id": order.customer_id,
                "coupon_id": order.coupon_id,
                "shipping_address_id": order.shipping_address_id,
                "seller_id": order.seller_id,
            }
            return jsonify({"data": data})
        except DataNotFound as e:
            abort(404, e.message)
        except Exception as err:
            print(err)
            abort(500)

    @staticmethod
    @swag_from("../swagger/order/get_all.yml")
    @requires_auth('get:orders')
    def get_all():
        """ Return all order key information based on the query parameter """
        orders = OrderRepository.getAll()
        return jsonify({"data": orders})

    @staticmethod
    @parse_params(
        Argument("total_cost", location="json",
                 help="The total_cost of the order."),
        Argument("tax", location="json",
                 help="The tax of the order."),
        Argument("delivery_status", location="json",
                 help="The delivery_status of the order."),
        Argument("delivered_at", location="json",
                 help="The order of the order."),
    )
    @swag_from("../swagger/order/put.yml")
    @requires_auth('patch:order')
    def update_order(order_id, total_cost, tax, delivery_status, delivered_at):
        """ Update a order """
        print("printing orders")
        print(order_id)
        repo = OrderRepository()
        order = repo.update(
            order_id=order_id,
            total_cost=total_cost,
            tax=tax,
            delivery_status=delivery_status,
            delivered_at=delivered_at,
        )

        return jsonify({"message": f"order with the id {order_id} updated successfully"})

    @staticmethod
    @parse_params(
        Argument("total_cost", location="json",
                 help="The total_cost of the order."),
        Argument("tax", location="json",
                 help="The tax of the order."),
        Argument("delivery_status", location="json",
                 help="The delivery_status of the order."),
        Argument("delivered_at", location="json",
                 help="The order of the order."),
        Argument("customer_id", location="json",
                 help="The customer_id of the order."),
        Argument("shipping_address_id", location="json",
                 help="The shipping_address_id of the order."),
        Argument("coupon_id", location="json",
                 help="The coupon_id of the order."),
        Argument("seller_id", location="json",
                 help="The seller_id of the order."),
    )
    @swag_from("../swagger/order/post.yml")
    @requires_auth('post:order')
    def post(total_cost, tax, delivery_status, delivered_at,
             customer_id, shipping_address_id, coupon_id, seller_id):
        """ Create an order detail """
        order = OrderRepository.create(
            total_cost=total_cost,
            tax=tax,
            delivery_status=delivery_status,
            delivered_at=delivered_at,
            customer_id=customer_id,
            shipping_address_id=shipping_address_id,
            coupon_id=coupon_id,
            seller_id=seller_id,
        )
        data = {
            "tax": order.tax,
            "total_cost": order.total_cost,
            "delivery_status": order.delivery_status,
            "shipping_address_id": order.shipping_address_id,
            "customer_id": order.customer_id,
            "seller_id": order.seller_id,
        }
        return jsonify({"data": data})

    @swag_from("../swagger/order/delete.yml")
    @requires_auth('delete:order')
    def delete(order_id):
        """ delete a order via the provided id """
        OrderRepository.delete(order_id=order_id)
        return jsonify({"message": "order successfully deleted"})
