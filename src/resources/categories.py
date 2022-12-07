"""
Define the resources for the Catgories
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
    def get_category(category_id):
        """ get product category """

        try:
            products = CategoriesRepository.get(category_id=category_id)
            return jsonify({"data": products.json})
        except DataNotFound as e:
            abort(404, e.message)
        except Exception:
            abort(500)

    @staticmethod
    @swag_from("../swagger/category/get_all.yml")
    def get_all():
        """ Return all category key information based on the query parameter """
        caetgories = CategoriesRepository.getAll()
        return jsonify({"data": caetgories})

    @staticmethod
    @parse_params(
        Argument("sku", location="json",
                 help="The sku of the category."),
        Argument("name", location="json",
                 help="The name of the category.")
    )
    def update_category(category_id, name, sku):
        """ Update a category based on the provided information """
        repository = CategoriesRepository()
        category = repository.update(
            category_id=category_id, name=name, sku=sku
        )
        return jsonify({"data": category.json})

    @staticmethod
    @parse_params(
        Argument("sku", location="json",
                 help="The sku of the category."),
        Argument("name", location="json",
                 help="The name of the category."),
    )
    def post(name, sku, products):
        """ Create a category based on the provided information """
        category = CategoriesRepository.create(
            name=name,
            sku=sku
        )
        return jsonify({"data": category.json})
