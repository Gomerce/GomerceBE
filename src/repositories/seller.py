""" Defines the Customer repository """
import sys
from sqlalchemy import or_
from models import Seller
from utils.errors import DataNotFound, DuplicateData, InternalServerError
from sqlalchemy.exc import IntegrityError


class SellerRepository:
    """ The repository for the seller model """

    @staticmethod
    def get(seller_id=None, username=None, email=None):
        """ Query a seller by seller_id """

        # make sure one of the parameters was passed
        if not seller_id and not username and not email:
            raise DataNotFound(f"Seller not found, no detail provided")

        try:
            query = Seller.query
            if seller_id:
                query = query.filter(Seller.id == seller_id)
            if username:
                query = query.filter(
                    or_(
                        Seller.username == username,
                        Seller.email == username
                    ))
            if email:
                query = query.filter(
                    or_(Seller.email == email, Seller.username == email))

            seller = query.first()
            return seller
        except DataNotFound as e:
            print(sys.exc_info())
            raise DataNotFound(f"Seller with {seller_id} not found")

    @staticmethod
    def getAll():
        """ Query all sellers"""
        sellers = Seller.query.all()
        all_sellers = [seller.json for seller in sellers]
        return all_sellers

    def update(self, seller_id, **args):
        """ Update a seller's details """
        seller = self.get(seller_id)
        if 'phone' in args and args['phone'] is not None:
            seller.phone = args['phone']

        if 'email' in args and args['email'] is not None:
            seller.email = args['email']

        if 'last_name' in args and args['last_name'] is not None:
            seller.last_name = args['last_name']

        if 'first_name' in args and args['first_name'] is not None:
            seller.first_name = args['first_name']

        if 'rating' in args and args['rating'] is not None:
            seller.rating = args['rating']

        return seller.save()

    @staticmethod
    def create(username, last_name, first_name, email, password, phone=None):
        """ Create a new seller """
        try:
            new_seller = Seller(username=username, first_name=first_name,
                                last_name=last_name, email=email, phone=phone)
            new_seller.set_password(password)

            return new_seller.save()
        except IntegrityError as e:
            message = e.orig.diag.message_detail
            raise DuplicateData(message)
        except Exception:
            raise InternalServerError

    @staticmethod
    def delete(seller_id):
        """ Delete a seller by seller_id """

        # make sure seller_id was passed
        if not seller_id:
            raise DataNotFound(f"Seller not found, no detail provided")

        try:
            query = Seller.query.filter(Seller.id == seller_id)

            seller = query.first()
            return seller.delete()
        except DataNotFound as e:
            print(sys.exc_info())
            raise DataNotFound(f"Seller with {seller_id} not found")\
