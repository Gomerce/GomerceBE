""" Defines the Customer repository """
import sys
from sqlalchemy import or_
from models import Product
from utils.errors import DataNotFound, DuplicateData, InternalServerError
from sqlalchemy.exc import IntegrityError


class ProductRepository:
    """ The repository for the product model """

    @staticmethod
    def get(product_id=None):
        """ Query a product by product_id """

        # make sure one of the parameters was passed
        if not product_id:
            raise DataNotFound(f"Product not found, no detail provided")

        try:
            query = Product.query
            if product_id:
                query = query.filter(Product.id == product_id)

            product = query.first()
            return product
        except DataNotFound as e:
            print(sys.exc_info())
            raise DataNotFound(f"Product with {product_id} not found")

    @staticmethod
    def getAll():
        """ Query all products"""
        products = Product.query.all()
        all_products = [product.json for product in products]
        return all_products

   
