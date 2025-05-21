from __future__ import annotations
from mysql.connector import Error
from db import get_connection
from models.validators import AuthorValidator
from models.db_exceptions import (
    DatabaseOperationError,
    DuplicateNameError,
    UserNotFound,
    ValidationFailedError,
)


class Author:
    def __init__(self, name: str, id: int | None = None) -> None:
        self.id: int | None = id
        self.name: str = name

    def validate(self) -> None:
        validator = AuthorValidator()
        validator.validate(self)

    def save(self) -> bool:
        try:
            self.validate()
        except ValueError as e:
            raise ValidationFailedError(f"Validation failed:\n{e}") from e

        query, values = self._build_query()

        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, values)
                    if self.id is None:
                        self.id = cur.lastrowid
                    conn.commit()
            return True
        except Error as err:
            if err.errno == 1062 and "name" in err.msg.lower():
                raise DuplicateNameError(
                    f"Author with name '{self.name}' already exists."
                )
            raise DatabaseOperationError(f"Unexpected database error: {err}") from err

    def _build_query(self) -> tuple[str, tuple]:
        if self.id is None:
            return (
                "INSERT INTO authors (name) VALUES (%s)",
                (self.name,),
            )
        else:
            return (
                "UPDATE authors SET name=%s WHERE id=%s",
                (self.name, self.id),
            )

    @classmethod
    def get_by_id(cls, id: int) -> Author:
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cur:
                cur.execute("SELECT * FROM authors WHERE id=%s", (id,))
                row = cur.fetchone()
        if not row:
            raise UserNotFound(f"No author found with ID {id}")
        return cls(**row)

    @classmethod
    def delete_all(cls) -> None:
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("DELETE FROM authors;")
                    conn.commit()
        except Exception as e:
            raise DatabaseOperationError("Failed to delete authors.") from e
