""" Defines the Seller repository """
import sys
from sqlalchemy import or_, and_
from models import Seller
from utils.errors import DataNotFound, DuplicateData, InternalServerError
from sqlalchemy.exc import IntegrityError, DataError
class SellerRepository:
    """ The repository for the sellers model """

    @staticmethod
    def get(id=None):
        """ Query seller by id """
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