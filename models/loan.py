from __future__ import annotations
from datetime import date, timedelta
from mysql.connector import Error
from db import get_connection
from models.exceptions import (
    ValidationFailedError,
    DatabaseOperationError,
    LoanNotFound,
)
from models.validators import LoanValidator


class Loan:

    def __init__(
        self,
        user_id: int,
        book_id: int,
        loan_date: date = date.today(),
        due_date: date = date.today() + timedelta(days=14),
        return_date: date | None = None,
        id: int | None = None,
    ) -> None:
        self.id = id
        self.user_id = user_id
        self.book_id = book_id
        self.loan_date = loan_date
        self.due_date = due_date
        self.return_date = return_date

    def validate(self) -> None:
        validator = LoanValidator()
        validator.validate(self, False if self.id else True)

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
            raise DatabaseOperationError(f"Database error: {err}") from err

    def _build_query(self) -> tuple[str, tuple]:
        if self.id is None:
            return (
                "INSERT INTO loans (user_id, book_id, loan_date, due_date, return_date) VALUES (%s, %s, %s, %s, %s)",
                (
                    self.user_id,
                    self.book_id,
                    self.loan_date,
                    self.due_date,
                    self.return_date,
                ),
            )
        else:
            return (
                "UPDATE loans SET return_date=%s WHERE id=%s",
                (self.return_date, self.id),
            )

    @classmethod
    def get_by_user(cls, user_id: int, status: str = "all") -> list[Loan]:
        try:
            if status not in ["all", "active", "returned"]:
                raise ValueError(
                    """Status should be:
                        all for all types of loans
                        active for loans that are not returned
                        returned for the loans that are returned"""
                )

            query = "SELECT * FROM loans WHERE user_id = %s"
            params = [user_id]

            if status == "active":
                query += " AND return_date IS NULL"
            elif status == "returned":
                query += " AND return_date IS NOT NULL"

            with get_connection() as conn:
                with conn.cursor(dictionary=True) as cur:
                    cur.execute(query, params)
                    rows = cur.fetchall()
                    if not rows:
                        raise LoanNotFound(f"No loan found for user with ID {user_id}")
                    return [cls(**row) for row in rows]

        except Error as err:
            raise DatabaseOperationError(f"Failed to get loans by user: {err}") from err

    @classmethod
    def get_by_book(cls, book_id: int, status: str = "all") -> list[Loan]:
        try:
            if status not in ["all", "active", "returned"]:
                raise ValueError(
                    """Status should be:
                        all for all types of loans
                        active for loans that are not returned
                        returned for the loans that are returned"""
                )

            query = "SELECT * FROM loans WHERE book_id = %s"
            params = [book_id]

            if status == "active":
                query += " AND return_date IS NULL"
            elif status == "returned":
                query += " AND return_date IS NOT NULL"

            with get_connection() as conn:
                with conn.cursor(dictionary=True) as cur:
                    cur.execute(query, params)
                    rows = cur.fetchall()
                    if not rows:
                        raise LoanNotFound(f"No loan found for book with ID {book_id}")
                    return [cls(**row) for row in rows]

        except Error as err:
            raise DatabaseOperationError(f"Failed to get loans by book: {err}") from err

    @classmethod
    def get_by_id(cls, loan_id: int) -> Loan:
        try:
            with get_connection() as conn:
                with conn.cursor(dictionary=True) as cur:
                    cur.execute("SELECT * FROM loans WHERE id = %s", (loan_id,))
                    row = cur.fetchone()
                    if not row:
                        raise LoanNotFound(f"No loan found with ID {loan_id}")
                    return cls(**row)
        except Error as err:
            raise DatabaseOperationError(f"Failed to get loan by ID: {err}") from err
