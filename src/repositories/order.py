""" Defines the Order repository """
import sys
from sqlalchemy import or_, and_
from models import Order
from utils.errors import DataNotFound, DuplicateData, InternalServerError
from sqlalchemy.exc import IntegrityError, DataError


class OrderRepository:
    """ The repository for the order model """

    @staticmethod
    def get(order_id=None):
        """ Query a payment method by order_id """

        # make sure one of the parameters was passed
        if not order_id:
            raise DataNotFound(f"Order not found, no detail provided")

        try:
            query = Order.query
            if order_id:
                query = query.filter(Order.id == order_id)

            order = query.first()
            return order
        except:
            print(sys.exc_info())
            raise DataNotFound(f"Payment Method with {order_id} not found")

    @staticmethod
    def getAll():
        """ Query all orders"""
        orders = Order.query.all()
        all_orders = [order.json for order in orders]
        return all_orders