""" Defines the Status repository """
import sys
from sqlalchemy import or_, and_
from models import Status, db
from utils.errors import DataNotFound, DuplicateData, InternalServerError
from sqlalchemy.exc import IntegrityError, DataError


class StatusRepository:
    """ The repository for the Status model """

    @staticmethod
    def get(status_id=None):
        """ Query a Status by status_id """

        # make sure one of the parameters was passed
        if not status_id:
            raise DataNotFound(f"Status not found, no detail provided")

        try:
            query = Status.query
            if status_id:
                query = query.filter(Status.id == status_id)

            status = query.first()
            return status
        except:
            print(sys.exc_info())
            raise DataNotFound(f"Status with {status_id} not found")

    @staticmethod
    def getAll():
        """ Query all categories"""
        status = db.session.query(Status).all()
        data = []
        for st in status:
            data.append({
                "status": st.status,
                "order_id": st.order_id,
            })
        return data

    def update(self, status_id, **args):
        """ Update a Status's  """
        status = self.get(status_id)
        if not status:
            raise DataNotFound(f"Status Detail with {status_id} not found")

        if 'status' in args and args['status'] is not None:
            status.status = args['status']

        if 'order_id' in args and args['order_id'] is not None:
            status.order_id = args['order_id']
        return status.save()

    @staticmethod
    def create(status, order_id):
        """ Create a new Status """
        try:
            new_Status = Status(status=status, order_id=order_id)

            return new_Status.save()
        except IntegrityError as e:
            message = e.orig.diag.message_detail
            raise DuplicateData(message)
        except Exception:
            raise InternalServerError

    @staticmethod
    def delete(status_id):
        """ Delete a status by id """
        if not status_id:
            raise DataNotFound(f"Status not found")

        try:
            query = Status.query.filter(Status.id == status_id).first()
            if not query:
                raise DataNotFound(f"Status Detail with {status_id} not found")
            return query.delete()
        except DataNotFound as e:
            print(sys.exc_info())
            raise DataNotFound(f"Status with {status_id} not found")
