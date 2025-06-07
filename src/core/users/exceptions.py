class TokenIsNotValidException(Exception):
    def __init__(self):
        message = "Taken is invalid!"
        super().__init__(message)


class UserAlreadyExistsException(Exception):
    def __init__(self, username):
        message = f"User with username '{username}' already exists!"
        super().__init__(message)


class ServiceError(Exception):
    pass
