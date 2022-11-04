"""
Defines the blueprint for the categories
"""
from flask import Blueprint

from resources import CategoriesResource

CATEGORIES_BLUEPRINT = Blueprint("categories", __name__)

CATEGORIES_BLUEPRINT.route(
    "/categories/<int:search_id>", methods=['GET'])(CategoriesResource.get_category_product)
CATEGORIES_BLUEPRINT.route(
    "/categories", methods=['GET'])(CategoriesResource.get_all)
CATEGORIES_BLUEPRINT.route(
    "/categories", methods=['POST'])(CategoriesResource.post)