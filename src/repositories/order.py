""" Defines the Order repository """
import sys
from sqlalchemy import or_, and_
from models import Order, db
from utils.errors import DataNotFound, DuplicateData, InternalServerError
from sqlalchemy.exc import IntegrityError, DataError


class OrderRepository:
    """ The repository for the order model """

    @staticmethod
    def get(order_id):
        """ Query a payment method by order_id """

        # make sure one of the parameters was passed
        if not order_id:
            raise DataNotFound(f"Order not found, no detail provided")

        try:
            order = db.session.query(Order).filter(
                Order.id == order_id).first()
            return order
        except:
            print(sys.exc_info())
            raise DataNotFound(f"Order with {order_id} not found")

    @staticmethod
    def getAll():
        """ Query all orders"""
        orders = db.session.query(Order).all()
        data = []
        for order in orders:
            data.append({
                "id": order.id,
                "tax": order.tax,
                "total_cost": order.total_cost,
                "delivery_status": order.delivery_status,
                "delivered_at": order.delivered_at,
                "customer_id": order.customer_id,
                "coupon_id": order.coupon_id,
                "shipping_address_id": order.shipping_address_id,
                "seller_id": order.seller_id,
            })

        return data

    def update(self, order_id, **args):
        """ Update a order details"""
        order = self.get(order_id)
        if not order:
            raise DataNotFound(f"Order Detail with {order_id} not found")
        if 'total_cost' in args and args['total_cost'] is not None:
            order.total_cost = args['total_cost']
        if 'tax' in args and args['tax'] is not None:
            order.tax = args['tax']
        if 'delivery_status' in args and args['delivery_status'] is not None:
            order.delivery_status = args['delivery_status']
        if 'delivered_at' in args and args['delivered_at'] is not None:
            order.delivered_at = args['delivered_at']
        return order.save()

    @staticmethod
    def create(total_cost, tax, delivery_status, delivered_at, customer_id, shipping_address_id, coupon_id, seller_id):
        """ Create a new order Details """
        try:
            order_detail = Order(total_cost=total_cost,
                                 tax=tax,
                                 delivery_status=delivery_status,
                                 delivered_at=delivered_at,
                                 customer_id=customer_id,
                                 shipping_address_id=shipping_address_id,
                                 coupon_id=coupon_id,
                                 seller_id=seller_id,
                                 )
            return order_detail.save()
        except IntegrityError as e:
            message = e.orig.diag.message_detail
            raise DuplicateData(message)
        except Exception:
            raise InternalServerError

    @staticmethod
    def delete(order_id):
        """ Delete a Order by id """
        if not order_id:
            raise DataNotFound(f"Order not found")

        try:
            query = Order.query.filter(Order.id == order_id).first()
            if not query:
                raise DataNotFound(f"Order Detail with {order_id} not found")
            return query.delete()
        except DataNotFound as e:
            print(sys.exc_info())
            raise DataNotFound(f"Order Detail with {order_id} not found")
