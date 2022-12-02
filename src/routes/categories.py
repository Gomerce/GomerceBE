"""
Defines the blueprint for the categories
"""
"""
Defines the blueprint for the categories
"""
from flask import Blueprint

from resources import CategoriesResource

CATEGORIES_BLUEPRINT = Blueprint("categories", __name__)

CATEGORIES_BLUEPRINT.route(
    "/categories", methods=['GET'])(CategoriesResource.get_all)
CATEGORIES_BLUEPRINT.route(
    "/categories", methods=['POST'])(CategoriesResource.post)
CATEGORIES_BLUEPRINT.route("/categories/<int:category_id>",
                           methods=['GET'])(CategoriesResource.get_category)