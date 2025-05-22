from __future__ import annotations
from typing import Literal
from datetime import date
from mysql.connector import Error
from auth import hash_password
from db import get_connection
from models.validators import MemberValidator
from models.db_exceptions import (
    AdminAlreadyExistsError,
    UserNotFound,
    DuplicateEmailError,
    DatabaseOperationError,
    ValidationFailedError,
)


class Member:
    def __init__(
        self,
        name: str,
        email: str,
        password: str,
        id: int | None = None,
        joined_date: date = date.today(),
        role: Literal["member", "admin"] = "member",
    ) -> None:
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.joined_date = joined_date
        self.role = role

    def validate(self) -> None:
        validator = MemberValidator()
        validator.validate(self)

    def prepare_for_save(self):
        self.password = hash_password(self.password)

    def save(self) -> bool:
        try:
            self.validate()
            self.prepare_for_save()
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
            if err.errno == 1644:
                raise AdminAlreadyExistsError("Only one admin is allowed.") from err
            elif err.errno == 1062 and "email" in err.msg.lower():
                raise DuplicateEmailError(
                    f"A member with this email already exists: {self.email}"
                ) from err
            else:
                raise DatabaseOperationError(
                    f"Unexpected database error: {err}"
                ) from err

    def _build_query(self) -> tuple[str, tuple]:
        if self.id is None:
            return (
                "INSERT INTO members (name, email, password, joined_date, role) VALUES (%s, %s, %s, %s, %s)",
                (self.name, self.email, self.password, self.joined_date, self.role),
            )
        else:
            return (
                "UPDATE members SET name=%s, email=%s, password=%s WHERE id=%s",
                (self.name, self.email, self.password, self.id),
            )

    @classmethod
    def get_by_email(cls, email: str) -> Member:
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cur:
                cur.execute("SELECT * FROM members WHERE email=%s", (email,))
                row = cur.fetchone()
        if not row:
            raise UserNotFound(f"No user found with the email: {email}")
        return cls(**row)

    @classmethod
    def delete_by_email(cls, email: str) -> None:
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("DELETE FROM members WHERE email=%s", (email,))
                    if cur.rowcount == 0:
                        raise UserNotFound(f"No user found with the email: {email}")
                    conn.commit()
        except Error as err:
            raise DatabaseOperationError(
                f"Failed to delete user with email {email}."
            ) from err

    @classmethod
    def delete_all(cls) -> None:
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("DELETE FROM members;")
                    conn.commit()
        except Exception as e:
            raise DatabaseOperationError("Failed to delete members.") from e
