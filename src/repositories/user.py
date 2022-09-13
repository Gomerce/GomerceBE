""" Defines the User repository """
from models import User
from utils.errors import *


class UserRepository:
    """ The repository for the user model """

    @staticmethod
    def get(user_id):
        """ Query a user by user_id """
        user = User.query.filter(User.user_id == user_id).first()

        if user is None:
            raise UserNotFound(f"User with {user_id} not found")
        return user

    @staticmethod
    def getAll():
        """ Query all users"""
        users = User.query.all()
        all_users = [user.json for user in users]
        return all_users

    def update(self, user_id, **args):
        """ Update a user's age """
        user = self.get(user_id)
        if 'age' in args and args['age'] is not None:
            user.age = args['age']

        if 'last_name' in args and args['last_name'] is not None:
            user.last_name = args['last_name']

        if 'first_name' in args and args['first_name'] is not None:
            user.first_name = args['first_name']

        return user.save()

    @staticmethod
    def create(last_name, first_name, age):
        """ Create a new user """
        user = User(last_name=last_name, first_name=first_name, age=age)
        return user.save()
