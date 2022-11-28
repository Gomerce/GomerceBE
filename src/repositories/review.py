""" Defines the Review repository """
import sys
from sqlalchemy import or_, and_
from models import Review
from utils.errors import DataNotFound, DuplicateData, InternalServerError
from sqlalchemy.exc import IntegrityError, DataError


class ReviewRepository:
    """ The repository for the review model """

    @staticmethod
    def get(review_id=None):
        """ Query a review by review_id """

        # make sure one of the parameters was passed
        if not review_id:
            raise DataNotFound(f"Review not found, no detail provided")

        try:
            query = Review.query
            if review_id:
                query = query.filter(Review.id == review_id)

            review_item = query.first()
            return review_item
        except:
            print(sys.exc_info())
            raise DataNotFound(f"Review with {review_id} not found")

    @staticmethod
    def getAll():
        """ Query all reviews """
        reviews = Review.query.all()
        all_reviews = [review_item.json for review_item in reviews]
        return all_reviews

