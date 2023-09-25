""" Defines the VerificationToken repository """


from datetime import datetime, timedelta

from models import VerificationToken
from utils.errors import DataNotFound, ResourceNotCreated
from utils.utilities import generate_token


class VerificationTokenRepository:
    """ The repository for the verification_token model """

    @staticmethod
    def get(user_id, token, user_type, status=None):
        """ Query a token by data provided """

        # make sure the parameters were passed
        if not user_id or not token or not user_type:
            raise DataNotFound("VerificationToken not found, some details not provided")  # noqa

        query = VerificationToken.query.filter(VerificationToken.token == token,  # noqa
                                               VerificationToken.user_id == user_type,  # noqa
                                               VerificationToken.user_type == user_type)  # noqa
        if status is not None:
            query.filter(VerificationToken.used_status == status)

        return query.first()

    def update(self, user_id, token, user_type):
        """ Update a token """

        token = self.get(user_id, token, user_type, status=False)
        if token is None:
            raise DataNotFound("VerificationToken not found")

        token.used_status = True
        token.expires_at = datetime.now()
        token.updated_at = datetime.now()

        return token.save()

    @classmethod
    def create(cls, user_id, user_type, email, phone, length=16):
        """ Create a new token """

        token = generate_token(length)
        existing_token = cls.get(
            token=token, user_id=user_id, user_type=user_type)
        while existing_token:
            token = generate_token(length)
            existing_token = cls.get(
                token=token, user_id=user_id, user_type=user_type)

        expiry = datetime.now() + timedelta(minutes=10)

        try:
            new_token = VerificationToken(token=token, user_id=user_id,
                                          user_type=user_type,
                                          expires_at=expiry, email_token=email,
                                          phone_token=phone
                                          )

        except ResourceNotCreated:
            raise ResourceNotCreated("VerificationToken not created")
        return new_token
