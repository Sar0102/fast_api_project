class ProductAlreadyExistsError(Exception):
    def __init__(self):
        message = "Product already exist!"
        super().__init__(message)


class ProductNotFoundError(Exception):
    def __init__(self):
        message = "Not found!"
        super().__init__(message)
