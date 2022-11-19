""" Defines the Payment Method repository """
import sys
from sqlalchemy import or_, and_
from models import PaymentMethod
from utils.errors import DataNotFound, DuplicateData, InternalServerError
from sqlalchemy.exc import IntegrityError, DataError


class PaymentMethodRepository:
    """ The repository for the payment method model """

    @staticmethod
    def get(method_id=None):
        """ Query a payment method by method_id """

        # make sure one of the parameters was passed
        if not method_id:
            raise DataNotFound(f"Payment Method not found, no detail provided")

        try:
            query = PaymentMethod.query
            if method_id:
                query = query.filter(PaymentMethod.id == method_id)

            payment_method = query.first()
            return payment_method
        except:
            print(sys.exc_info())
            raise DataNotFound(f"Payment Method with {method_id} not found")

    @staticmethod
    def getAll():
        """ Query all payment methods"""
        payment_methods = PaymentMethod.query.all()
        all_payment_methods = [payment_method.json for payment_method in payment_methods]
        return all_payment_methods

