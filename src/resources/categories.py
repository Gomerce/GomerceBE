"""
Define the resources for the product categories
"""
from flask import jsonify, abort
from flasgger import swag_from
from flask_restful import Resource
from flask_restful.reqparse import Argument
from repositories import CategoriesRepository
from utils import parse_params
from utils.errors import DataNotFound


class CategoriesResource(Resource):
    """ methods relative to the product Category """

    @staticmethod
    @swag_from("../swagger/category/get_one.yml")
    def get_category(category_id):
        """ get product category """
        try:
            category = CategoriesRepository.get(category_id=category_id)
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
    @swag_from("../swagger/category/get_all.yml")
    def get_all():
        """ Return all category key information based on the query parameter """
        categories = CategoriesRepository.getAll()
        return jsonify({"data": categories})

    @staticmethod
    @parse_params(
        Argument("name", location="json", required=True,
                 help="The name of the product_category."),
        Argument("sku", location="json", required=True,
                 help="The sku of the product_category.")
    )
    def update(category_id, name, sku):
        """ Update a category """
        category = CategoriesRepository().update(
            category_id=category_id, name=name, sku=sku
        )
        return jsonify({"message": category.json})

    def delete(category_id):
        """ delete a category"""
        CategoriesRepository.delete(category_id=category_id)
        return jsonify({"message": "category successfully deleted"})

    @staticmethod
    @parse_params(
        Argument("name", location="json", required=True,
                 help="The name of the category."),
        Argument("sku", location="json", required=True,
                 help="The sku of the category."),
        Argument("products", location="json", required=True,
                 help="The product of the category.")
    )
    def post(name, sku, products):
        """ Create a category """
        category = CategoriesRepository.create(
            name=name, sku=sku, products=products
        )
        return jsonify({"data": category.json})