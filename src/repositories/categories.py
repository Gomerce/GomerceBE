""" Defines the Categories repository """
import sys
from sqlalchemy import or_, and_
from models import product_category
from utils.errors import DataNotFound, DuplicateData, InternalServerError
from sqlalchemy.exc import IntegrityError, DataError


class CategoriesRepository:
    """ The repository for the categories model """

    @staticmethod
    def get(search_id=None):
        """ Query product by category """
        if not search_id:
            raise DataNotFound(f"can't check for empty category name")

        try:
            query = product_category.query
            if search_id:
                query = query.filter(product_category.id == search_id)

            products = query.products.all()
            all_products = [p.json for p in products]
            return all_products
        except:
            print(sys.exc_info())
            raise DataNotFound(f"category with {search_id} not found")

    @staticmethod
    def getAll():
        """ get all categories"""
        catgories = product_category.query.all()
        all_categories = [c.json for c in catgories]
        return all_categories

    @staticmethod
    def create(name, sku, products):
        """ Create a new category """
        try:
            category = product_category(name=name, sku=sku, products=products)
            return category.save()
        except IntegrityError as e:
            message = e.orig.diag.message_detail
            raise DuplicateData(message)
        except Exception:
            raise InternalServerError
