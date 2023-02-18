""" Defines the Seller repository """
import sys
from sqlalchemy import or_, and_
from flask import jsonify
from models import Seller
from utils.errors import DataNotFound, DuplicateData, InternalServerError
from sqlalchemy.exc import IntegrityError, DataError


class SellerRepository:
    """ The repository for the sellers model """

    @staticmethod
    def get(id=None):
        """ get seller by id """
        if not id:
            raise DataNotFound(f"can't check for empty seller id")

        try:
            query = Seller.query
            if id:
                query = query.filter(Seller.id == id)
            seller = query.first()
            return seller
        except:
            print(sys.exc_info())
            raise DataNotFound(f"seller with {id} not found")

    @staticmethod
    def getAll():
        """ get all seller"""
        sellers = Seller.query.all()
        all_sellers = [s.json for s in sellers]
        return all_sellers

    @staticmethod
    def create(username, last_name, first_name, email, password, phone=None):
        """ Create a new seller """
        try:
            created_seller = Seller(username=username, first_name=first_name,
                                last_name=last_name, email=email, phone=phone)
            created_seller.set_password(password)

            if len(password) < 6:
                return jsonify({"error": "Password must be at least 6 characters"}), 400

            seller = created_seller.save()

        except IntegrityError as e:
            message = e.orig.diag.message_detail
            raise DuplicateData(message)
        except Exception:
            raise InternalServerError

        return jsonify({
            "seller": seller.username,
            "email": seller.email,
            "firstName": seller.first_name,
            "lastName": seller.last_name,
            })

    def update(self, seller_id, **args):
        """ Update a seller's informations """
        seller = self.get(seller_id)
        if 'last_name' in args and args['last_name'] is not None:
            seller.last_name = args['last_name']

        if 'first_name' in args and args['first_name'] is not None:
            seller.first_name = args['first_name']

        if 'phone' in args and args['phone'] is not None:
            seller.phone = args['phone']

        if 'email' in args and args['email'] is not None:
            seller.email = args['email']

        if 'rating' in args and args['rating'] is not None:
            seller.rating = args['rating']

        return seller.save()

    @staticmethod
    def delete(seller_id):
        """ Delete a seller by seller_id """
        if not seller_id:
            raise DataNotFound(f"Seller not found, no id provided")

        try:
            query = Seller.query.filter(Seller.id == seller_id)

            seller = query.first()
            return seller.delete()
        except DataNotFound as e:
            print(sys.exc_info())
            raise DataNotFound(f"Seller with {seller_id} not found")\
