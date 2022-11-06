""" Defines the Payment Detail repository """
import sys
from sqlalchemy import or_, and_
from models import PaymentDetail
from utils.errors import DataNotFound, DuplicateData, InternalServerError
from sqlalchemy.exc import IntegrityError, DataError


class PaymentDetailRepository:
    """ The repository for the payment detail model """

    @staticmethod
    def get(detail_id=None):
        """ Query a payment detail by detail_id """

        # make sure one of the parameters was passed
        if not detail_id:
            raise DataNotFound(f"Payment Detail not found, no detail provided")

        try:
            query = PaymentDetail.query
            if detail_id:
                query = query.filter(PaymentDetail.id == detail_id)

            payment_detail = query.first()
            return payment_detail
        except:
            print(sys.exc_info())
            raise DataNotFound(f"Payment Detail with {detail_id} not found")

    @staticmethod
    def getAll():
        """ Query all payment details"""
        payment_details = PaymentDetail.query.all()
        all_payment_details = [payment_detail.json for payment_detail in payment_details]
        return all_payment_details

