""" Defines the Store repository """
import sys
from sqlalchemy import or_, and_
from models import Store
from utils.errors import DataNotFound, DuplicateData, InternalServerError
from sqlalchemy.exc import IntegrityError, DataError


class StoreRepository:
    """ The repository for the Store model """

    @staticmethod
    def get(store_id=None, name=None, email=None, phone=None):
        """ Query a Store by store_id """

        # make sure one of the parameters was passed
        if not store_id and not name and not email and not phone:
            raise DataNotFound(f"Store not found, no detail provided")

        try:
            query = Store.query
            if store_id:
                query = query.filter(Store.id == store_id)
            if name:
                query = query.filter(
                    or_(Store.name == name, Store.email == name, Store.phone == name))
            if email:
                query = query.filter(
                    or_(Store.email == email, Store.name == email, Store.phone == email))
            if phone:
                query = query.filter(
                    or_(Store.phone == phone, Store.email == phone, Store.name == phone))

            store = query.first()
            return store
        except:
            print(sys.exc_info())
            raise DataNotFound(f"Store with {store_id} not found")

    @staticmethod
    def getAll():
        """ Query all Stores"""
        stores = Store.query.all()
        all_stores = [s.json for s in stores]
        return all_stores

    def update(self, store_id, **args):
        """ Update a Store's age """
        store = self.get(store_id)
        if 'phone' in args and args['phone'] is not None:
            store.phone = args['phone']

        if 'name' in args and args['name'] is not None:
            store.name = args['name']

        if 'email' in args and args['email'] is not None:
            store.email = args['email']
        if 'address' in args and args['address'] is not None:
            store.address = args['address']
        if 'email_verified' in args and args['email_verified'] is not None:
            store.email_verified = args['email_verified']
        if 'phone_verified' in args and args['phone_verified'] is not None:
            store.phone_verified = args['phone_verified']

        return store.save()

    @staticmethod
    def create(name, address, email=None, phone=None, email_verified=None,
               phone_verified=None, sellers_id=None):
        """ Create a new Store """
        try:
            new_Store = Store(name=name, address=address,
                              email=email, phone=phone,
                              email_verified=email_verified,
                              phone_verified=phone_verified,
                              sellers_id=sellers_id
                              )

            return new_Store.save()
        except IntegrityError as e:
            message = e.orig.diag.message_detail
            raise DuplicateData(message)
        except Exception:
            raise InternalServerError
