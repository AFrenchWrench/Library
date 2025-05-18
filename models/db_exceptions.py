class AdminAlreadyExistsError(Exception):
    """Raised when trying to insert a second admin."""

    pass


class UserNotFound(Exception):
    """Raised when no user is found with the given email."""

    pass


class DuplicateEmailError(Exception):
    """Raised when trying to use an email that already exists."""

    pass


class DatabaseOperationError(Exception):
    """Generic DB operation failure."""

    pass


class ValidationFailedError(Exception):
    """Raised when validation fails."""

    pass
