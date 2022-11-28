"""
Define the resources for the review
"""
from flask import jsonify, abort
from flasgger import swag_from
from flask_restful import Resource
from flask_restful.reqparse import Argument
from repositories import ReviewRepository
from utils import parse_params
from utils.errors import DataNotFound


class ReviewResource(Resource):
    """ methods relative to the review """

    @staticmethod
    @swag_from("../swagger/review/get_one.yml")
    def get_one(review_id):
        """ Return a review key information based on review_id """

        try:
            review = ReviewRepository.get(review_id=review_id)
            return jsonify({"data": review.json})
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
