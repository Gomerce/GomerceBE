"""
Define the resources for the product categories
"""
from flasgger import swag_from
from flask import abort, jsonify
from flask_restful import Resource
from flask_restful.reqparse import Argument

from repositories import ProductCategoryRepository
from utils import parse_params
from utils.errors import DataNotFound
from validators.auth import requires_auth


class ProductCategoryResource(Resource):
    """ methods relative to the product Category """

    @staticmethod
    @swag_from("../swagger/product_category/get_one.yml")
    def get_one(product_category_id):
        """ Return a product category key information based on product_category_id """

        try:
            category = ProductCategoryRepository.get(
                product_category_id=product_category_id)
            if not category:
                return jsonify(
                    {"message": f" Category with the id {product_category_id} not found"})

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
    @swag_from("../swagger/product_category/get_all.yml")
    def get_all():
        """ Return all categories key information based on the query parameter """
        product_categories = ProductCategoryRepository.getAll()
        return jsonify({"data": product_categories})

    @staticmethod
    @parse_params(
        Argument("name", location="json",
                 help="The name of the product_category."),
        Argument("sku", location="json",
                 help="The sku of the product_category.")
    )
    @swag_from("../swagger/product_category/post.yml")
    @requires_auth('post:product_category')
    def post(name, sku):
        """ Create a category based on the provided information """
        # Check duplicates
        if name is None:
            abort(400, 'Name cannot be null')
        if name == "":
            abort(400, 'Name cannot be empty')
        if sku is None:
            abort(400, 'SKU cannot be null')
        if sku == "":
            abort(400, 'SKU cannot be empty')
        product_category = ProductCategoryRepository.create(
            name=name, sku=sku
        )
        return jsonify({"data": product_category.json})

    @swag_from("../swagger/product_category/delete.yml")
    @requires_auth('delete:product_category')
    def delete(category_id):
        """ delete a category based on the category id provided """
        # fetch category
        category = ProductCategoryRepository

        if not (category.get(category_id)):
            abort(404, f"Category with id {category_id} not found.")
        category.delete(category_id=category_id)

        return jsonify({"message": "category successfully deleted"})

    @staticmethod
    @parse_params(
        Argument("name", location="json",
                 help="The name of the product_category."),
        Argument("sku", location="json",
                 help="The sku of the product_category.")
    )
    @swag_from("../swagger/product_category/put.yml")
    @requires_auth('patch:product_category')
    def update_category(category_id, name, sku):
        """ Update a category based on the provided information """
        print(category_id)
        repository = ProductCategoryRepository()

        if not (repository.get(category_id)):
            abort(404, f"Category with id {category_id} not found.")
        if name is None:
            abort(400, 'Name cannot be null')
        if name == "":
            abort(400, 'Name cannot be empty')
        if sku is None:
            abort(400, 'SKU cannot be null')
        if sku == "":
            abort(400, 'SKU cannot be empty')
        category = repository.update(
            category_id=category_id, name=name, sku=sku
        )
        return jsonify({"message": category.json})
