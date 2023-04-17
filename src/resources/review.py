"""
Define the resources for the review
"""
import json

from flasgger import swag_from
from flask import abort, jsonify
from flask_restful import Resource
from flask_restful.reqparse import Argument

from repositories import ReviewRepository
from utils import parse_params
from utils.errors import DataNotFound
from validators.auth import requires_auth


class ReviewResource(Resource):
    """ methods relative to the review """

    @staticmethod
    @swag_from("../swagger/review/get_one.yml")
    def get_one(review_id):
        """ Return a review """

        try:
            review = ReviewRepository.get(review_id=review_id)
            if not review:
                return jsonify(
                    {"message": f"review with id {review_id} not found"})
            data = {
                "id": review.id,
                "comment": review.comment,
                "images": review.images,
                "sellers_id": review.sellers_id,
                "products_id": review.products_id,
            }
            return jsonify({"data": data})
        except DataNotFound as e:
            abort(404, e.message)
        except Exception:
            abort(500)

    @staticmethod
    @swag_from("../swagger/review/get_all.yml")
    def get_all():
        """ Return all review key information based on the query parameter """
        reviews = ReviewRepository.getAll()
        return jsonify({"data": reviews})

    @staticmethod
    @parse_params(
        Argument("comment", location="json",
                 help="The comment for a review."),
        Argument("images", location="json",
                 help="The image for a review."),
        Argument("sellers_id", location="json",
                 help="The sellers_id for a review"),
        Argument("products_id", location="json",
                 help="The products_id for a review"),
    )
    @requires_auth('post:review')
    def post(comment, images, sellers_id, products_id):
        """ Create a review """
        review = ReviewRepository.create(
            comment=comment, images=images,
            sellers_id=sellers_id,
            products_id=products_id
        )
        return jsonify({"data": review.json})

    @staticmethod
    @parse_params(
        Argument("comment", location="json",
                 help="The comment for a review."),
        Argument("images", location="json",
                 help="The image for a review.")
    )
    @requires_auth('patch:review')
    def update(review_id, comment, images):
        """ Update a review"""
        repo = ReviewRepository()
        review = repo.update(
            review_id=review_id, comment=comment, images=images
        )
        data = {
            "comment": review.comment,
            "id": review.id,
            "images": review.images,
            "sellers_id": review.sellers_id,
            "products_id": review.products_id,
        }

        return jsonify({"data": data})

    @requires_auth('delete:review')
    def delete(review_id):
        """ delete a review via the provided id """
        ReviewRepository.delete(review_id=review_id)
        return jsonify({"message": "review successfully deleted"})
