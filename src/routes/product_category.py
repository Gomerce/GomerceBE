"""
Defines the blueprint for the product categories
"""
# from crypt import methods
from flask import Blueprint

from resources import ProductCategoryResource

CATEGORY_BLUEPRINT = Blueprint("category", __name__)

CATEGORY_BLUEPRINT.route(
    "/categories", methods=['GET'])(ProductCategoryResource.get_all)

CATEGORY_BLUEPRINT.route("/categories/<int:product_category_id>",
                        methods=['GET'])(ProductCategoryResource.get_one)

CATEGORY_BLUEPRINT.route("/categories", methods=['POST'])(ProductCategoryResource.post)

CATEGORY_BLUEPRINT.route("categories/<int:category_id>",
                        methods=["DELETE"])(ProductCategoryResource.delete)

CATEGORY_BLUEPRINT.route("categories/<int:category_id>",
                       methods=["PUT"])(ProductCategoryResource.update_category)
