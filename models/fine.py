from __future__ import annotations
from mysql.connector import Error
from db import get_connection
from models.exceptions import (
    ValidationFailedError,
    DatabaseOperationError,
    FineNotFound,
)
from models.validators import FineValidator

FINE_STATUSES = {"all", "paid", "unpaid"}


class Fine:
    def __init__(
        self,
        user_id: int,
        loan_id: int,
        amount: float,
        paid: bool = False,
        id: int | None = None,
    ) -> None:
        self.id = id
        self.user_id = user_id
        self.loan_id = loan_id
        self.amount = amount
        self.paid = paid

    def validate(self) -> None:
        validator = FineValidator()
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
            raise DatabaseOperationError(f"Database error: {err}") from err

    def _build_query(self) -> tuple[str, tuple]:
        if self.id is None:
            return (
                "INSERT INTO fines (user_id, loan_id, amount, paid) VALUES (%s, %s, %s, %s)",
                (self.user_id, self.loan_id, self.amount, self.paid),
            )
        else:
            return (
                "UPDATE fines SET paid=%s WHERE id=%s",
                (self.paid, self.id),
            )

    @classmethod
    def get_by_id(cls, fine_id: int) -> Fine:
        try:
            with get_connection() as conn:
                with conn.cursor(dictionary=True) as cur:
                    cur.execute("SELECT * FROM fines WHERE id = %s", (fine_id,))
                    row = cur.fetchone()
                    if not row:
                        raise FineNotFound(f"No fine found with ID {fine_id}")
                    return cls(**row)
        except Error as err:
            raise DatabaseOperationError(f"Failed to get fine by ID: {err}") from err

    @classmethod
    def get_by_user(cls, user_id: int, status: str = "all") -> list[Fine]:
        try:
            if status not in FINE_STATUSES:
                raise ValueError(
                    """Status should be:
                        all for all types of fines
                        paid for paid fines
                        unpaid for unpaid fines"""
                )

            query = "SELECT * FROM fines WHERE user_id = %s"
            params = [user_id]

            if status == "paid":
                query += " AND paid = TRUE"
            elif status == "unpaid":
                query += " AND paid = FALSE"

            with get_connection() as conn:
                with conn.cursor(dictionary=True) as cur:
                    cur.execute(query, params)
                    rows = cur.fetchall()
                    if not rows:
                        raise FineNotFound(f"No fines found for user with ID {user_id}")
                    return [cls(**row) for row in rows]
        except Error as err:
            raise DatabaseOperationError(f"Failed to get fines by user: {err}") from err

    @classmethod
    def get_by_loan(cls, loan_id: int) -> Fine:
        try:
            with get_connection() as conn:
                with conn.cursor(dictionary=True) as cur:
                    cur.execute("SELECT * FROM fines WHERE loan_id = %s", (loan_id,))
                    row = cur.fetchone()
                    if not row:
                        raise FineNotFound(f"No fine found for loan with ID {loan_id}")
                    return cls(**row)
        except Error as err:
            raise DatabaseOperationError(
                f"Failed to get fine by loan ID: {err}"
            ) from err

    @classmethod
    def get_all(cls):
        try:
            with get_connection() as conn:
                with conn.cursor(dictionary=True) as cur:
                    cur.execute("SELECT * FROM fines")
                    results = cur.fetchall()
                    return [cls(**row) for row in results]
        except Error as err:
            raise Exception(f"Failed to fetch fines: {err}")

    @classmethod
    def delete_by_id(cls, fine_id: int) -> None:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM fines WHERE id = %s", (fine_id,))
                if cur.rowcount == 0:
                    raise FineNotFound(f"Fine with ID {fine_id} not found.")
                conn.commit()
