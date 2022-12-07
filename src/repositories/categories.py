""" Defines the Categories repository """
import sys
from sqlalchemy import or_, and_
from models import ProductCategory
from utils.errors import DataNotFound, DuplicateData, InternalServerError
from sqlalchemy.exc import IntegrityError, DataError


class CategoriesRepository:
    """ The repository for the categories model """

    @staticmethod
    def get(category_id, name=None, sku=None):
        """ Query product by category """
        if not category_id and not name and not sku:
            raise DataNotFound(f"can't check for empty category name")

        try:
            query = ProductCategory.query
            if category_id:
                query = query.filter(ProductCategory.id == category_id)

            if name:
                query = query.filter(
                    or_(ProductCategory.name == name, ProductCategory.sku == name))

            if sku:
                query = query.filter(
                    or_(ProductCategory.sku == sku, ProductCategory.name == sku))

            products = query.products.all()
            all_products = [p.json for p in products]
            return all_products
        except:
            print(sys.exc_info())
            raise DataNotFound(f"category with {name} not found")

    @staticmethod
    def getAll():
        """ Query all category"""
        categories = ProductCategory.query.all()
        all_categories = [cat.json for cat in categories]
        return all_categories

    def update(self, category_id, **args):
        """ Update a category's age """
        category = self.get(category_id)
        if 'name' in args and args['name'] is not None:
            category.name = args['name']

        if 'sku' in args and args['sku'] is not None:
            category.sku = args['sku']
        return category.save()

    @staticmethod
    def create(name, sku):
        """ Create a new category """
        try:
            category = ProductCategory(name=name, sku=sku)
            return category.save()
        except IntegrityError as e:
            message = e.orig.diag.message_detail
            raise DuplicateData(message)
        except Exception:
            raise InternalServerError
