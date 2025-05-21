class AdminAlreadyExistsError(Exception):
    pass


class UserNotFound(Exception):
    pass


class DuplicateEmailError(Exception):
    pass


class DatabaseOperationError(Exception):
    pass


class ValidationFailedError(Exception):
    pass


class DuplicateNameError(Exception):
    pass


class DuplicateISBNError(Exception):
    pass


class BookNotFound(Exception):
    pass
