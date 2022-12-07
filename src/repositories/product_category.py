""" Defines the Product Category repository """
import sys
from sqlalchemy import or_
from models import ProductCategory, db
from utils.errors import DataNotFound, DuplicateData, InternalServerError
from sqlalchemy.exc import IntegrityError
from flask import jsonify


class ProductCategoryRepository:
    """ The repository for the product category model """

    @staticmethod
    def get(product_category_id=None):
        """ Query a product_category by product_category_id """

        # make sure one of the parameters was passed
        if not product_category_id:
            raise DataNotFound(f"Product category not found, no detail provided")

        try:
            query = ProductCategory.query
            if product_category_id:
                query = query.filter(ProductCategory.id == product_category_id)

            product_category = query.first()
            return product_category
        except DataNotFound as e:
            print(sys.exc_info())
            raise DataNotFound(f"Product Category with {product_category_id} not found")

    @staticmethod
    def getAll():
        """ Query all categories"""
        product_categories = db.session.query(ProductCategory).all()
        
        data = []
        
        for category in product_categories:
            data.append({
                "id": category.id, 
                "name": category.name,
                "sku": category.sku
            })
            
        return data
    
    def update(self, category_id, **args):
        """ Update a category details """
        product_category = self.get(category_id)
        if 'name' in args and args['name'] is not None:
            product_category.name = args['name']

        if 'sku' in args and args['sku'] is not None:
            product_category.sku = args['sku']


        return product_category.save()

    @staticmethod
    def create(name, sku):
        """ Create a new category """
        try:
            new_product_category = ProductCategory(name=name, sku=sku)

            return new_product_category.save()

        except IntegrityError as e:
            message = e.orig.diag.message_detail
            raise DuplicateData(message)
        except Exception:
            raise InternalServerError
        
    @staticmethod
    def delete(category_id):
        """ Delete a product by product_id """

        # make sure product_id was passed
        if not category_id:
            raise DataNotFound(f"Category not found, no detail provided")

        try:
            query = ProductCategory.query.filter(ProductCategory.id == category_id)

            category = query.first()
            return category.delete()
        except DataNotFound as e:
            print(sys.exc_info())
            raise DataNotFound(f"Category with {category_id} not found")\

