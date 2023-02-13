""" Defines the Order Detail repository """
import sys
from sqlalchemy import or_, and_
from models import OrderDetail
from utils.errors import DataNotFound, DuplicateData, InternalServerError
from sqlalchemy.exc import IntegrityError, DataError


class OrderDetailRepository:
    """ The repository for the order detail model """

    @staticmethod
    def get(detail_id=None):
        """ Query a order detail by detail_id """

        # make sure one of the parameters was passed
        if not detail_id:
            raise DataNotFound(f"Order Detail not found, no detail provided")

        try:
            query = OrderDetail.query
            if detail_id:
                query = query.filter(OrderDetail.id == detail_id)

            order_detail = query.first()
            if order_detail:
                return {}
            return order_detail
        except:
            print(sys.exc_info())
            raise DataNotFound(f"Order Detail with {detail_id} not found")

    @staticmethod
    def getAll():
        """ Query all order details"""
        order_details = OrderDetail.query.all()
        data = []
        for order in order_details:
            data.append({
                "id": order.id,
                "sku": order.sku,
                "created_at": order.created_at,
                "updated_at": order.updated_at,
                "orders_id": order.orders_id,
                "products_id": order.products_id,
                "statuses_id": order.statuses_id,
            })

        return data

    def update(self, detail_id, **args):
        """ Update a order details"""
        order_details = self.get(detail_id)
        if not order_details:
            raise DataNotFound(f"Order Detail with {detail_id} not found")
        if 'sku' in args and args['sku'] is not None:
            order_details.sku = args['sku']

        if 'statuses_id' in args and args['statuses_id'] is not None:
            order_details.statuses_id = args['statuses_id']

        if 'products_id' in args and args['products_id'] is not None:
            order_details.products_id = args['products_id']
        return order_details.save()

    @staticmethod
    def create(sku, orders_id, products_id, statuses_id):
        """ Create a new Order Details """
        try:
            order_detail = OrderDetail(sku=sku, orders_id=orders_id,
                                       products_id=products_id,
                                       statuses_id=statuses_id,
                                       )
            return order_detail.save()
        except IntegrityError as e:
            message = e.orig.diag.message_detail
            raise DuplicateData(message)
        except Exception as err:
            print(err)
            raise InternalServerError

    @staticmethod
    def delete(detail_id):
        """ Delete a OrderDetail by id """
        if not detail_id:
            raise DataNotFound(f"OrderDetail not found")

        try:
            query = OrderDetail.query.filter(
                OrderDetail.id == detail_id).first()
            if not query:
                raise DataNotFound(f"Order Detail with {detail_id} not found")
            return query.delete()
        except DataNotFound as e:
            print(sys.exc_info())
            raise DataNotFound(
                f"Order Detail with {detail_id} not found")
