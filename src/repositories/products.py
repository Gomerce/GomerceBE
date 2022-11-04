""" Defines the product repository """
import sys
from sqlalchemy import or_, and_
from models import Product
from utils.errors import DataNotFound, DuplicateData, InternalServerError
from sqlalchemy.exc import IntegrityError, DataError
class ProductRepository:
    """ The repository for the products model """

    @staticmethod
    def get(id=None):
        """ Query product by id """
        if not id:
            raise DataNotFound(f"can't check for empty product id")

        try:
            query = Product.query
            if id:
                query = query.filter(Product.id == id)
            product = query.first()
            return product
        except:
            print(sys.exc_info())
            raise DataNotFound(f"product with {id} not found")

    
    @staticmethod
    def getAll():
        """ get all product"""
        products = Product.query.all()
        all_products = [product.json for product in products]
        return all_products