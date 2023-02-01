""" Defines the Payment Method repository """
import sys
from sqlalchemy import or_, and_
from models import PaymentMethod, db
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

            return query.first()
        except:
            print(sys.exc_info())
            raise DataNotFound(f"Payment Method with {method_id} not found")

    @staticmethod
    def getAll():
        """ Query all payment methods"""
        payment_methods = db.session.query(PaymentMethod).all()
        data = []
        for pay in payment_methods:
            data.append({
                "id": pay.id,
                "name": pay.name,
                "currency": pay.currency,
                "created_at": pay.created_at,
                "updated_at": pay.updated_at,
            })

        return data

    def update(self, method_id, **args):
        """ Update a Payment Method"""
        pay_method = self.get(method_id)
        if 'name' in args and args['name'] is not None:
            pay_method.name = args['name']
        if 'currency' in args and args['currency'] is not None:
            pay_method.currency = args['currency']
        return db.session().commit()

    @staticmethod
    def create(name, currency):
        """ Create a new payment method """
        try:

            pay_method = PaymentMethod(name=name, currency=currency)
            db.session.add(pay_method)
            db.session.commit()
            return pay_method
        except IntegrityError as e:
            message = e.orig.diag.message_detail
            raise DuplicateData(message)
        except Exception:
            raise InternalServerError

    @staticmethod
    def delete(method_id):
        """ Delete Payment Method by id """
        if not method_id:
            raise DataNotFound(f"Payment Method not found")

        try:
            query = PaymentMethod.query.filter(
                PaymentMethod.id == method_id).first()
            if not query:
                raise DataNotFound(
                    f"Payments Method with {method_id} not found")
            db.session.delete(query)
            db.session.commit()
            return query
        except DataNotFound as e:
            print(sys.exc_info())
            raise DataNotFound(f"Payment Method with {method_id} not found")
