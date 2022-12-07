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
            return order_detail
        except:
            print(sys.exc_info())
            raise DataNotFound(f"Order Detail with {detail_id} not found")

    @staticmethod
    def getAll():
        """ Query all order details"""
        order_details = OrderDetail.query.all()
        all_order_details = [order_detail.json for order_detail in order_details]
        return all_order_details

