"""
Defines the blueprint for the reviews
"""
from flask import Blueprint

from resources import ReviewResource

REVIEW_BLUEPRINT = Blueprint("review", __name__)

REVIEW_BLUEPRINT.route(
    "/reviews", methods=['GET'])(ReviewResource.get_all)
REVIEW_BLUEPRINT.route("/reviews/<int:review_id>",
                         methods=['GET'])(ReviewResource.get_one)
