""" Defines the Coupon repository """
import sys
from sqlalchemy import or_, and_
from models import Coupon
from utils.errors import DataNotFound, DuplicateData, InternalServerError
from sqlalchemy.exc import IntegrityError, DataError


class CouponRepository:
    """ The repository for the Coupon model """

    @staticmethod
    def get_one(coupon_id=None, code=None):
        """ Query a Coupon by coupon_id """

        # ensure that atleast one parameter is passed
        if not coupon_id and not code:
            raise DataNotFound(f"Coupon not found, no detail provided")

        try:
            query = Coupon.query
            if coupon_id:
                query = query.filter(Coupon.id == coupon_id)
            if code:
                query = query.filter(
                    or_(Coupon.code == code, Coupon.id == code))

            coupon = query.first()
            return coupon
        except:
            print(sys.exc_info())
            raise DataNotFound(f"Coupon with {coupon_id} not found")

    @staticmethod
    def get_all():
        """ Query all Coupons"""
        coupons = Coupon.query.all()
        data = []
        for coup in coupons:
            data.append({
                "id": coup.id,
                "code": coup.code,
                "amount": coup.amount,
                "expires_at": coup.expires_at,
                "created_at": coup.created_at,
                "updated_at": coup.updated_at,
            })

        return data

    def update(self, coupon_id, **args):
        """ Update a Coupon's age """
        Coupon = self.get_one(coupon_id)
        if not Coupon:
            raise DataNotFound(f"Coupon Detail with {coupon_id} not found")

        if 'code' in args and args['code'] is not None:
            Coupon.code = args['code']

        if 'amount' in args and args['amount'] is not None:
            Coupon.amount = args['amount']

        if 'expires_at' in args and args['expires_at'] is not None:
            Coupon.expires_at = args['expires_at']
        return Coupon.save()

    @staticmethod
    def create(amount, code, expires_at):
        """ Create a new Coupon """
        try:
            new_Coupon = Coupon(amount=amount, code=code,
                                expires_at=expires_at)
            return new_Coupon.save()
        except IntegrityError as e:
            message = e.orig.diag.message_detail
            raise DuplicateData(message)
        except Exception:
            raise InternalServerError

    @staticmethod
    def delete(coupon_id):
        """ Delete a coupoun by id """
        if not coupon_id:
            raise DataNotFound(f"Coupon not found")

        try:
            query = Coupon.query.filter(Coupon.id == coupon_id).first()
            if not query:
                raise DataNotFound(f"Coupon Detail with {coupon_id} not found")
            return query.delete()
        except DataNotFound as e:
            print(sys.exc_info())
            raise DataNotFound(f"Store with {coupon_id} not found")
