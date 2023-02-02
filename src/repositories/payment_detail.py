""" Defines the Payment Detail repository """
import sys
from sqlalchemy import or_, and_
from models import PaymentDetail
from utils.errors import DataNotFound, DuplicateData, InternalServerError
from sqlalchemy.exc import IntegrityError, DataError


class PaymentDetailRepository:
    """ The repository for the payment detail model """

    @staticmethod
    def get(payment_id=None):
        """ Query a payment detail by payment_id """

        # make sure one of the parameters was passed
        if not payment_id:
            raise DataNotFound(f"Payment Detail not found, no detail provided")

        try:
            query = PaymentDetail.query
            if query:
                query = query.filter(PaymentDetail.id == payment_id)

            payment_detail = query.first()
            return payment_detail
        except:
            print(sys.exc_info())
            raise DataNotFound(f"Payment Detail with {payment_id} not found")

    @staticmethod
    def getAll():
        """ Query all payment details"""
        payment_details = PaymentDetail.query.all()
        data = []
        for pay in payment_details:
            data.append({
                "id": pay.id,
                "amount": pay.amount,
                "status": pay.status,
                "created_at": pay.created_at,
                "updated_at": pay.updated_at,
                "orders_id": pay.orders_id,
                "payment_methods_id": pay.payment_methods_id,
            })
        return data

    def update(self, payment_id, **args):
        """ Update a Payment details"""
        payment = self.get(payment_id)
        if 'amount' in args and args['amount'] is not None:
            payment.amount = args['amount']
        if 'status' in args and args['status'] is not None:
            payment.status = args['status']
        if 'orders_id' in args and args['orders_id'] is not None:
            payment.orders_id = args['orders_id']
        if 'payment_methods_id' in args and args['payment_methods_id'] is not None:
            payment.payment_methods_id = args['payment_methods_id']
        return payment.save()

    @staticmethod
    def create(amount, status, orders_id, payment_methods_id):
        """ Create a new payment Details """
        try:
            payment_detail = PaymentDetail(amount=amount,
                                           status=status,
                                           orders_id=orders_id,
                                           payment_methods_id=payment_methods_id,
                                           )
            return payment_detail.save()
        except IntegrityError as e:
            message = e.orig.diag.message_detail
            raise DuplicateData(message)
        except Exception:
            raise InternalServerError

    @staticmethod
    def delete(payment_id):
        """ Delete Payment Detail by id """
        if not payment_id:
            raise DataNotFound(f"PaymentDetail not found")

        try:
            query = PaymentDetail.query.filter(
                PaymentDetail.id == payment_id).first()
            if not query:
                raise DataNotFound(
                    f"Payments Detail with {payment_id} not found")
            return query.delete()
        except DataNotFound as e:
            print(sys.exc_info())
            raise DataNotFound(f"PaymentDetail with {payment_id} not found")
