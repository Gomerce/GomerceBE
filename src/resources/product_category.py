"""
Define the resources for the product categories
"""
from flask import jsonify, abort
from flasgger import swag_from
from flask_restful import Resource
from flask_restful.reqparse import Argument
from repositories import ProductCategoryRepository
from utils import parse_params
from utils.errors import DataNotFound


class ProductCategoryResource(Resource):
    """ methods relative to the product Category """

    @staticmethod
    @swag_from("../swagger/product_category/get_one.yml")
    def get_one(product_category_id):
        """ Return a product category key information based on product_category_id """

        try:
            category = ProductCategoryRepository.get(product_category_id=product_category_id)
            return jsonify({
                "id": category.id,
                "name": category.name,
                "sku": category.sku
            })
        except DataNotFound as e:
            abort(404, e.message)
        except Exception:
            abort(500)

    @staticmethod
    @swag_from("../swagger/product_categories/get_all.yml")
    def get_all():
        """ Return all categories key information based on the query parameter """
        product_categories = ProductCategoryRepository.getAll()
        return jsonify({"data": product_categories})

    @staticmethod
    @parse_params(
        Argument("name", location="json", required=True,
                 help="The name of the product_category."),
        Argument("sku", location="json", required=True,
                 help="The sku of the product_category.")
    )
    # @swag_from("../swagger/product/POST.yml")
    def post(name, sku):
        """ Create a category based on the provided information """
        # Check duplicates
        product_category = ProductCategoryRepository.create(
            name=name, sku=sku
        )
        return jsonify({"data": product_category.json})
    
    def delete(category_id):
        """ delete a category based on the category id provided """
        # fetch category
        category = ProductCategoryRepository.delete(category_id=category_id)

        return jsonify({"message": "category successfully deleted"})
    
    @staticmethod
    @parse_params(
        Argument("name", location="json", required=True,
                 help="The name of the product_category."),
        Argument("sku", location="json", required=True,
                 help="The sku of the product_category.")
    )
    # @swag_from("../swagger/category/PUT.yml")
    def update_category(category_id, name, sku):
        """ Update a category based on the provided information """
        print(category_id)
        repository = ProductCategoryRepository()
        category = repository.update(
            category_id=category_id, name=name, sku=sku
        )
        return jsonify({"message": category.json})
    
    
