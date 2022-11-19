"""
Define the resources for the categories
"""
from flask import jsonify, abort
from flasgger import swag_from
from flask_restful import Resource
from flask_restful.reqparse import Argument
from repositories import CategoriesRepository
from utils import parse_params
from utils.errors import DataNotFound


class CategoriesResource(Resource):
    """ methods relative to the category """

    @staticmethod    
    @swag_from("../swagger/categories/get_one.yml")
    def get_category_product(search_id):
        """ get product category """

        try:
            products = CategoriesRepository.get(search_id=search_id)
            return jsonify({"data": products.json})
        except DataNotFound as e:
            abort(404, e.message)
        except Exception:
            abort(500)

    @staticmethod  
    @swag_from("../swagger/categories/get_all.yml")  
    def get_all():
        """ get all categories information """
        categories = CategoriesRepository.getAll()
        return jsonify({"data": categories})

    @staticmethod
    # @swag_from("../swagger/categories/post.yml")
    @parse_params(
        Argument("name", location="json",
                 help="The category name"),
        Argument("sku", location="json",
                 help=" the category sku"),
        Argument("products", location="json",
                 help="defines the products of this categories")
    )
    def post(name, sku, products):
        """ Create a category based on the provided information """
        print("i was called")
        category = CategoriesRepository.create(
            name=name,
            sku=sku,
            products=products
        )
        return jsonify({"data": category.json})
