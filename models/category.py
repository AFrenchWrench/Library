from __future__ import annotations
from mysql.connector import Error
from db import get_connection
from models.validators import CategoryValidator
from models.exceptions import (
    DatabaseOperationError,
    DuplicateNameError,
    CategoryNotFound,
    ValidationFailedError,
    CategoryInUse,
)


class Category:
    def __init__(self, name: str, id: int | None = None) -> None:
        self.id = id
        self.name = name

    def validate(self) -> None:
        validator = CategoryValidator()
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
                    f"Category with name '{self.name}' already exists."
                )
            raise DatabaseOperationError(f"Unexpected database error: {err}") from err

    def _build_query(self) -> tuple[str, tuple]:
        if self.id is None:
            return (
                "INSERT INTO categories (name) VALUES (%s)",
                (self.name,),
            )
        else:
            return (
                "UPDATE categories SET name=%s WHERE id=%s",
                (self.name, self.id),
            )

    @classmethod
    def get_by_name(cls, name: str) -> Category:
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cur:
                cur.execute("SELECT * FROM categories WHERE name=%s", (name,))
                row = cur.fetchone()
        if not row:
            raise CategoryNotFound(f"No category found with name '{name}'")
        return cls(**row)

    @classmethod
    def delete_by_name(cls, name: str) -> None:
        try:
            with get_connection() as conn:
                with conn.cursor(dictionary=True) as cur:
                    cur.execute("SELECT id FROM categories WHERE name = %s", (name,))
                    result = cur.fetchone()
                    if not result:
                        raise CategoryNotFound(f"No category found with name '{name}'")

                    category_id = result["id"]

                    try:
                        cur.execute(
                            "DELETE FROM categories WHERE id = %s", (category_id,)
                        )
                        conn.commit()
                    except Error as err:
                        if err.errno == 1451:
                            cur.execute(
                                "SELECT title FROM books WHERE category_id = %s",
                                (category_id,),
                            )
                            books = cur.fetchall()
                            titles = [row["title"] for row in books]
                            title_list = ", ".join(f"'{t}'" for t in titles)
                            raise CategoryInUse(
                                f"Cannot delete category '{name}' because it is referenced by the following books: {title_list}"
                            ) from err
                        raise

        except Error as err:
            raise DatabaseOperationError("Failed to delete category.") from err
