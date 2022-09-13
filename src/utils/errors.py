import sys


class InternalServerError(Exception):
    pass
    """ def __init__(self):
        self.code = 500

        print(sys.exc_info())
        return {
            "error": "Internal server error",
            "code": self.code
        } """


class SchemaValidationError(Exception):
    pass


class UserNotFound(Exception):
    def __init__(self, message) -> None:
        self.code = 404
        self.message = message


class UpdatingMovieError(Exception):
    pass


class DeletingMovieError(Exception):
    pass


class MovieNotExistsError(Exception):
    pass


class EmailAlreadyExistsError(Exception):
    pass


class UnauthorizedError(Exception):
    pass


errors = {
    "InternalServerError": {
        "message": "Something went wrong",
        "status": 500
    },
    "SchemaValidationError": {
        "message": "Request is missing required fields",
        "status": 400
    },
    "UserNotFound": {
        "message": "User with given name already exists",
        "status": 400
    },
    "UpdatingMovieError": {
        "message": "Updating movie added by other is forbidden",
        "status": 403
    },
    "DeletingMovieError": {
        "message": "Deleting movie added by other is forbidden",
        "status": 403
    },
    "MovieNotExistsError": {
        "message": "Movie with given id doesn't exists",
        "status": 400
    },
    "EmailAlreadyExistsError": {
        "message": "User with given email address already exists",
        "status": 400
    },
    "UnauthorizedError": {
        "message": "Invalid username or password",
        "status": 401
    }
}
