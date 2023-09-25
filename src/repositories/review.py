""" Defines the Review repository """


import sys

from flask import jsonify
from sqlalchemy.exc import IntegrityError

from models import Review, db
from utils.errors import DataNotFound, DuplicateData, InternalServerError


class ReviewRepository:
    """ The repository for the review model """

    @staticmethod
    def get(review_id=None):
        """ Query a review by review_id """

        # make sure one of the parameters was passed
        if not review_id:
            raise DataNotFound("Review not found, no detail provided")

        try:
            query = Review.query
            if review_id:
                query = query.filter(Review.id == review_id)

            review_item = query.first()
            return review_item

        except DataNotFound:
            print(sys.exc_info())
            raise DataNotFound(f"Review with {review_id} not found")

    @staticmethod
    def getAll():
        """ Query all reviews """

        all_reviews = db.session.query(Review).all()
        data = []
        for rev in all_reviews:
            data.append({
                "id": rev.id,
                "comment": rev.comment,
                "images": rev.images,
                "sellers_id": rev.sellers_id,
                "products_id": rev.products_id,
            })

        return data

    @staticmethod
    def create(comment, images, sellers_id, products_id):
        """ Create a new review """

        try:
            created_review = Review(comment=comment, images=images,
                                    sellers_id=sellers_id,
                                    products_id=products_id)
            review = created_review.save()
            return jsonify({
                "comment": review.comment,
                "images": review.images,
                "sellers_id": review.sellers_id,
                "products_id": review.products_id,
            })

        except IntegrityError as e:
            message = e.orig.diag.message_detail
            raise DuplicateData(message)

        except Exception:
            raise InternalServerError

    def update(self, review_id, **args):
        """ Update a reviews """

        review = self.get(review_id)
        if 'comment' in args and args['comment'] is not None:
            review.comment = args['comment']

        if 'images' in args and args['images'] is not None:
            review.images = args['images']

        return review.save()

    @staticmethod
    def delete(review_id):
        """ Delete a review by review_id """

        if not review_id:
            raise DataNotFound("Review not found, no id provided")

        try:
            query = Review.query.filter(Review.id == review_id).first()
            return query.delete()

        except DataNotFound:
            print(sys.exc_info())
            raise DataNotFound(f"Review with {review_id} not found")
