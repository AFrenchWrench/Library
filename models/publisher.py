from __future__ import annotations
from mysql.connector import Error
from db import get_connection
from models.validators import PublisherValidator
from models.db_exceptions import (
    DatabaseOperationError,
    DuplicateNameError,
    UserNotFound,
    ValidationFailedError,
)


class Publisher:
    def __init__(self, name: str, id: int | None = None) -> None:
        self.id: int | None = id
        self.name: str = name

    def validate(self) -> None:
        validator = PublisherValidator()
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
                    f"Publisher with name '{self.name}' already exists."
                )
            raise DatabaseOperationError(f"Unexpected database error: {err}") from err

    def _build_query(self) -> tuple[str, tuple]:
        if self.id is None:
            return (
                "INSERT INTO publishers (name) VALUES (%s)",
                (self.name,),
            )
        else:
            return (
                "UPDATE publishers SET name=%s WHERE id=%s",
                (self.name, self.id),
            )

    @classmethod
    def get_by_id(cls, id: int) -> Publisher:
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cur:
                cur.execute("SELECT * FROM publishers WHERE id=%s", (id,))
                row = cur.fetchone()
        if not row:
            raise UserNotFound(f"No publisher found with ID {id}")
        return cls(**row)

    @classmethod
    def delete_all(cls) -> None:
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("DELETE FROM publishers;")
                    conn.commit()
        except Exception as e:
            raise DatabaseOperationError("Failed to delete publishers.") from e
