class AdminAlreadyExistsError(Exception):
    pass


class UserNotFound(Exception):
    pass


class PublisherNotFound(Exception):
    pass


class AuthorNotFound(Exception):
    pass


class CategoryNotFound(Exception):
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


class PublisherInUse(Exception):
    pass


class CategoryInUse(Exception):
    pass


class AuthorInUse(Exception):
    pass
